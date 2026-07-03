from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import sqlite3


class Historique(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # ================= TITRE =================
        titre = Label(
            text="HISTORIQUE",
            font_size=24,
            size_hint=(1, 0.1)
        )

        # ================= SCROLL =================
        self.scroll = ScrollView(size_hint=(1, 0.8))

        self.content = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5
        )
        self.content.bind(minimum_height=self.content.setter("height"))

        self.scroll.add_widget(self.content)

        # ================= BOUTONS =================
        btn_refresh = Button(text="🔄 Actualiser", size_hint=(1, 0.1))
        btn_refresh.bind(on_press=self.load_data)

        btn_back = Button(text="⬅ Retour", size_hint=(1, 0.1))
        btn_back.bind(on_press=self.go_back)

        # ================= UI =================
        self.layout.add_widget(titre)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(btn_refresh)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

        # auto load
        self.load_data()

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= CHARGER =================
    def load_data(self, instance=None):

        self.content.clear_widgets()

        try:
            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            cur.execute("""
                SELECT date_action, module, operation, valeur
                FROM historique
                ORDER BY id DESC
                LIMIT 50
            """)

            rows = cur.fetchall()
            conn.close()

            if not rows:
                self.content.add_widget(
                    Label(
                        text="Aucune donnée",
                        size_hint_y=None,
                        height=40
                    )
                )
                return

            for r in rows:

                date, module, operation, valeur = r

                txt = f"[{date}]  {module} | {operation}\n{valeur}"

                self.content.add_widget(
                    Label(
                        text=txt,
                        size_hint_y=None,
                        height=60
                    )
                )

        except Exception as e:
            self.content.add_widget(
                Label(
                    text=f"Erreur: {e}",
                    size_hint_y=None,
                    height=40
                )
            )