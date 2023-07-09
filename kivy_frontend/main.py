from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivymd.uix.snackbar import Snackbar

from kivy.uix.screenmanager import (
    ScreenManager, 
    Screen,
    NoTransition,
    FadeTransition,
    SwapTransition,
    SlideTransition,
)

from kivy.lang import Builder
from threading import Thread

from kivy.network.urlrequest import UrlRequest

# mine
from screens.home.home import HomeScreen
from utils.utils import create_screen
from settings import url

__version__ = '0.8'

class LoadScreen(Screen):

    def on_enter(self):
        create_screen('home.kv', 'home_screen', HomeScreen)

class MainApp(MDApp):

    app_version = __version__
    
    def build(self):
        Builder.load_file('main.kv')
        Builder.load_file('custom.kv')
        config = self.config
        theme = config.get('Settings', 'theme')
        MDApp.get_running_app().theme_cls.primary_palette = 'Teal'
        MDApp.get_running_app().theme_cls.theme_style = theme

        # Some screens
        self.sm = ScreenManager()
        self.sm.add_widget(LoadScreen(name='load_screen'))
        return self.sm

    def on_start(self):
        self.request = UrlRequest(
            f'{url}/api/app/all/', 
            on_success=self.success,
            on_error=self.on_error,
            timeout=5,
        )

    #Handle request if there is no connection
    def on_error(self, req, error):
        Snackbar(MDLabel(
            text='No connection',
            ),
        ).open()

    #def success(self, *args):
    def success(self, req, result):
        HomeScreen.levels = [x for x in result if x['approved'] == True]
        self.sm.current = 'home_screen'

    def get_data(self):
        for x in range(50000):
            print(x)
        Clock.schedule_interval(self.go_to_app, 1)

    def go_to_app(self, i):
        self.sm.current = 'home_screen'

    def build_config(self, config):
        self.config.setdefaults(
            "Settings", {
                'theme': 'Light',
                'questions': 5,
                'minutes': 1,
                'sound': True,
            }
        )

        self.config.setdefaults(
            "Favorite", {'ids': []},
        )

        self.config.setdefaults(
            "Progress", {'progress': {}},
        )

if __name__ == '__main__':
    LabelBase.register(name='OpenSans',
        fn_regular='fonts/OpenSans/OpenSans-Regular.ttf',
        fn_italic='fonts/OpenSans/OpenSans-Italic.ttf',
        fn_bold='fonts/OpenSans/OpenSans-Bold.ttf',
    )

    MainApp().run()

    
