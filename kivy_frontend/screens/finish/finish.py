from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.properties import NumericProperty

import ast

class FinishScreen(Screen):
    
    level_id = NumericProperty()
    points = NumericProperty() 

    def on_enter(self):
        config = MDApp.get_running_app().config
        get_total_questions = config.getint('Settings', 'questions')
        get_total_minutes = config.getint('Settings', 'minutes')
        self.points = get_total_minutes * get_total_questions
        progress_value = get_total_questions * (get_total_minutes * 60) // 100
        progress = ast.literal_eval(config.get('Progress', 'progress'))

        try:  
            if progress[self.level_id] < 100:
                progress[self.level_id] += progress_value
                if progress[self.level_id] >= 100:
                    progress[self.level_id] = 100

        except KeyError:
            progress[self.level_id] = progress_value

        config.set('Progress', 'progress', progress)
        config.write()
        
        



