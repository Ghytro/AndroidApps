from kivy.config import Config
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import easygui
import pytube
import threading
import requests

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def change_screen(self, screen_name):
        self.ids.main_screen_manager.current = screen_name

    def open_file_manager(self, labtext):
        path = easygui.diropenbox()
        print(path)
        if path != None:
            labtext.text = "Your video will be saved in " + path

    def download_video(self, link, dirname, errlabel):
        if link == '':
            errlabel.text = "Link cannot be empty!"
            return
        if '\\' not in dirname:
            errlabel.text = "Choose a directory to save the video"
            return
        self.change_screen("loadingscreen")

        dowloadscreen = self.ids.main_screen_manager.get_screen("downloadscreen")
        
        yt = pytube.YouTube(link)

        video_title = yt.title
        dowloadscreen.ids.preview.ids.video_title.text = video_title

        #getting thumbnail
        video_id = yt.video_id
        dowloadscreen.ids.preview.ids.preview_img.source = f"https://img.youtube.com/vi/{video_id}/0.jpg"
        dowloadscreen.ids.preview.ids.preview_img.reload()

        self.ids.main_screen_manager.current = "downloadscreen"

class YTApp(MDApp):
    def __init__(self, **kwargs):
        super(YTApp, self).__init__(**kwargs)
    def build(self):
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.theme_style = 'Dark'
        self.title = 'YTDownloader'
        return RootWidget()

class SubScreen(Screen):
    pass

class LoadingScreen(Screen):
    pass

class DownloadScreen(Screen):
    pass

YTApp().run()
