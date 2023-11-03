from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty

from kivy.metrics import dp
from kivy.utils import rgba
import logging
import ast

from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import (
    IRightBodyTouch, 
    OneLineAvatarIconListItem,
    OneLineIconListItem,
    TwoLineRightIconListItem,
    OneLineAvatarIconListItem,
    OneLineRightIconListItem,
    OneLineAvatarListItem,
)
from kivymd.uix.menu import MDDropdownMenu

# main
from utils.utils import create_screen
from screens.detail.detail import DetailScreen
from screens.vocabulary.vocabulary import VocabularyScreen
from screens.settings.settings import SettingsScreen

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


    def __init__(self, **kwargs):
        super(FavoriteScreen, self).__init__(**kwargs)
        print('----------- FavoriteScreen ----------')
        Clock.schedule_interval(self.get_start, 5)
        #Clock.schedule_once(self.get_start, 3)


    def data_from_dataset(self):
        print('I am working on add widgets ...... ')

        #self.ids.rv_favorite.data = []

        ids_favorite = ast.literal_eval(self.config.get('Favorite', 'ids'))
        ids_progress = ast.literal_eval(self.config.get('Progress', 'progress'))

        favorite_levels = []
        for x in self.levels:
            if x.get('id') in ids_favorite:
                favorite_levels.append(x)
        
        lst = [
            {
                'opacity_': 0,
                'id': x.get('id'),
                'name': x.get('name'),
                'slug': x.get('slug'),
                #'icon': x.get('icon'),
                'star': 'star' if x.get('id') in ids_favorite else '',
                'progress_value': ids_progress[x.get('id')] if x.get('id') in list(ids_progress) else 0.1,
                'progress_value_opacity': 1 if x.get('id') in list(ids_progress) else 0,

                } for x in favorite_levels] 

        return lst


    def refresh_recycleview(self, i):
        #Clock.schedule_once(self.check_empty_favorites, 0.5)
        print('------------ refresh  ------')
        self.ids.rv_favorite.data = self.data_from_dataset()
        self.ids.rv_favorite.refresh_from_data()
        

    def check_empty_favorites(self, i):
        ids_favorite = ast.literal_eval(self.config.get('Favorite', 'ids'))
        if len(ids_favorite) == 0:
            self.empty_text = MDLabel(
                text='Empty',
                halign='center',
                font_name='OpenSans',
                font_size='16sp',
            )
            self.add_widget(self.empty_text)



    def get_start(self, i):
        print('---------------- I am "get_start" in Favorite screen ---------')
        self.config = MDApp.get_running_app().config
        Clock.schedule_once(self.refresh_recycleview, .2)
        #Clock.schedule_once(self.add_levels_widgets, .2)
        DetailScreen.levels = self.levels 

    def on_kv_post(self, *largs):
        #self.ids.favorites.text = 'Bitch'
        print('------- ON_KV_POST ----------')


    def get_stars_icon(self):
        id = self.level.get('id')
        ids = ast.literal_eval(self.config.get('Favorite', 'ids'))
         
        if id in ids:
            self.ids.star.icon_color = MDApp.get_running_app().theme_cls.primary_dark
        else:
            self.ids.star.icon_color = 'grey'

    def send_msg(self):
        var = self.scroll_pos_y
        print(f'fuck you, bitch {var}')
    
    def remove_all(self):
        print('test test test')

    def on_leave(self):
        try:
            self.remove_widget(self.empty_text)
        except:
            pass

    def intro():
        print('------- INTRO ------')
        FavoriteScreen.get_start('self')
