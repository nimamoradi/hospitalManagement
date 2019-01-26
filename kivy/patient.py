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
        app = App.get_running_app()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'edit'
        app.config.read(app.get_application_config())
        app.config.write()
    def inbox(self):
        pass
    def sent(self):
        pass
    def search(self):
        pass
