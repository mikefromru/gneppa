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
from screens.favorite.favorite import FavoriteScreen
from screens.search.search import SearchScreen

class RightContainer(IRightBodyTouch, MDBoxLayout):

    pass

class MenuHeader(MDBoxLayout):
    '''An instance of the class that will be added to the menu header.'''
    pass


class MyContainer(ButtonBehavior, MDBoxLayout):

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
        DetailScreen.level = {'slug': self.slug, 'id': self.id, 'name': self.name}
        MDApp.get_running_app().sm.transition.direction = 'left'
        MDApp.get_running_app().sm.current = 'detail_screen'

class HomeScreen(Screen):

    scroll_pos_y = 0
    head_height = NumericProperty(70)
    levels = ObjectProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading = MDLabel(text='Loading ...', halign='center')
        self.add_widget(self.loading)
        dct_settings = {'Favorite': 'star', 'Search': 'magnify', 'Settings': 'cog', 'tmp': ''}

        menu_settings_items = [
                {
                    "text": f"{i}",
                    "leading_icon": dct_settings[i],
                    'leading_icon_color': MDApp.get_running_app().theme_cls.primary_dark,
                    "on_release": lambda x=f"{i}": self.menu_settings_callback(x),
                    } for i in dct_settings
            ]

        self.menu_settings = MDDropdownMenu(
            header_cls=MenuHeader(),
            caller=self.ids.settings_menu,
            items=menu_settings_items,
            width_mult=2,
        )

    def menu_settings_callback(self, text_item):
        if text_item == 'Favorite':
            create_screen('favorite.kv', 'favorite_screen', FavoriteScreen)
            FavoriteScreen.levels = self.levels
            MDApp.get_running_app().sm.current = 'favorite_screen'
        elif text_item == 'Search':
            create_screen('search.kv', 'search_screen', SearchScreen)
            MDApp.get_running_app().sm.current = 'search_screen'
        elif text_item == 'Settings':
            create_screen('settings.kv', 'settings_screen', SettingsScreen)
            MDApp.get_running_app().sm.current = 'settings_screen'

        MDApp.get_running_app().sm.transition.direction = 'left'
        self.menu_settings.dismiss()
     
    def add_levels_widgets(self, i):
        ids_favorite = ast.literal_eval(self.config.get('Favorite', 'ids'))
        ids_progress = ast.literal_eval(self.config.get('Progress', 'progress'))

        lst = [
            {
                'opacity_': 0,
                'id': x.get('id'),
                'name': x.get('name'),
                'slug': x.get('slug'),
                'icon': x.get('icon'),
                'star': 'star' if x.get('id') in ids_favorite else '',
                'progress_value': ids_progress[x.get('id')] if x.get('id') in list(ids_progress) else 0.1,
                'progress_value_opacity': 1 if x.get('id') in list(ids_progress) else 0,

                } for x in self.levels] 

        self.ids.rv.data = lst

    
    def on_enter(self):
        self.config = MDApp.get_running_app().config
        Clock.schedule_once(self.add_levels_widgets, .1)
        Clock.schedule_once(self.show_main_box, .2)
        Clock.schedule_once(self.create_some_screens, .4)
        DetailScreen.levels = self.levels 

    def get_stars_icon(self):
        id = self.level.get('id')
        ids = ast.literal_eval(self.config.get('Favorite', 'ids'))
         
        if id in ids:
            self.ids.star.icon_color = MDApp.get_running_app().theme_cls.primary_color
        else:
            self.ids.star.icon_color = 'red'
        
    def show_main_box(self, i):
        self.ids.main_box.opacity = 1
        self.remove_widget(self.loading)

    def create_some_screens(self, i):
        create_screen('settings.kv', 'settings_screen', SettingsScreen)
        create_screen('detail.kv', 'detail_screen', DetailScreen)
