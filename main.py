from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import pymysql
from pymysql.cursors import DictCursor
import uuid
import hashlib
import xml.dom.minidom

def xml_parse(fileName):
    doc = xml.dom.minidom.parse(fileName)

#setting screen config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', 9*50)
Config.set('graphics', 'height', 16*50)

#uploading kv file
Builder.load_string("""

<AuthoriseScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: .95, .95, .97, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'Welcome to the chat!'
            pos_hint: {'y': .4}
            font_size: 24
            color: .1, .1, .1, 1
            font_name: 'font.ttf'

        TextInput:
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Логин'
            pos_hint: {'y': .6, 'center_x': .5}
            font_size: '20px'
            font_name: 'font.ttf'

        TextInput:
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Пароль'
            pos_hint: {'y': .5, 'center_x': .5}
            password: True
            password_mask: '•'
            font_size: '20px'
            font_name: 'font.ttf'

        Button:
            text: 'Войти'
            size_hint: None, None
            size: 150, 50
            pos_hint: {'y': .35, 'center_x': .5}
            font_size: 28
            on_press: root.Pr()
            background_normal: ''
            background_color: 74/255, 118/255, 168/255, 1
            font_name: 'font.ttf'

        Label:
            text: 'Нет аккаунта?'
            pos_hint: {'y': -.22}
            font_size: 18
            color: .1, .1, .1, 1
            font_name: 'font.ttf'

        Button:
            text: 'Зарегистрироваться!'
            size_hint: None, None
            size: 220, 40
            pos_hint: {'y': .2, 'center_x': .5}
            font_size: 22
            on_press: root.manager.current = 'register'
            background_normal: ''
            background_color: 74/255, 118/255, 168/255, 1
            font_name: 'font.ttf'

<RegisterScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: .95, .95, .97, 1                
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'Создать аккаунт'
            pos_hint: {'center_x': .5, 'y': .4}
            font_size: 24
            color: .1, .1, .1, 1
            font_name: 'font.ttf'

        Label:
            id: 'errorlabel'
            text: ''
            pos_hint: {'y': .33, 'center_x': .5}
            color: 1, 0, 0, 1
            font_name: 'font.ttf'
            font_size: 22

        TextInput:
            id: 'reglogininp'
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Логин'
            pos_hint: {'y': .7, 'center_x': .5}
            font_size: '20px'
            font_name: 'font.ttf'

        TextInput:
            id: 'regpassinp'
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Пароль'
            pos_hint: {'y': .6, 'center_x': .5}
            password: True
            password_mask: '•'
            font_size: '20px'
            font_name: 'font.ttf'

        TextInput:
            id: 'regpassconfirm'
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Повторите пароль'
            pos_hint: {'y': .5, 'center_x': .5}
            password: True
            password_mask: '•'
            font_size: '20px'
            font_name: 'font.ttf'

        Button:
            text: 'Зарегистрироваться!'
            size_hint: None, None
            size: 220, 50
            pos_hint: {'y': .35, 'center_x': .5}     
            background_normal: ''
            background_color: 74/255, 118/255, 168/255, 1
            font_name: 'font.ttf'
            font_size: 20
            on_press: root.RegisterUser()
""")

#connecting to database

def CheckUser(self, instance):
    connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
    with connection:
        cur = connection.cursor()
        cur.execute("")

    connection.close()


class AuthoriseScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthoriseScreen, self).__init__(**kwargs)

    def Pr(self):
        #здесь должна быть функция с SQL запросом по проверке пользователя
        print(1)
        

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

    def RegisterUser(self):

        textInputValues = []
        for i in self.children[0].children:
            if type(i) == TextInput:
                textInputValues.append(i.text)
        textInputValues = list(reversed(textInputValues))

        
        #проверочки:
        ########################################################################
        errLabel = self.children[0].children[len(self.children[0].children) - 2]

        if textInputValues[1] != textInputValues[2]:
            errLabel.text = 'Введенные пароли не совпадают'
            return

        if len(textInputValues[1]) < 6:
            errLabel.text = 'Пароль должен быть как минимум 6 символов!'
            return

        connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
        exists = 0
        with connection:
            cur = connection.cursor()
            exists = cur.execute("SELECT * FROM UserLoginData WHERE UserLoginData.login='" + textInputValues[0] + "'")
            
        if exists:
            errLabel.text = 'Пользователь с таким логином существует.'
            connection.close()
            return

        #если проверки пройдены подключаем
        
        with connection:
            cur = connection.cursor()
            request = "INSERT INTO UserLoginData (login, pass) values('" + textInputValues[0] + "', '" + textInputValues[1] + "')"
            cur.execute(request)

        connection.close()

mainScreenManager = ScreenManager()
mainScreenManager.add_widget(AuthoriseScreen(name='auth'))
mainScreenManager.add_widget(RegisterScreen(name='register'))

class ChatApp(App):
    def build(self):
        return mainScreenManager

if __name__ == '__main__':
    ChatApp().run()
