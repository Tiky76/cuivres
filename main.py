from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from dashboard import Dashboard
from production import Production
from stock import Stock
from finance import Finance
from extraction import Extraction
from broyage import Broyage
from lixiviation import Lixiviation
from sx import SX
from ew import EW
from historique import Historique
from export import Export
from graph import Graph


class UsineApp(App):

    def build(self):

        sm = ScreenManager()

        screens = [
            Dashboard(name="dashboard"),
            Production(name="production"),
            Stock(name="stock"),
            Finance(name="finance"),
            Extraction(name="extraction"),
            Broyage(name="broyage"),
            Lixiviation(name="lixiviation"),
            SX(name="sx"),
            EW(name="ew"),
            Historique(name="historique"),
            Export(name="export"),
            Graph(name="graph")
        ]

        for s in screens:
            sm.add_widget(s)

        print("Screens chargés :", sm.screen_names)

        return sm


UsineApp().run()