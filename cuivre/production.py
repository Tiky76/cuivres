from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class Production(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # ================= TITRE =================
        titre = Label(
            text="PRODUCTION",
            font_size=24
        )

        # ================= INPUT =================
        self.quantite = TextInput(
            hint_text="Quantité produite (T)",
            multiline=False
        )

        # ================= BOUTON =================
        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        # ================= RETOUR =================
        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        # ================= AJOUT UI =================
        layout.add_widget(titre)
        layout.add_widget(self.quantite)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTRER =================
    def enregistrer(self, instance):

        try:
            quantite = float(self.quantite.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO production(date, quantite)
                VALUES (?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                quantite
            ))

            cur.execute("""
                INSERT INTO historique(
                    date_action,
                    module,
                    operation,
                    valeur
                )
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Production",
                "Ajout",
                f"{quantite} T"
            ))

            conn.commit()
            conn.close()

            self.quantite.text = ""

            print("Production enregistrée ✔")

            # 🔥 AUTO REFRESH DASHBOARD KPI
            if self.manager:
                try:
                    self.manager.get_screen("dashboard").load_kpi()
                except Exception as e:
                    print("Refresh KPI erreur:", e)

        except Exception as e:
            print("Erreur :", e)