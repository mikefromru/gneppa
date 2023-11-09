from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.label import MDLabel

from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty

from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

import requests
import ast
import logging

# Mine
from utils.utils import create_screen
from screens.detail.detail import DetailScreen
from screens.vocabulary.vocabulary import VocabularyScreen
from settings import url


class MyContainerSearch(ButtonBehavior, MDBoxLayout):

    opacity_ = NumericProperty()
    slug = StringProperty()
    icon = StringProperty()
    id = NumericProperty()
    name = StringProperty()
    description = StringProperty()
    star = StringProperty()
    progress_value = NumericProperty()
    progress_value_opacity = NumericProperty(0)
    text_value_progress = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.opacity_star, 1)
    
    def opacity_star(self, i): # Show star icon in a second
        self.ids.my_star.opacity = 1

    def get_vocabulary(self):
        create_screen('vocabulary.kv', 'vocabulary_screen', VocabularyScreen)
        VocabularyScreen.level = dict(id=self.id, name=self.name)
        MDApp.get_running_app().sm.transition.direction = 'left'
        MDApp.get_running_app().sm.current = 'vocabulary_screen'

    def on_release(self):
        logging.info(f'{self.name=}')
        DetailScreen.level = {
            'slug': self.slug, 
            'id': self.id, 
            'name': self.name,
            'description': self.description,
            }
        MDApp.get_running_app().sm.transition.direction = 'left'
        MDApp.get_running_app().sm.current = 'detail_screen'

class SearchScreen(Screen):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.goBackWindow)
        self.config = MDApp.get_running_app().config
    
    def on_enter(self):
        self.config = MDApp.get_running_app().config

    def on_start(self):
        print('hello from Seearch')
        
    def goBackWindow(self, window, key, *args):
        if key == 13:
            self.callback(self)

    def callback(self, instance):
        instance = self.ids.name
        if len(instance.text) > 2 and len(instance.text) < 25:
            url_ = url + '/api/app/search/'
            payload = {'search': instance.text}
            r = requests.get(url_, params=payload)
            levels = []
            for x in r.json():
                if x['approved']:
                    levels.append(x)
                
            ids_favorite = ast.literal_eval(self.config.get('Favorite', 'ids'))
            ids_progress = ast.literal_eval(self.config.get('Progress', 'progress'))

            lst = [
                {
                    'opacity_': 0,
                    'id': x.get('id'),
                    'name': x.get('name'),
                    'slug': x.get('slug'),
                    'icon': x.get('icon'),
                    'description': x.get('description'),
                    'star': 'star' if x.get('id') in ids_favorite else '',
                    'progress_value': ids_progress[x.get('id')] if x.get('id') in list(ids_progress) else 0.1,
                    'progress_value_opacity': 1 if x.get('id') in list(ids_progress) else 0,

                    } for x in levels] 
            
            if len(lst) != 0:
                try:
                    self.remove_widget(self.icon_empty)
                except:
                    pass

            else:
                self.icon_empty = MDIconButton(icon='cloud-search', pos_hint={'center_x': .5, 'center_y': .5}, icon_size='40sp')
                self.add_widget(self.icon_empty)
                lst = []

            self.ids.search_rv.data = lst
