import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
import searchDr


r = {}
def get_ashghal_func():
    return r

def set_ashghal_func(r2):
    r = r2

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
        login = {}
        login['username'] = self.search_text_input.text
        print("searrcchhhh issss %s"%login['username'])
        
        set_ashghal_func(requests.post(url='http://localhost:2228/search_doctor', json=login))
        #print(r.json()['api_key'])

        app = App.get_running_app()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'search'
        app.config.read(app.get_application_config())
        app.config.write()

