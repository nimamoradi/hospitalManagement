
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
 

class StudentListButton(ListItemButton):
    pass
 
 
class StudentDB(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    user_name_text_input = ObjectProperty()
    password_text_input = ObjectProperty()
    student_list = ObjectProperty()
 
    def submit_student(self):
 
        # Get the student name from the TextInputs
        student_name = self.usert_name_text_input.text + " " + self.password_text_input.text

 
class StudentDBApp(App):
    def build(self):
        return StudentDB()
 
 
dbApp = StudentDBApp()
 
dbApp.run()