from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
import pymysql
from pymysql.cursors import DictCursor
#import uuid
import hashlib
#import os
import random

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

        Label:
            text: ''
            pos_hint: {'center_x': .5, 'y': .3}
            color: 1, 0, 0, 1
            font_size: 24
            font_name: 'font.ttf'
            halign: 'center'

        TextInput:
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Логин'
            pos_hint: {'y': .6, 'center_x': .5}
            font_size: '20px'
            font_name: 'font.ttf'
            cursor_color: 29//255, 105//255, 246//255, 1
            cursor_blink: True

        TextInput:
            cursor_color: 29//255, 105//255, 246//255, 1
            cursor_blink: True
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
            pos_hint: {'y': -.1999}
            font_size: 18
            color: .1, .1, .1, 1
            font_name: 'font.ttf'

        Button:
            text: 'Зарегистрироваться!'
            size_hint: None, None
            size: 260, 50
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
            halign: 'center'

        TextInput:
            cursor_color: 29//255, 105//255, 246//255, 1
            id: 'reglogininp'
            multiline: False
            size_hint: .75, None
            size: 0, 40
            hint_text: 'Логин'
            pos_hint: {'y': .7, 'center_x': .5}
            font_size: '20px'
            font_name: 'font.ttf'

        TextInput:
            cursor_color: 29//255, 105//255, 246//255, 1
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
            cursor_color: 29//255, 105//255, 246//255, 1
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
            size: 235, 50
            pos_hint: {'y': .35, 'center_x': .5}     
            background_normal: ''
            background_color: 74/255, 118/255, 168/255, 1
            font_name: 'font.ttf'
            font_size: 20
            on_press: root.RegisterUser()

<ChatScreen>:
    ScrollView:
        do_scroll_y: True
        do_scroll_x: False
       # size: Window.width, Window.height

<ChatLine>:
    canvas.before:
        Color:
            rgba: .95, .95, .97, 1
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint: 1, None
    size: 0, 150
    anchor_x: 'left'
    Image:
        source: 'testavatar.jpg'
        size: 100, 100
        size_hint_y: None
        size_hint_x: None
        pos: 15, 0
        pos_hint: {'center_y': .5}
        allow_stretch: True
    Label:
        size_hint_y: None
        size_hint_x: None
        text_size: 700, 30
        pos: 430, 70
        text: 'Myname'
        font_name: 'font.ttf'
        font_size: 24
        color: 0, 0, 0, 1
        pos_hint: {'center_y': .75}

    Label:
        size_hint_y: None
        size_hint_x: None
        text_size: 700, 30
        text: 'Lorem ipsum ooooo'
        pos: 440, 20
        font_name: 'font.ttf'
        font_size: 18
        color: .4, .4, .4, 1
        pos_hint: {'center_y': .45}
