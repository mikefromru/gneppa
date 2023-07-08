from kivymd.app import MDApp
from kivy.lang import Builder
from pathlib import Path
import os
import logging
from kivy.network.urlrequest import UrlRequest
from random import sample

def create_screen(kv_file, name_screen, NameScreen):
    ''' To create a new screen if it does not exist'''
    if not MDApp.get_running_app().sm.has_screen(name=name_screen):
        # Conver imutuble type Tuple to List
        # for changing file extension 
        name = list(os.path.splitext(kv_file))
        if name[1] == '':
            name[1] = '.kv'
        Builder.load_file(f'screens/{name[0]}/{name[0]}{name[1]}') 
        MDApp.get_running_app().sm.add_widget(NameScreen(name=name_screen))
        logging.info(f'Created {name_screen}')
