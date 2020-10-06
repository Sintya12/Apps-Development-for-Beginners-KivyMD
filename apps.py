import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class KivyApp(App):
    def build(self):
        self.title = "Login Screen"
        Window.size = (400,200)
        layout = GridLayout(cols=2, rows=2, spacing=18, row_default_height=30)

        emailinput = TextInput()
        passwordinput = TextInput(password=True)

        username = Label(text='Username')
        password = Label(text='Password')

        layout.add_widget(username)
        layout.add_widget(emailinput)
        layout.add_widget(password)
        layout.add_widget(passwordinput)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(layout)

        btn = Button(text='Login')
        main_layout.add_widget(btn)

        return main_layout

if __name__  == '__main__' :
    KivyApp().run()
