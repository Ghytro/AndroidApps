from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.list import IconLeftWidget
import pymysql
from pymysql.cursors import DictCursor
import random
import hashlib

def hash_password(_password):
    hash_object = hashlib.sha256(_password.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def getLoggedInUserLogin():
    f = open("authdata.pchat", "r")
    login = f.readline()[0:-1]
    f.close()
    return login

class Chatline(object):
    def __init__(self, username, last_message, cached_avatar):
        self.username = username
        self.last_message = last_message
        self.cached_avatar = cached_avatar

class ChatListScreen(Screen):
    def addLine(self, chatline):
        line = TwoLineIconListItem(text=chatline.username, secondary_text=chatline.last_message)
        line.add_widget(IconLeftWidget(icon=chatline.cached_avatar))
        self.children[0].children[0].children[0].add_widget(line)

class ChatCreationScreen(Screen):
    pass

class PieChatRootWidget(BoxLayout):
    openedScreens = []
    def __init__(self, **kwargs):
        super(PieChatRootWidget, self).__init__(**kwargs)
        authdatafile = None
        try:
            authdatafile = open('authdata.pchat', 'r')        
        except FileNotFoundError:
            self.changeScreen('auth_screen')
        else:
            lines = []
            for line in authdatafile:
                lines.append(line)
            childr_len = len(self.children[0].children)
            errlabel = self.children[0].children[childr_len - 1].ids.errlabel_auth
            self.authUser(lines[0], lines[1], errlabel)
        

    def openChatCreationScreen(self):
        print("opened")

    def changeScreen(self, screen_name):
        self.ids.main_screen_manager.current = screen_name
        self.openedScreens.append(screen_name)

    def gotoPrevScreen(self):
        if len(self.openedScreens) > 1:
            self.openedScreens.pop()
            self.ids.main_screen_manager.current = self.openedScreens[len(self.openedScreens) - 1]
            return True
        return False

    def createUser(self, login, password, confirm_password, errLabel):
        textInputValues = [login, password, confirm_password]

        if len(textInputValues[0]) == 0:
            errLabel.text = "Login can't be empty"
            errLabel.font_size = 18
            return

        if len(textInputValues[0]) > 20:
            errLabel.text = "Login is too long.\nThink of another one"
            errLabel.font_size = 18
            return

        allowed_symbols = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!$%^&?*()[]{}_-=`~+/\\\'|"<>.,'

        for i in textInputValues[0]:
            if not(i in allowed_symbols):
                errLabel.text = "Login can only consist of\nEnglish letters, numerals and symbols\n!$%^&?*()[]{}_-=`~+/\\\'|\"<>.,"
                errLabel.font_size = 16
                return

        if textInputValues[1] != textInputValues[2]:
            errLabel.text = "Passwords don't match"
            errLabel.font_size = 20
            return

        if len(textInputValues[1]) < 6:
            errLabel.text = 'Password should be at least 6 symbols'
            errLabel.font_size = 16
            return
        connection = None
        try:
            connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
        except pymysql.err.Error:
            conerrortext = ['Oops... Something went wrong.\nCheck your internet connection.', "Impossible to create a user.\nCheck your internet connection", "An error has occured.\nCheck your internet connection."]
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
                errLabel.text = 'A user with that login already exists.\nThink of another one'
                errLabel.font_size = 18
                connection.close()
                return

            #если проверки пройдены создаем пользователя
            
            with connection:
                cur = connection.cursor()
                hashed_password = str(hash_password(textInputValues[1]))
                query = "INSERT INTO UserLoginData (login, pass) values('" + textInputValues[0] + "', '" + hashed_password + "')"
                cur.execute(query)
                cur.execute("SELECT MAX(`id`) FROM `UserLoginData`")
                rows = cur.fetchall()
                user_id = rows[0][0]
                cur.execute("CREATE TABLE `MainScreen" + str(user_id) + "`(`chat_id` INT NOT NULL, PRIMARY KEY (`chat_id`))")
            
            authdata = open('authdata.pchat', 'w')
            authdata.write(textInputValues[0] + '\n')
            authdata.write(hashed_password)
            authdata.close()

            connection.close()

    def authUser(self, login, password, errlabel):
        try:
            connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
        except pymysql.err.Error:
            conerrortext = ['Oops... Something went wrong.\nCheck your internet connection.', "Impossible to log in.\nCheck your internet connection", "An error has occured.\nCheck your internet connection."]
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
                    textInputValues = [login, password]
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
            if not res:
                errlabel.text = 'Incorrect login or password'
                errlabel.font_size = 16
                connection.close()
                return
            if not authdatar:
                authdata = open('authdata.pchat', 'w')
                authdata.write(textInputValues[0] + '\n')
                authdata.write(hashedPass)  
                authdata.close()
            print('Logged-in')
            self.openedScreens.clear()
            self.changeScreen('chat_list_screen')
            with connection:
                authdatar = open('authdata.pchat', 'r')
                login = authdatar.readline()
                login = login[0:-1]
                cur = connection.cursor()
                cur.execute("SELECT * FROM UserLoginData WHERE UserLoginData.login = '" + login + "'")
                loggedInUserID = cur.fetchone()[0]
                cur.execute("SELECT * FROM MainScreen" + str(loggedInUserID))
                chatList = cur.fetchall()
                for chatID in chatList:
                    chatID = chatID[0]
                    cur.execute("SELECT name FROM ChatInfo WHERE id = " + str(chatID))
                    chatName = str(cur.fetchone()[0])
                    cur.execute("SELECT MAX(`id`) FROM `Chat" + str(chatID) + "messages`")
                    lastMessageID = int(cur.fetchone()[0])
                    cur.execute("SELECT message_text, sender_id FROM `Chat" + str(chatID) + "messages` WHERE id = " + str(lastMessageID))
                    row = cur.fetchone()
                    lastMessageText = str(row[0])
                    senderID = int(row[1])
                    cur.execute("SELECT login from `UserLoginData` WHERE id = " + str(senderID))
                    senderLogin = cur.fetchone()[0]
                    if senderLogin == getLoggedInUserLogin():
                        senderLogin = "You"
                    lastMessageText = senderLogin + ": " + lastMessageText
                    self.children[0].children[0].addLine(Chatline(chatName, lastMessageText, "testavatar.png"))

class PieChat(MDApp):
    def __init__(self, **kwargs):
        super(PieChat, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key, *args):
        if key == 27:
            return self.root.gotoPrevScreen()

    def build(self):
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.accent_palette = 'BlueGray'
        self.theme_cls.theme_style = 'Dark'
        self.title = 'PieChat'
        return PieChatRootWidget()

if __name__ == '__main__':
    PieChat().run()
