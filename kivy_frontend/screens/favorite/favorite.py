from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty, BooleanProperty

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

from kivymd.uix.label import MDLabel

from kivy.logger import Logger, LOG_LEVELS

Logger.setLevel(LOG_LEVELS["debug"])


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

    bla = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        Logger.debug('Aplication: FavoriteScreen __init__')
        super(FavoriteScreen, self).__init__(**kwargs)
        self.config = MDApp.get_running_app().config
        self.fav_event = Clock.schedule_interval(self.get_or_update_favorites_widgets, 2)
        #self.bla_event = Clock.schedule_interval(self.tutu, 2)

    def tutu(self, i):
        Logger.debug('Application: tutu() is checking ...')
        if not self.bla:
           self.fav_event.cancel() 


    def get_or_update_favorites_widgets(self, i):
        Logger.debug('Application: run get_or_update_favorites_widgets()')
        favorites_lst = eval(self.config.get('Favorite', 'ids'))
        if len(favorites_lst) > 0:
            ids_progress = ast.literal_eval(self.config.get('Progress', 'progress'))
            DetailScreen.levels = favorites_lst

            lst = [
                {
                    'id': x.get('id'),
                    'name': x.get('name'),
                    'slug': x.get('slug'),
                    'progress_value': ids_progress[x.get('id')] if x.get('id') in list(ids_progress) else 0.1,
                    } for x in favorites_lst] 

            self.ids.rv_favorite.data = lst
        else:
            self.empty_text = MDLabel(
                text='Empty',
                halign='center',
                font_name='OpenSans',
                font_size='16sp',
            )
            self.add_widget(self.empty_text)

           


    '''

    def data_from_dataset(self):
        Logger.debug('Application: data_from_dataset()')

        self.config = MDApp.get_running_app().config
        favorites_lst = eval(self.config.get('Favorite', 'ids'))
        DetailScreen.levels = favorites_lst

        lst = [
            {
                #'opacity_': 0,
                'id': x.get('id'),
                'name': x.get('name'),
                'slug': x.get('slug'),
                ##'icon': x.get('icon'),
                #'star': 'star' if x.get('id') in ids_favorite else '',
                #'progress_value': ids_progress[x.get('id')] if x.get('id') in list(ids_progress) else 0.1,
                #'progress_value_opacity': 1 if x.get('id') in list(ids_progress) else 0,
                } for x in favorites_lst] 

        return lst


    def refresh_recycleview(self, i):
        Logger.debug('Application: refresh_recycleview()')
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
        Logger.debug('Application: get_start()')
        self.config = MDApp.get_running_app().config
        #Clock.schedule_once(self.refresh_recycleview, .2)
        #self.refresh_recycleview()

        DetailScreen.levels = self.levels 

        #Clock.schedule_once(self.add_levels_widgets, .2)

    def on_kv_post_TMP(self, *largs):
        Logger.debug('Application: ON_KV_POST()')
        #self.ids.my_title.text = 'Bitch'
        Clock.schedule_once(self.get_start, 1)
        #self.add_favorites_widgets()

    def get_stars_icon(self):
        id = self.level.get('id')
        ids = ast.literal_eval(self.config.get('Favorite', 'ids'))
         
        if id in ids:
            self.ids.star.icon_color = MDApp.get_running_app().theme_cls.primary_dark
        else:
            self.ids.star.icon_color = 'grey'

    def on_leave(self):
        try:
            self.remove_widget(self.empty_text)
        except:
            pass
    '''
