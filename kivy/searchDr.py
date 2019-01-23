
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
 

class SearchDrListButton(ListItemButton):
    pass
 
 
class SearchDr(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    search_list = ObjectProperty()
 
    def edit(self):
        pass

 
class SearchDrApp(App):
    def build(self):
        return SearchDr()
 
 
dbApp = SearchDrApp()
 
dbApp.run()