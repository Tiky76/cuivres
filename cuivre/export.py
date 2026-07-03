from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import sqlite3
from datetime import datetime

from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class Export(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="📊 RAPPORTS USINE CUIVRE",
            font_size=24,
            size_hint=(1, 0.2)
        )

        # ================= BOUTONS =================
        btn_journalier = Button(text="📅 Bilan Journalier")
        btn_finance = Button(text="💰 Rapport Financier")
        btn_excel = Button(text="📊 Export Excel")
        btn_pdf = Button(text="📄 Export PDF")
        btn_back = Button(text="⬅ Retour")

        btn_journalier.bind(on_press=self.bilan_journalier)
        btn_finance.bind(on_press=self.rapport_financier)
        btn_excel.bind(on_press=self.export_excel)
        btn_pdf.bind(on_press=self.export_pdf)
        btn_back.bind(on_press=self.go_back)

        layout.add_widget(titre)
        layout.add_widget(btn_journalier)
        layout.add_widget(btn_finance)
        layout.add_widget(btn_excel)
        layout.add_widget(btn_pdf)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= CONNEXION =================
    def get_conn(self):
        return sqlite3.connect("usine.db")

    # ================= KPI GLOBAL =================
    def kpi(self):

        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("SELECT COALESCE(SUM(quantite),0) FROM production")
        prod = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(minerai),0), COALESCE(SUM(cathodes),0) FROM stock")
        minerai, cathodes = cur.fetchone()

        conn.close()

        return prod, minerai, cathodes

    # ================= BILAN =================
    def bilan_journalier(self, instance):

        prod, minerai, cathodes = self.kpi()

        self.popup("Bilan Journalier",
                   f"Production: {prod}\nMinerai: {minerai}\nCathodes: {cathodes}")

    # ================= FINANCE =================
    def rapport_financier(self, instance):

        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("SELECT COALESCE(SUM(revenus),0), COALESCE(SUM(depenses),0) FROM finance")
        revenus, depenses = cur.fetchone()

        conn.close()

        profit = revenus - depenses

        self.popup("Finance",
                   f"Revenus: {revenus}\nDépenses: {depenses}\nProfit: {profit}")

    # ================= POPUP =================
    def popup(self, title, text):

        box = BoxLayout(orientation="vertical", padding=10)
        box.add_widget(Label(text=text))

        Popup(title=title, content=box, size_hint=(0.8, 0.6)).open()

    # ================= EXCEL =================
    def export_excel(self, instance):

        file = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Usine"

        conn = self.get_conn()
        cur = conn.cursor()

        # Production
        cur.execute("SELECT date, quantite FROM production")
        ws.append(["PRODUCTION"])
        ws.append(["Date", "Quantité"])
        for r in cur.fetchall():
            ws.append(r)

        ws.append([])

        # Stock
        cur.execute("SELECT date, minerai, cathodes FROM stock")
        ws.append(["STOCK"])
        ws.append(["Date", "Minerai", "Cathodes"])
        for r in cur.fetchall():
            ws.append(r)

        conn.close()
        wb.save(file)

        self.popup("Excel", f"Fichier créé:\n{file}")

    # ================= PDF =================
    def export_pdf(self, instance):

        file = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        doc = SimpleDocTemplate(file)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("RAPPORT USINE CUIVRE", styles["Title"]))
        elements.append(Spacer(1, 12))

        prod, minerai, cathodes = self.kpi()

        text = f"""
Production: {prod}
Minerai: {minerai}
Cathodes: {cathodes}
"""

        elements.append(Paragraph(text, styles["Normal"]))

        doc.build(elements)

        self.popup("PDF", f"Fichier créé:\n{file}")