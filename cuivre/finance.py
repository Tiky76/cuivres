from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class Finance(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="FINANCE",
            font_size=24
        )

        self.revenus = TextInput(
            hint_text="Revenus ($)",
            multiline=False
        )

        self.depenses = TextInput(
            hint_text="Dépenses ($)",
            multiline=False
        )

        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        layout.add_widget(titre)
        layout.add_widget(self.revenus)
        layout.add_widget(self.depenses)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            if not self.revenus.text or not self.depenses.text:
                print("❌ Champs vides")
                return

            revenus = float(self.revenus.text)
            depenses = float(self.depenses.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= FINANCE =================
            cur.execute("""
                INSERT INTO finance(date, revenus, depenses)
                VALUES (?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                revenus,
                depenses
            ))

            profit = revenus - depenses

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Finance",
                "Ajout",
                f"Revenus={revenus} | Dépenses={depenses} | Profit={profit}"
            ))

            conn.commit()
            conn.close()

            # reset inputs
            self.revenus.text = ""
            self.depenses.text = ""

            print("Finance enregistrée ✔")

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