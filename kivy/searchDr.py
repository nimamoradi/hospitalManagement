import requests
import patient
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
class SearchDr(Screen):
    # features = ["A", "B", "C"]
    features = []
    # conf = patient.Config()
    # r3 = conf.myValue()
    # for d in r3['doctors']:
    #     features.append(d['username'])
    def edit(self):
        pass

