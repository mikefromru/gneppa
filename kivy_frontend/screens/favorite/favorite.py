from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty

import logging
import ast

from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import (
    IRightBodyTouch, 
)

# main
from utils.utils import create_screen
from screens.detail.detail import DetailScreen
from screens.vocabulary.vocabulary import VocabularyScreen

from kivy.logger import Logger


class RightContainer(IRightBodyTouch, MDBoxLayout):
    pass

class MenuHeader(MDBoxLayout):
    pass

class MyContainerFavorite(ButtonBehavior, MDBoxLayout):

    opacity_ = NumericProperty()
    slug = StringProperty()
    icon = StringProperty('home')
    id = NumericProperty()
    name = StringProperty()
    description = StringProperty()
    star = StringProperty()
    progress_value = NumericProperty()
    progress_value_opacity = NumericProperty(0)
    text_value_progress = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_vocabulary(self):
        create_screen('vocabulary.kv', 'vocabulary_screen', VocabularyScreen)
        VocabularyScreen.level = dict(id=self.id, name=self.name)
        MDApp.get_running_app().sm.transition.direction = 'left'
        MDApp.get_running_app().sm.current = 'vocabulary_screen'

    def on_release(self):
        logging.info(f'{self.name=}')
        DetailScreen.level = {'slug': self.slug, 'id': self.id, 'name': self.name}
        MDApp.get_running_app().sm.transition.direction = 'left'
        MDApp.get_running_app().sm.current = 'detail_screen'


class FavoriteScreen(Screen):

    scroll_pos_y = 0
    head_height = NumericProperty(70)
    levels = ObjectProperty()
    name = StringProperty()
    demo_test = StringProperty()

    bla = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        Logger.debug('Aplication: FavoriteScreen __init__')
        super(FavoriteScreen, self).__init__(**kwargs)
        self.config = MDApp.get_running_app().config
        self.fav_event = Clock.schedule_interval(self.get_or_update_favorites_widgets, 2)

    def get_or_update_favorites_widgets(self, i):
        Logger.debug('Application: run get_or_update_favorites_widgets()')
        favorites_lst = eval(self.config.get('Favorite', 'ids'))
        ids_progress = ast.literal_eval(self.config.get('Progress', 'progress'))
        DetailScreen.levels = favorites_lst

        lst = [
            {
                'id': x.get('id'),
                'name': x.get('name'),
                'description': x.get('description'),
                'slug': x.get('slug'),
                'icon': '' if x.get('icon') == 'circle' else x.get('icon'),
                'progress_value': ids_progress[x.get('id')] if x.get('id') in list(ids_progress) else 0.1,
                } for x in favorites_lst] 

        self.ids.rv_favorite.data = lst
       