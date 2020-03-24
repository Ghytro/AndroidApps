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


def hash_password(_password):
    hash_object = hashlib.sha256(_password.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

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
            on_press: root.CheckUser()
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

class AuthoriseScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthoriseScreen, self).__init__(**kwargs)

    def CheckUser(self):
        #здесь должна быть функция с SQL запросом по проверке пользователя
        
        textInputValues = []
        for i in self.children[0].children:
            if type(i) == TextInput:
                textInputValues.append(i.text)
        textInputValues = list(reversed(textInputValues))

        hashedPass = str(hash_password(textInputValues[1]))

        connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
        with connection:
            cur = connection.cursor()
            query = "SELECT * FROM UserLoginData WHERE UserLoginData.login = '" + textInputValues[0] + "' and UserLoginData.pass = '" + hashedPass + "'"
            res = cur.execute(query)
        
        if res == 0:
            print('user doesnt exist')
        else:
            print('LOGIN OK')

        connection.close()

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

        if len(textInputValues[0]) == 0:
            errLabel.text = 'Логин не может быть пустым'
            errLabel.font_size = 18
            return

        prohibited_symbols = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!$%^&?*()[]{}_-=`~+/\\\'|"<>.,'

        for i in textInputValues[0]:
            if not(i in prohibited_symbols):
                errLabel.text = 'Логин может состоять только из букв\nлатинского алфавита и символов\n!$%^&?*()[]{}_-=`~+/\\\'|"<>.,'
                errLabel.font_size = 16
                return

        if textInputValues[1] != textInputValues[2]:
            errLabel.text = 'Введенные пароли не совпадают'
            errLabel.font_size = 20
            return

        if len(textInputValues[1]) < 6:
            errLabel.text = 'Пароль должен быть как минимум 6 символов!'
            errLabel.font_size = 16
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

        #если проверки пройдены создаем пользователя
        
        with connection:
            cur = connection.cursor()
            hashed_password = str(hash_password(textInputValues[1]))
            query = "INSERT INTO UserLoginData (login, pass) values('" + textInputValues[0] + "', '" + hashed_password + "')"
            cur.execute(query)

        connection.close()

mainScreenManager = ScreenManager()
mainScreenManager.add_widget(AuthoriseScreen(name='auth'))
mainScreenManager.add_widget(RegisterScreen(name='register'))

class ChatApp(App):
    def build(self):
        return mainScreenManager

print (hash_password('Hello world!'))

if __name__ == '__main__':
    ChatApp().run()
