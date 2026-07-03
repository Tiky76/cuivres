from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class EW(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # ================= TITRE =================
        titre = Label(
            text="ÉLECTROLYSE (EW)",
            font_size=24
        )

        # ================= CHAMPS =================
        self.cathodes_produites = TextInput(
            hint_text="Cathodes produites (T)",
            multiline=False
        )

        # ================= BOUTONS =================
        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        # ================= UI =================
        layout.add_widget(titre)
        layout.add_widget(self.cathodes_produites)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            if not self.cathodes_produites.text:
                print("❌ Champ vide")
                return

            cathodes = float(self.cathodes_produites.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= EW =================
            cur.execute("""
                INSERT INTO ew(date, cathodes_produites)
                VALUES (?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                cathodes
            ))

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "EW",
                "Ajout",
                f"Cathodes={cathodes} T"
            ))

            conn.commit()
            conn.close()

            # reset UI
            self.cathodes_produites.text = ""

            print("EW enregistré ✔")

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
            print("Erreur EW :", e)