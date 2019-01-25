import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty

import edit

 
class Patient(Screen):
    def edit(self):
        #print("helooo")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'edit'

    def vist(self):
        pass


class PatientApp(App):
    search_text_input = ObjectProperty()
    search_list = ObjectProperty()
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Patient(name='patient'))
        manager.add_widget(edit.Edit(name='edit'))
        return manager