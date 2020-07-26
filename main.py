from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import easygui
import pytube
import threading

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def change_screen(self, screen_name):
        self.ids.main_screen_manager.current = screen_name

    def open_file_manager(self, labtext):
        path = easygui.diropenbox()
        print(path)
        if path != None:
            labtext.text = path

    def download_video(self, link, dirname):
        if link == '':
            print("link cannot be empty")
            return
        if '\\' not in dirname:
            print("choose a directory")
            return
        self.change_screen("loadingscreen")
        video_title = pytube.YouTube(link).title
        self.ids.main_screen_manager.get_screen("downloadscreen").ids.video_title.text = video_title
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