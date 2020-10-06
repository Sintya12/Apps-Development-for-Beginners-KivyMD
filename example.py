import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons

from kivy.properties import ObjectProperty, StringProperty

import json
import requests
import uuid
from kivy.storage.jsonstore import JsonStore

Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        GridLayout:
            rows: 4
            cols: 1
            padding: 10
            spacing: 10
            row_default_height: 30
            MDTextField:
                hint_text: 'Email'
                id: usernamevalue
            MDTextField:
                hint_text: 'Password'
                id: passwordvalue
                password: True
            MDRectangleFlatButton:
                text: 'login'
                on_press: root.login_button_action()


<FailedLoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        GridLayout:
            rows: 2
            cols: 1
            padding: 10
            spacing: 10
            row_default_height: 30
        MDLabel:
            text:'Failed Login'
        MDRectangleFlatButton:
            text: 'Back'
            on_press: root.manager.current = 'login'

<AddTaskScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        GridLayout:
            rows: 3
            cols: 1
            padding: 10
            spacing: 10
            row_default_height: 30
            MDTextField:
                hint_text: 'Task Name'
                id: taskname
            MDRectangleFlatButton:
                text: 'Add Task'
                on_press: root.add_task()

<TaskScreen>:
    ScrollView:
        MDList:
            id: taskscreen
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        x: root.width - self.width - dp(10)
        y: dp(10)
        on_press: root.manager.current = 'addtaskscreen'

<ListItemWithCheckbox>:
    IconLeftWidget:
        icon: root.icon
    RightCheckbox:


""")
db = JsonStore("tasks.json")

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty("android")
    pass

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class LoginScreen(Screen):
    def build(self):
        pass

    def login_button_action(self):
        url = "https://reqres.in/api/login"

        data = json.dumps({"email": "eve.holt@reqres.in", "password": "cityslicka"})

        response = requests.post(url, data=data, headers={'Content-Type':'application/json'})

        userdata = json.loads(response.text)

        if userdata.get("token"):
            self.manager.current = 'taskscreen'
        else:
            self.manager.current = 'failedlogin'

class FailedLoginScreen(Screen):
        pass



class AddTaskScreen(Screen):
    def build(self):
        pass
    def add_task(self):
        db.put(uuid.uuid1().int, name=self.ids.taskname.text)
        self.manager.current = 'taskscreen'

class TaskScreen(Screen):
    def on_pre_enter(self):
        self.ids.taskscreen.clear_widgets()
        for key,item in db.find():
            self.ids.taskscreen.add_widget(
                ListItemWithCheckbox(text=f"{item.get('name')}",icon='pen')
            )


class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FailedLoginScreen(name='failedlogin'))
        sm.add_widget(AddTaskScreen(name='addtaskscreen'))
        sm.add_widget(TaskScreen(name='taskscreen'))
        return sm


if __name__ == '__main__':
    MainApp().run()
