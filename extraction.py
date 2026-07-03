from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class Extraction(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="EXTRACTION",
            font_size=24
        )

        self.tonnage = TextInput(
            hint_text="Tonnage extrait (T)",
            multiline=False
        )

        self.teneur = TextInput(
            hint_text="Teneur (%)",
            multiline=False
        )

        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        layout.add_widget(titre)
        layout.add_widget(self.tonnage)
        layout.add_widget(self.teneur)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            if not self.tonnage.text or not self.teneur.text:
                print("❌ Champs vides")
                return

            tonnage = float(self.tonnage.text)
            teneur = float(self.teneur.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= EXTRACTION =================
            cur.execute("""
                INSERT INTO extraction(date, tonnage, teneur)
                VALUES (?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                tonnage,
                teneur
            ))

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Extraction",
                "Ajout",
                f"Tonnage={tonnage} T | Teneur={teneur} %"
            ))

            conn.commit()
            conn.close()

            # reset UI
            self.tonnage.text = ""
            self.teneur.text = ""

            print("Extraction enregistrée ✔")

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