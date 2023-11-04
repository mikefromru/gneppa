from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
import logging
import ast # convert string to another Python data type from ini file

from kivy.properties import ObjectProperty, StringProperty
import logging
from kivy.network.urlrequest import UrlRequest
from kivy.metrics import dp
from kivy.utils import rgba
from random import sample
from kivymd.app import MDApp

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDLabel, MDIcon

from kivymd.uix.snackbar import MDSnackbar
from kivy.clock import Clock

# mine
from utils.utils import create_screen
from settings import url
from screens.talk.talk import TalkScreen


class DetailScreen(Screen):
    
    levels = ObjectProperty()
    level = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading = MDLabel(text='Loading ...', halign='center')

    def on_enter(self):
        self.config = MDApp.get_running_app().config
        Clock.schedule_once(self.get_color_of_star, 0.5)
        create_screen('talk.kv', 'talk_screen', TalkScreen)
        self.ids.title.text = self.level.get('name')
        slug = self.level.get('slug')
        self.request = UrlRequest(f'{url}/api/app/{slug}/', self.success)
        self.total_questions = self.config.get('Settings', 'questions')

    def success(self, *args):
        questions = [x for x in self.request.result if len(x.get('name')) < 61]
        try:
            result = sample(questions, int(self.total_questions))
        except ValueError:
            result = sample(questions, len(questions))
        self.level['questions'] = result
        TalkScreen.level = self.level
        j = 1
        for x in result:
            bl = MDBoxLayout(radius=dp(3), md_bg_color=MDApp.get_running_app().theme_cls.bg_dark, size_hint_y=None, height=dp(45), padding=(dp(10), dp(0), dp(0), dp(0))) 
            gl = MDGridLayout(cols=2)
            gl.add_widget(MDIcon(icon='circle-small',
                size_hint_y=None, 
                size_hint_x=None, 
                theme_text_color='Custom',
                pos_hint={'center_y': .5},
                text_color=MDApp.get_running_app().theme_cls.primary_color,
                font_size='10sp',
                width=dp(0),
                )
            )
            #bl.add_widget(MDLabel(text=f"[b][color=009688]{j}.[/color][/b] [size=14sp]{x.get('name')}?[/size]", 
            bl.add_widget(MDLabel(text=f"[b]{j}.[/b] [size=14sp]{x.get('name')}?[/size]", 
                valign='center',
                padding_x=dp(0), 
                font_name='fonts/OpenSans/OpenSans-Medium.ttf',
                markup=True))
            self.ids.box.add_widget(bl)
            j += 1

        self.remove_widget(self.loading)
        self.ids.question_lbl.opacity = 1
        self.ids.start_btn.opacity = 1
    
    def get_color_of_star(self, i):
        lst_fav = eval(self.config.get('Favorite', 'ids'))
        matches = [item for item in lst_fav if item['id'] == self.level.get('id')]

        if len(matches) > 0:
            print('Removed')
            self.ids.star.icon_color = MDApp.get_running_app().theme_cls.primary_dark
        else:
            print('Added')
            fav = {'slug': self.level.get('slug'), 'id': self.level.get('id'), 'name': self.level.get('name')}
            self.ids.star.icon_color = 'gray'

        self.ids.star.opacity = 1


    def set_star(self):
        lst_fav = eval(self.config.get('Favorite', 'ids'))
        matches = [item for item in lst_fav if item['id'] == self.level.get('id')]

        if len(matches) > 0:
            # Remove from favorite
            lst_fav.remove(*matches)
            self.ids.star.icon_color = 'gray'
        else:
            # Add to favorite
            if len(lst_fav) < 10:
                fav = {'slug': self.level.get('slug'), 'id': self.level.get('id'), 'name': self.level.get('name')}
                lst_fav.append(fav)
                self.ids.star.icon_color = MDApp.get_running_app().theme_cls.primary_dark
            else:
                MDSnackbar(MDLabel(text='You can have only 10 favorite topics')).open()



        self.config.set('Favorite', 'ids', lst_fav)
        self.config.write()

    def on_leave(self):
        self.ids.box.clear_widgets()
        self.ids.question_lbl.opacity = 0
        self.ids.start_btn.opacity = 0
        self.ids.star.opacity = 0

    def show_icon_star(self, i):
        self.ids.star.opacity = 1


