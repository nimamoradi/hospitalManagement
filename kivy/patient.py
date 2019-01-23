
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
 

class PatientButton(ListItemButton):
    pass
 
 
class Patient(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    search_text_input = ObjectProperty()
    search_list = ObjectProperty()
 
    def edit(self):
        pass

 
class PatientApp(App):
    def build(self):
        return Patient()
 
 
dbApp = PatientApp()
 
dbApp.run()