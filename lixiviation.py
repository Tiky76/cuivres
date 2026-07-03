from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class Lixiviation(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="LIXIVIATION",
            font_size=24
        )

        self.minerai_traite = TextInput(
            hint_text="Minerai traité (T)",
            multiline=False
        )

        self.acide_utilise = TextInput(
            hint_text="Acide utilisé (kg)",
            multiline=False
        )

        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        layout.add_widget(titre)
        layout.add_widget(self.minerai_traite)
        layout.add_widget(self.acide_utilise)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            if not self.minerai_traite.text or not self.acide_utilise.text:
                print("❌ Champs vides")
                return

            minerai = float(self.minerai_traite.text)
            acide = float(self.acide_utilise.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= LIXIVIATION =================
            cur.execute("""
                INSERT INTO lixiviation(date, minerai_traite, acide_utilise)
                VALUES (?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                minerai,
                acide
            ))

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Lixiviation",
                "Ajout",
                f"Minerai={minerai} T | Acide={acide} kg"
            ))

            conn.commit()
            conn.close()

            # reset UI
            self.minerai_traite.text = ""
            self.acide_utilise.text = ""

            print("Lixiviation enregistrée ✔")

            # ================= KPI AUTO UPDATE =================
            if self.manager:
                try:
                    dashboard = self.manager.get_screen("dashboard")
                    if hasattr(dashboard, "load_kpi"):
                        dashboard.load_kpi()
                except Exception as e:
                    print("KPI refresh error:", e)

        except ValueError:
            print("❌ Valeur invalide")
        except Exception as e:
            print("Erreur :", e)