from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class Broyage(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="BROYAGE",
            font_size=24
        )

        self.entree = TextInput(
            hint_text="Entrée (T)",
            multiline=False
        )

        self.sortie = TextInput(
            hint_text="Sortie (T)",
            multiline=False
        )

        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        layout.add_widget(titre)
        layout.add_widget(self.entree)
        layout.add_widget(self.sortie)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            # validation champs
            if not self.entree.text or not self.sortie.text:
                print("❌ Champs vides")
                return

            entree = float(self.entree.text)
            sortie = float(self.sortie.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= BROYAGE =================
            cur.execute("""
                INSERT INTO broyage(date, entree, sortie)
                VALUES (?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                entree,
                sortie
            ))

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Broyage",
                "Ajout",
                f"Entrée={entree} T | Sortie={sortie} T"
            ))

            conn.commit()
            conn.close()

            # reset UI
            self.entree.text = ""
            self.sortie.text = ""

            print("Broyage enregistré ✔")

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