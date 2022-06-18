from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager,SlideTransition
from kivy.properties import StringProperty
import os
from araba import ArabaScreen,ArabaIslemlerScreen
from tezgah import TezgahScreen
from login import LoginScreen
from maya import MayaScreen
from yonetim import YonetimScreen

import mysql.connector






# set window size
Window.size=(300,500)        
class MyApp(MDApp):
    
    
    def build(self):
        # define theme colors
        self.theme_cls.primary_palette = "Indigo"


        # load and return kv string
        return Builder.load_file("main.kv") 
    



# run app    
MyApp().run()