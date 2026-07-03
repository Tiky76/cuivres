from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class Stock(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="STOCK",
            font_size=24
        )

        self.minerai = TextInput(
            hint_text="Minerai (T)",
            multiline=False
        )

        self.cathodes = TextInput(
            hint_text="Cathodes (T)",
            multiline=False
        )

        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        layout.add_widget(titre)
        layout.add_widget(self.minerai)
        layout.add_widget(self.cathodes)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            # ✔ vérification champs vides
            if not self.minerai.text or not self.cathodes.text:
                print("❌ Champs vides")
                return

            minerai = float(self.minerai.text)
            cathodes = float(self.cathodes.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= STOCK =================
            cur.execute("""
                INSERT INTO stock(date, minerai, cathodes)
                VALUES (?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                minerai,
                cathodes
            ))

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Stock",
                "Ajout",
                f"Minerai={minerai} T | Cathodes={cathodes} T"
            ))

            conn.commit()
            conn.close()

            # reset UI
            self.minerai.text = ""
            self.cathodes.text = ""

            print("Stock enregistré ✔")

            # ================= REFRESH KPI =================
            if self.manager:
                dashboard = self.manager.get_screen("dashboard")
                if hasattr(dashboard, "load_kpi"):
                    dashboard.load_kpi()

        except ValueError:
            print("❌ Valeur invalide (doit être un nombre)")
        except Exception as e:
            print("Erreur :", e)