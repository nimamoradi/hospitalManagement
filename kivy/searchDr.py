import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from patient import get_ashghal_func

class SearchDr(Screen):
    # features = ["A", "B", "C"]
    features = []
    r3 = get_ashghal_func()
    for d in r3['doctors']:
        features.append(d['username'])
    def edit(self):
        pass

