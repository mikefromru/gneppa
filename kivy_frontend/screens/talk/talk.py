from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from kivy.properties import (
    ObjectProperty, 
    StringProperty, 
    ListProperty,
    NumericProperty,
    BooleanProperty,
)

import time
import logging
import requests
from threading import Thread
from kivy.utils import platform
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# uix
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar

# main
from screens.finish.finish import FinishScreen
from settings import url
from kivy.storage.jsonstore import JsonStore
from utils.utils import create_screen

if platform != 'android':
    from playsound import playsound

class TalkScreen(Screen):

    level = ObjectProperty()
    counter = NumericProperty()
    n_question = NumericProperty(1)
    total = NumericProperty()
    pause = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        # this code for Finish Screen
        create_screen('finish.kv', 'finish_screen', FinishScreen)
        self.config = MDApp.get_running_app().config
        self.sound_settings = self.config.get('Settings', 'sound')
        self.questions = self.level.get('questions')
        self.total = len(self.questions)
        self.say()
 
    def set_counter(self, *args):
        self.counter = self.config.getint('Settings', 'minutes') * 60
        self.ids.timer.text = time.strftime('%M:%S', time.gmtime(self.counter))
    
    def set_tablo(self, n_question, total):
        self.ids.tablo.text = str(n_question) + '/' + str(self.total)

    def set_button_active(self, i):
        self.ids.play_button.disabled = False
        self.ids.play_button.icon_color = MDApp.get_running_app().theme_cls.primary_dark
    
    def play(self):
        self.ids.play_button.icon_color = MDApp.get_running_app().theme_cls.primary_dark
        self.ids.play_button.disabled = True
        '''This is a play button to get a voice.
           Make the play button disabled then to run < play_ > function to get voice 
        '''
        self.ids.play_button.disabled_color = MDApp.get_running_app().theme_cls.primary_dark
        Clock.schedule_once(self.play_, 0.2) # Run play_

    def play_(self, i):
        if platform == 'android':
            self.sound = SoundLoader.load('sounds/sound.ogg')
            if self.sound:
                Clock.schedule_once(self.set_button_active, self.sound.length)
                self.sound.play()
        else:
            playsound('sounds/sound.ogg')
            Clock.schedule_once(self.set_button_active, 4)


    def say(self, *args):
        self.ids.timer.opacity = 0
        self.set_tablo(self.n_question, self.total) # Set tablo in the head
        self.set_counter() # Set timer in reable format
        Clock.schedule_once(self.show_timer, 3)
        Clock.schedule_once(self.run_timer, 3)
        self.ids.name.text = self.questions[0].get('name') + ' ?' # Get question text
        self.ids.play_button.disabled = True # Set play button disabled then run say() func
        self.ids.play_button.disabled_color = MDApp.get_running_app().theme_cls.primary_dark
        Clock.schedule_once(self.say_, 0.2)
    
    def say_(self, i):
        try:
            self.check_sound = self.questions[0].get('robot_voice')
            self.n_question += 1
            if self.check_sound:
                url_ = url + self.check_sound
                r = requests.get(url_)
                with open('sounds/sound.ogg', 'wb') as o:
                    o.write(r.content)
                if platform == 'android':
                    self.sound = SoundLoader.load('sounds/sound.ogg')
                    if self.sound:
                        Clock.schedule_once(self.set_button_active, self.sound.length)
                        self.sound.play()
                else:
                    playsound('sounds/sound.ogg')
                    Clock.schedule_once(self.set_button_active, 4)
            else:
                self.event_timer.cancel()
        except IndexError as err:
            print(err)

    def run_timer(self, i):
        self.event_timer = Clock.schedule_interval(self.timer, 1)

    def show_timer(self, i):
        self.ids.timer.opacity = 1

    def hide_timer(self, i):
        self.ids.timer.opacity = 0

    def timer(self, *args):
        path_over_sound = 'sounds/over.ogg'
        var = time.gmtime(self.counter)
        self.ids.timer.text = time.strftime('%M:%S', var)
        self.counter -= 1

        if self.counter == 2:
            if self.sound_settings == 'True':
                if platform == 'android':
                    self.sound = SoundLoader.load('sounds/over.ogg')
                    if self.sound:
                        self.sound.play()
                else:
                    playsound('sounds/over.ogg')
        elif self.counter == 29:
            self.ids.next_btn.opacity = 1
            self.ids.next_btn.disabled = False

        elif self.counter == 0:
            self.event_timer.cancel()
            self.hide_next_btn(self)
            self.next()

    def hide_next_btn(self, i):
        self.ids.next_btn.opacity = 0 # Hide the next button in kv file
        self.ids.next_btn.disabled = True

    def next(self):
        try:
            self.event_timer.cancel()
            del self.questions[0]
            self.ids.name.text = self.questions[0].get('name')
            self.say()
        except IndexError:
            FinishScreen.level_id = self.level.get('id')
            MDApp.get_running_app().sm.current = 'finish_screen'
            self.event_timer.cancel()

    def next_button(self):
        ''' This function to get next question by click on button'''
        if len(self.questions) > 1:
            self.event_timer.cancel()
            del self.questions[0]
            self.ids.name.text = self.questions[0].get('name')
            Clock.schedule_once(self.hide_next_btn, 0.3)
            Clock.schedule_once(self.say, 1)

        elif len(self.questions) == 1:
            MDSnackbar(MDLabel(text='This is the last one')).open()

    def make_pause(self):
        if self.pause:
            self.event_timer()
            self.pause = False
        else: 
            self.event_timer.cancel()
            self.pause = True

    def on_leave(self):
        self.ids.name.text = ''
        self.ids.timer.opacity = 0
        try:
            self.event_timer.cancel()
        except:
            pass
        self.n_question = 1
        self.hide_next_btn(self)
        self.ids.play_button.disabled = False # Set play button disabled then run say() func
        self.ids.play_button.disabled_color = MDApp.get_running_app().theme_cls.primary_dark
