import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty

import patient


class Edit(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    email_text_input = ObjectProperty()
 
    def edit(self):
        pass
 

 
class EditApp(App):

    user_name_log_text_input = ObjectProperty()
    password_log_text_input = ObjectProperty()
    student_list = ObjectProperty()
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Edit(name='studentdb'))
        manager.add_widget(Patient(name='patient'))

        return manager
