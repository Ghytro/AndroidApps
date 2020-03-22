from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import pymysql



#setting screen config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', 720 // 2)
Config.set('graphics', 'height', 1280 // 2)


#connecting to database
from pymysql.cursors import DictCursor
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123',
    db='iata',
    charset='utf8mb4',
    cursorclass=DictCursor
)

class AuthoriseScreen(Screen):
    def __init__(self, **kw):
        super(AuthoriseScreen, self).__init__(**kw)

        fl              = FloatLayout(size_hint=[1, 1])
        
        welcomeLb       = Label(text="Чат-нейм", pos_hint={"y": .4}, font_size=24)

        loginLabel      = Label(text="Логин:", pos_hint={"y":.175, "x":-.175}, font_size=18)
        loginInp        = TextInput(size_hint=[0.5, 0.05], pos_hint={"y": .60, "x": .25}, multiline=False)

        passLabel       = Label(text="Пароль:", pos_hint={"y": .025, "x":-.16}, font_size=18)
        passInp         = TextInput(size_hint=[0.5, 0.05], pos_hint={"y": .45, "x": .25}, multiline=False, password=True, password_mask="•")

        logInButton     = Button(text="Войти", size_hint=[1/3, .07], pos_hint={"y": .3, "x": 1 - 2/3}, font_size=24)

        fl.add_widget(welcomeLb)
        fl.add_widget(loginLabel)
        fl.add_widget(loginInp)
        fl.add_widget(passLabel)
        fl.add_widget(passInp)
        fl.add_widget(logInButton)
        self.add_widget(fl)

    def CheckUser(self, instance):


mainScreenManager = ScreenManager()
mainScreenManager.add_widget(AuthoriseScreen(name="auth"))

class KivyApp(App):
    def build(self):
        return mainScreenManager

if __name__ == '__main__':
    KivyApp().run()

connection.close()
