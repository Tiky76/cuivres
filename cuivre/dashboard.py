from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import sqlite3


class Dashboard(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root = BoxLayout(orientation="vertical")

        # ================= TOP BAR =================
        top = BoxLayout(size_hint=(1, 0.1))

        menu_btn = Button(text="☰ MENU", size_hint=(0.25, 1))
        menu_btn.bind(on_press=self.open_menu)

        title = Label(text="TABLEAU DE BORD USINE CUIVRE")

        top.add_widget(menu_btn)
        top.add_widget(title)

        self.root.add_widget(top)

        # ================= KPI GRID =================
        self.kpis = GridLayout(cols=2, spacing=10, padding=10)

        self.kpi_prod = Label(text="Production\n0 T")
        self.kpi_stock = Label(text="Stock\n0 T")
        self.kpi_finance = Label(text="Finance\n0 $")
        self.kpi_acide = Label(text="Acide\n0 kg")
        self.kpi_cathodes = Label(text="Cathodes\n0 T")
        self.kpi_rendement = Label(text="Rendement\n0 %")
        self.kpi_teneur = Label(text="Teneur\n0 %")
        self.kpi_profit = Label(text="Profit\n0 $")

        self.kpis.add_widget(self.kpi_prod)
        self.kpis.add_widget(self.kpi_stock)
        self.kpis.add_widget(self.kpi_finance)
        self.kpis.add_widget(self.kpi_acide)
        self.kpis.add_widget(self.kpi_cathodes)
        self.kpis.add_widget(self.kpi_rendement)
        self.kpis.add_widget(self.kpi_teneur)
        self.kpis.add_widget(self.kpi_profit)

        self.root.add_widget(self.kpis)

        # ================= BUTTON REFRESH =================
        refresh = Button(text="🔄 Actualiser KPI", size_hint=(1, 0.1))
        refresh.bind(on_press=lambda x: self.load_kpi())
        self.root.add_widget(refresh)

        self.add_widget(self.root)

        # auto load
        self.load_kpi()

    # ================= MENU =================
    def open_menu(self, instance):

        layout = BoxLayout(orientation="vertical", spacing=5)

        screens = [
            "dashboard",
            "production",
            "stock",
            "finance",
            "extraction",
            "broyage",
            "lixiviation",
            "sx",
            "ew",
            "historique",
            "export",
            "graph"
        ]

        for s in screens:
            btn = Button(text=s.upper(), size_hint_y=None, height=45)
            btn.bind(on_press=lambda x, name=s: self.go(name))
            layout.add_widget(btn)

        popup = Popup(title="MENU USINE", content=layout, size_hint=(0.8, 0.9))

        close = Button(text="FERMER", size_hint_y=None, height=50)
        close.bind(on_press=popup.dismiss)
        layout.add_widget(close)

        popup.open()

    # ================= NAVIGATION =================
    def go(self, screen_name):
        if screen_name in self.manager.screen_names:
            self.manager.current = screen_name
        else:
            print("❌ Screen introuvable:", screen_name)

    # ================= KPI =================
    def load_kpi(self):

        try:
            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= PRODUCTION =================
            cur.execute("SELECT COALESCE(SUM(quantite),0) FROM production")
            prod = cur.fetchone()[0]

            # ================= STOCK =================
            cur.execute("""
                SELECT COALESCE(SUM(minerai),0),
                       COALESCE(SUM(cathodes),0)
                FROM stock
            """)
            minerai_stock, cathodes_stock = cur.fetchone()

            # ================= FINANCE =================
            cur.execute("""
                SELECT COALESCE(SUM(revenus),0),
                       COALESCE(SUM(depenses),0)
                FROM finance
            """)
            revenus, depenses = cur.fetchone()
            profit = revenus - depenses

            # ================= EXTRACTION =================
            cur.execute("""
                SELECT COALESCE(SUM(tonnage),0),
                       COALESCE(AVG(teneur),0)
                FROM extraction
            """)
            prod_ext, teneur = cur.fetchone()

            # ================= LIXIVIATION =================
            cur.execute("""
                SELECT COALESCE(SUM(acide_utilise),0)
                FROM lixiviation
            """)
            acide = cur.fetchone()[0]

            # ================= EW =================
            cur.execute("""
                SELECT COALESCE(SUM(cathodes_produites),0)
                FROM ew
            """)
            cathodes = cur.fetchone()[0]

            conn.close()

            # ================= CALCUL =================
            rendement = (cathodes / prod if prod > 0 else 0) * 100

            # ================= UPDATE UI =================
            self.kpi_prod.text = f"Production\n{prod:.2f} T"
            self.kpi_stock.text = f"Stock\nM:{minerai_stock:.2f} C:{cathodes_stock:.2f}"
            self.kpi_finance.text = f"Profit\n{profit:.2f} $"
            self.kpi_acide.text = f"Acide\n{acide:.2f} kg"
            self.kpi_cathodes.text = f"Cathodes\n{cathodes:.2f} T"
            self.kpi_rendement.text = f"Rendement\n{rendement:.2f} %"
            self.kpi_teneur.text = f"Teneur\n{teneur:.2f} %"

            print("KPI mis à jour ✔")

        except Exception as e:
            print("❌ KPI ERROR:", e)