
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
 
class Forget(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    email_text_input = ObjectProperty()
 
    def submit_forget(self):
        pass
 

 
class ForgetApp(App):
    def build(self):
        return Forget()
 
 
dbApp = ForgetApp()
 
dbApp.run()