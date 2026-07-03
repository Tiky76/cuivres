from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3
from datetime import datetime


class SX(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # ================= TITRE =================
        titre = Label(
            text="EXTRACTION SOLVANT (SX)",
            font_size=24
        )

        # ================= CHAMPS =================
        self.solution_entree = TextInput(
            hint_text="Solution entrée (L)",
            multiline=False
        )

        self.cuivre_extrait = TextInput(
            hint_text="Cuivre extrait (T)",
            multiline=False
        )

        # ================= BOUTONS =================
        btn = Button(text="Enregistrer")
        btn.bind(on_press=self.enregistrer)

        back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        back.bind(on_press=self.go_back)

        # ================= UI =================
        layout.add_widget(titre)
        layout.add_widget(self.solution_entree)
        layout.add_widget(self.cuivre_extrait)
        layout.add_widget(btn)
        layout.add_widget(back)

        self.add_widget(layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= ENREGISTREMENT =================
    def enregistrer(self, instance):

        try:
            if not self.solution_entree.text or not self.cuivre_extrait.text:
                print("❌ Champs vides")
                return

            solution = float(self.solution_entree.text)
            cuivre = float(self.cuivre_extrait.text)

            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ================= SX =================
            cur.execute("""
                INSERT INTO sx(date, solution_entree, cuivre_extrait)
                VALUES (?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                solution,
                cuivre
            ))

            # ================= HISTORIQUE =================
            cur.execute("""
                INSERT INTO historique(date_action, module, operation, valeur)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "SX",
                "Ajout",
                f"Solution={solution} L | Cuivre={cuivre} T"
            ))

            conn.commit()
            conn.close()

            # reset UI
            self.solution_entree.text = ""
            self.cuivre_extrait.text = ""

            print("SX enregistré ✔")

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
            print("Erreur SX :", e)