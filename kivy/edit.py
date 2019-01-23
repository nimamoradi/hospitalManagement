
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
 
class Edit(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    email_text_input = ObjectProperty()
 
    def edit(self):
        pass
 

 
class EditApp(App):
    def build(self):
        return Edit()
 
 
dbApp = EditApp()
 
dbApp.run()