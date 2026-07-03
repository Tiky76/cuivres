from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

import sqlite3
import matplotlib.pyplot as plt


class Graph(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        self.title = Label(text="GRAPHIQUES USINE", font_size=24)
        self.layout.add_widget(self.title)

        # ================= BTN =================
        btn = Button(
            text="📊 Graph Production",
            size_hint=(1, 0.15)
        )
        btn.bind(on_press=self.generate_graph)
        self.layout.add_widget(btn)

        # ================= IMAGE =================
        self.img = Image()
        self.layout.add_widget(self.img)

        # ================= RETOUR =================
        back = Button(
            text="⬅ Retour",
            size_hint=(1, 0.15)
        )
        back.bind(on_press=self.go_back)
        self.layout.add_widget(back)

        self.add_widget(self.layout)

    # ================= RETOUR =================
    def go_back(self, instance):
        self.manager.current = "dashboard"

    # ================= GRAPH =================
    def generate_graph(self, instance):

        try:
            conn = sqlite3.connect("usine.db")
            cur = conn.cursor()

            # ✅ PRODUCTION (BONNE TABLE)
            cur.execute("""
                SELECT date, quantite
                FROM production
                ORDER BY id ASC
            """)

            data = cur.fetchall()
            conn.close()

            if not data:
                self.title.text = "Aucune donnée"
                return

            dates = [d[0] for d in data]
            values = [d[1] for d in data]

            plt.clf()
            plt.figure(figsize=(6, 4))
            plt.plot(dates, values, marker="o")

            plt.title("Production Usine")
            plt.xticks(rotation=45)
            plt.tight_layout()

            file = "graph.png"
            plt.savefig(file)
            plt.close()

            self.img.source = file
            self.img.reload()

            self.title.text = "Graphique généré ✔"

        except Exception as e:
            self.title.text = f"Erreur: {e}"