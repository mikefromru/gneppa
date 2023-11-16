from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivymd.uix.snackbar import Snackbar

from kivymd.uix.spinner.spinner import MDSpinner

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
import os

from kivy.network.urlrequest import UrlRequest

# mine
from screens.home.home import HomeScreen
from screens.favorite.favorite import FavoriteScreen

from utils.utils import create_screen
from settings import url

from kivy.logger import Logger, LOG_LEVELS
Logger.setLevel(LOG_LEVELS['info'])

__version__ = 1.1

class LoadScreen(Screen):

    def on_enter(self):
        create_screen('home.kv', 'home_screen', HomeScreen)

    def on_leave(self):
        self.ids.my_spinner.active = False

class MainApp(MDApp):

    app_version = __version__
    
    def build(self):
        Logger.info(f'Application: Version is {self.app_version}')

        Builder.load_file('main.kv')

        config = self.config
        self.theme = config.get('Settings', 'theme')
        # self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.primary_palette = 'LightBlue'
        self.theme_cls.primary_hue = "900"  # "500"

        MDApp.get_running_app().theme_cls.theme_style = self.theme

        # Some screens
        #self.sm = ScreenManager(transition=NoTransition())
        self.sm = ScreenManager()
        self.sm.add_widget(LoadScreen(name='load_screen'))

        return self.sm

    def on_start(self):

        self.request = UrlRequest(
            f'{url}/api/app/all/', 
            on_success=self.success,
            on_error=self.on_error,
            timeout=20,
        )


    #Handle request if there is no connection
    def on_error(self, req, error):
        print(error)
        Snackbar(MDLabel(
            text='No connection',
            ),
        ).open()

    def success(self, req, result):
        HomeScreen.levels = [x for x in result if x['approved'] == True]
        self.sm.current = 'home_screen'

    def build_config(self, config):
        self.config.setdefaults(
            "Settings", {
                'theme': 'Dark',
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

    
