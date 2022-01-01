rom kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import requests as req
from kivy.properties import ObjectProperty

ip = '127.0.0.1'
port = '8800'


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv

def buttonEvents(button):
    buttons_list = {'+': 'volume-up', '-': 'volume-down',
                    '=>': 'next-song', '<=': 'previous-song', 'play/pause': 'pause-play-toggle',
                    'space': 'space', 'enter': 'enter', 'exit': 'exit', 'left': 'left',
                    'right': 'right', 'shutdown': 'shutdown'}
    if button in buttons_list:
        try:
            req.get(f'http://{ip}:{port}/{buttons_list[button]}')
        except Exception:
            pass

if __name__ == "__main__":
    MyMainApp().run()