""")

class AuthoriseScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthoriseScreen, self).__init__(**kwargs)

    def CheckUser(self):
        #здесь должна быть функция с SQL запросом по проверке пользователя
        errlabel = self.children[0].children[len(self.children[0].children) - 2]
        try:
            connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
        except pymysql.err.Error:
            conerrortext = ['Упс, что-то пошло не так.\nПроверьте подключение к интернету или зайдите позже.', 'Не удалось войти.\nПроверьте подключение к интернету.', 'Не получилось.\nПроверьте подключение к интернету.']
            errlabel.text = conerrortext[random.randint(0, 2)]
            errlabel.font_size = 16
            return
        else:
            authdatar = None
            with connection:
                cur = connection.cursor()
                query = ''
                try:
                    authdatar = open('authdata.pchat', 'r')
                except FileNotFoundError:
                    errlabel = self.children[0].children[len(self.children[0].children) - 2]
                    textInputValues = []
                    for i in self.children[0].children:
                        if type(i) == TextInput:
                            textInputValues.append(i.text)
                    textInputValues = list(reversed(textInputValues))
                    hashedPass = str(hash_password(textInputValues[1]))
                    query = "SELECT * FROM UserLoginData WHERE UserLoginData.login = '" + textInputValues[0] + "' and UserLoginData.pass = '" + hashedPass + "'"
                else:
                    filelines = []
                    for line in authdatar:
                        if line[len(line) - 1] == '\n':
                            line = line[0:-1]
                        filelines.append(line)
                    query = "SELECT * FROM UserLoginData WHERE UserLoginData.login = '" + filelines[0] + "' and UserLoginData.pass = '" + filelines[1] + "'"
                    authdatar.close()
                res = cur.execute(query)
            connection.close()
            if res == 0:
                errlabel.text = 'Неверно введен логин или пароль'
                return
            if not authdatar:
                authdata = open('authdata.pchat', 'w')
                authdata.write(textInputValues[0] + '\n')
                authdata.write(hashedPass)  
                authdata.close()
            self.manager.current = 'chatscreen'

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

        allowed_symbols = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!$%^&?*()[]{}_-=`~+/\\\'|"<>.,'

        for i in textInputValues[0]:
            if not(i in allowed_symbols):
                errLabel.text = 'Логин может состоять только из букв\nлатинского алфавита, цифр и символов\n!$%^&?*()[]{}_-=`~+/\\\'|"<>.,'
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
        connection = None
        try:
            connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
        except pymysql.err.Error:
            conerrortext = ['Упс, что-то пошло не так.\nПроверьте подключение к интернету или зайдите позже.', 'Не удалось создать пользователя.\nПроверьте подключение к интернету.', 'Не получилось.\nПроверьте подключение к интернету.']
            errLabel.text = conerrortext[random.randint(0, 2)]
            errLabel.font_size = 16
            return
        else:
            user_exists = False

            with connection:
                cur = connection.cursor()
                try:
                    res = cur.execute("SELECT * FROM UserLoginData")
                except pymysql.err.ProgrammingError:
                    print('The table UserLoginData doesnt exist')
                    req = cur.execute("CREATE TABLE `UserLoginData`(`id` INT NOT NULL AUTO_INCREMENT, `login` VARCHAR (80) NOT NULL, `pass` VARCHAR (256) NOT NULL, PRIMARY KEY (`id`))")
                    print(req)

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
            
            authdata = open('authdata.pchat', 'w')
            authdata.write(textInputValues[0] + '\n')
            authdata.write(hashed_password)
            authdata.close()

            connection.close()

        self.manager.current = 'chatscreen'

class ChatLine(FloatLayout):
    def __init__(self, **kwargs):
        super(ChatLine, self).__init__(**kwargs)

    def setUserData(self, **kwargs):
        keys = ['lastmessage', 'username', 'avatar']
        for key, value in kwargs.items():
            if key == 'lastmessage':
                if len(value) > 23:
                    value = value[0:22] + '...'
                self.children[0].text = value
            if key == 'username':
                self.children[1].text = value
            if key == 'avatar':
                self.children[2].source = value

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        gr = GridLayout(cols=1, spacing=10, size_hint_y=None)
        gr.bind(minimum_height=gr.setter('height'))
        for i in range(2):
            ch = ChatLine()
            ch.setUserData(username='Nickname ' + str(i), lastmessage='LastMessageфыфффффффффффффффффффффффффффффффффффффффффф ' + str(i), avatar='testavatar.jpg')
            gr.add_widget(ch)
        self.children[0].add_widget(gr)
        self.children[0].size_hint=(1, 1)

mainScreenManager = ScreenManager()
mainScreenManager.add_widget(AuthoriseScreen(name='auth'))
mainScreenManager.add_widget(RegisterScreen(name='register'))
mainScreenManager.add_widget(ChatScreen(name='chatscreen'))

class ChatApp(App):
    def build(self):
        return mainScreenManager

if __name__ == '__main__':
    authdatafile = None
    try:
        authdatafile = open('authdata.pchat', 'r')        
    except FileNotFoundError:
        mainScreenManager.current = 'auth'
    else:
        mainScreenManager.children[0].CheckUser()
    ChatApp().run()
