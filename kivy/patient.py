import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
import searchDr

 
class Patient(Screen):
    def edit(self):
        app = App.get_running_app()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'edit'
        app.config.read(app.get_application_config())
        app.config.write()
        def inbox(self):
            app = App.get_running_app()
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'inbox'
            app.config.read(app.get_application_config())
            app.config.write()
        def sent(self):
            app = App.get_running_app()
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'sent'
            app.config.read(app.get_application_config())
            app.config.write()
    def search(self):
        app = App.get_running_app()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'search'
        app.config.read(app.get_application_config())
        app.config.write()
