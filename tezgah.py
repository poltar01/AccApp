from kivy.uix.screenmanager import Screen,SlideTransition
from kivymd.uix.screen import MDScreen

class TezgahScreen(MDScreen):

    def on_start(self):
        pass
    
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login_screen'
        self.manager.get_screen('login_screen').resetForm()