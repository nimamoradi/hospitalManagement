import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty

import patient
import edit

class StudentDBApp(App):
 
    # Connects the value in the TextInput widget to these
    # fields
    user_name_log_text_input = ObjectProperty()
    password_log_text_input = ObjectProperty()
    student_list = ObjectProperty()
    def build(self):
        manager = ScreenManager()
        manager.add_widget(StudentDB(name='studentdb'))
        manager.add_widget(patient.Patient(name='patient'))
        manager.add_widget(edit.Edit(name='edit'))
        return manager

class StudentDB(Screen):
    def submit_student(self):
        login = {}
        login['username'] = self.user_name_log_text_input.text
        login['password'] = self.password_log_text_input.text
        print(login)
        r = requests.post(url='http://localhost:2228/login', json=login)
        #print(r.json()['api_key'])
        # print(r.json())
        
        app = App.get_running_app()



        if 'User' in r.json().keys():
            if r.json()['User']['role'] == 'patient':
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'patient'

        app.config.read(app.get_application_config())
        app.config.write()

if __name__ == '__main__':
    StudentDBApp().run()

