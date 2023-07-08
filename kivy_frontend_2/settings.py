from kivy.utils import platform
from kivy.core.window import Window

if platform == 'linux':
    Window.size = (420, 820)
    Window.top = 10
    Window.left 
    #url = 'http://localhost:8000'
    url = 'http://192.168.0.15:8000'
else:
    #url = 'https://gneppa.com'
    url = 'http://192.168.0.15:8000'

whatsapp_link = 'https://api.whatsapp.com/send?phone=79958760977'
telegram_link = 'https://t.me/+79958760977'

