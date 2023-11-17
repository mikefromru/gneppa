from kivymd.app import MDApp 
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.utils import rgba
from kivy.clock import Clock
import logging
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from settings import url
from kivymd.uix.snackbar import Snackbar

from kivymd.uix.spinner.spinner import MDSpinner
from threading import Thread

class VocabularyScreen(Screen):

    level = ObjectProperty()

    def __init__(self, **kwargs):
        super(VocabularyScreen, self).__init__(**kwargs)

    def on_progress(self, *args):
        pass

    def on_finish(self, *args):
        pass

    # Handle request failures 
    def on_failure(self, req, failure):
        self.loading.text = 'Sorry, no vocabulary for this topic!\nWe are workning on it.'
    
    #Handle request if there is no connection
    def on_error(self, req, error):
        self.loading.text = 'No connection'

    def success(self, *args):
        result = self.request.result
        self.remove_widget(self.loading)
        self.ids.sc.scroll_y = 1

        for x in result:
            items = MDBoxLayout(
                orientation='vertical',
                adaptive_height=True,
                spacing=dp(10),
                padding=(dp(10), dp(10), dp(10), dp(10))
            )
            title = MDLabel(
                text=x.get('name'),
                adaptive_height=True,
                theme_text_color='Custom',
                text_color= MDApp.get_running_app().theme_cls.primary_color,
                font_name='fonts/OpenSans/OpenSans-Bold.ttf',
                font_size='14sp',
                bold=True,
            )

            description = MDLabel(
                text='[i]Description[/i]: ' + x.get('description'),
                markup=True,
                adaptive_height=True,
                font_name='OpenSans',
                theme_text_color='Hint',
                font_style='Subtitle2',
            )

            example = MDLabel(
                text='[i]Example[/i]: ' + x.get('example'),
                markup=True,
                adaptive_height=True,
                theme_text_color='Primary',
                font_style='Subtitle2',
            )

            items.add_widget(title)
            items.add_widget(description)
            items.add_widget(example)
            self.ids.box.add_widget(items)

    def on_enter(self, *args):
        self.loading = MDLabel(
            text='Loading...', 
            halign='center',
            font_name='fonts/OpenSans/OpenSans-Regular',
        )
        self.add_widget(self.loading)

        logging.debug(f'VocabularyScreen is running ... {self.level.get("id")}')
        url_ = f'{url}/api/app/vocabulary/{self.level.get("id")}/'
        self.request = UrlRequest(
            url_, 
            on_success=self.success, 
            on_error=self.on_error,
            on_failure=self.on_failure,
            on_progress=self.on_progress,
            on_finish=self.on_finish,
            timeout=5,
        )

    def go_back(self):
        self.ids.box.clear_widgets()
        self.remove_widget(self.loading)

        self.manager.current = 'home_screen'
        self.manager.transition.direction = 'right'
