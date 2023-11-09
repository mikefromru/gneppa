from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDRoundFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.storage.jsonstore import JsonStore
from kivymd.uix.menu import MDDropdownMenu

from kivy.metrics import dp

from kivy.properties import (
    NumericProperty,
    StringProperty,
)

from kivy.lang import Builder
import webbrowser
import datetime

# Mine
from settings import whatsapp_link, telegram_link

class SettingsScreen(Screen):

    dialog = None
    minutes = NumericProperty()
    questions = StringProperty()

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.config = MDApp.get_running_app().config
        Clock.schedule_once(self.create_menu, 1)
        Clock.schedule_once(self.get_window, 2)
        Clock.schedule_once(self.get_version, 3)
        
        self.menu_minutes = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                'height': dp(54),
                "on_release": lambda x=f"{i}": self.minutes_change(x),
            } for i in [1, 2, 5]
        ]

        self.menu_questions = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                'height': dp(54),
                "on_release": lambda x=f"{i}": self.questions_change(x),
            } for i in ['5', '7', '10'] # you can add 'All' to the list
        ]

    def create_menu(self, i):
        """This func is to create two widgets for minutes and questions"""
        self.menu_minutes = MDDropdownMenu(
            caller=self.ids.minutes,
            items=self.menu_minutes,
            width_mult=1,
        )

        self.menu_questions = MDDropdownMenu(
            caller=self.ids.questions,
            items=self.menu_questions,
            width_mult=1,
        )

    #def on_enter(self):
    def get_version(self, i):
        current_year = datetime.date.today().year
        msg = f'(c) 2022-{current_year}. MFR'
        self.ids.fromtoyear.text = msg
        app_version= MDApp.get_running_app().app_version
        self.ids.app_version.text =  'Version ' + str(app_version)
        #Clock.schedule_once(self.get_window, 0.1)

    def get_window(self, i):
        self.minutes = self.config.getint('Settings', 'minutes')
        self.questions = self.config.get('Settings', 'questions')
        self.sound = self.config.get('Settings', 'sound')
        theme = self.config.get('Settings', 'theme')
        if theme == 'Dark':
            self.ids.set_bool.active = True
        if self.sound == 'True':
            self.ids.set_sound.active = True

    def minutes_change(self, insta):
        self.minutes = int(insta)
        self.config.set('Settings', 'minutes', int(insta))
        self.config.write()
        self.menu_minutes.dismiss()

    def change_theme(self, insta):
        switch = self.ids.set_bool.active

        if switch:
            MDApp.get_running_app().theme_cls.theme_style = 'Dark'
            self.config.set('Settings', 'theme', 'Dark')
        else:
            MDApp.get_running_app().theme_cls.theme_style = 'Light'
            self.config.set('Settings', 'theme', 'Light')
            Builder.load_file('screens/home/home.kv')

        self.config.write()

    def questions_change(self, insta):
        self.questions = insta
        self.config.set('Settings', 'questions', insta)
        self.config.write()
        self.menu_questions.dismiss()

    def set_sound(self, instance):
        switch = self.ids.set_sound.active
        if switch:
            self.config.set('Settings', 'sound', True)
        else:
            self.config.set('Settings', 'sound', False)
        self.config.write()

    def get_messanger(self, instance):
        if instance == 'telegram':
            webbrowser.open(telegram_link)
        else:
            webbrowser.open(whatsapp_link)

    def get_privacy_police(self):
        print('hi from Policy')
        webbrowser.open('https://gneppa.com/politica')

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def reset_progress(self, instance):
        self.config.set('Progress', 'progress', {})
        self.config.write()
        self.dialog_close()

    def clean_progress(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Reset progress levels?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=self.dialog_close
                    ),
                    MDRoundFlatButton(
                        text="ACCEPT",
                        on_release=self.reset_progress,
                        theme_text_color="Primary",
                    ),
                ],
            )
        self.dialog.open()

