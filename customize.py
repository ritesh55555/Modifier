import kivy
import json 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen , ScreenManager
from kivy.lang import Builder


class customizePage(BoxLayout):

    deviceid = StringProperty('')
    modf = ObjectProperty()

    def __init__(self, did , modif   , **kwargs):
        super().__init__(**kwargs)
        self.deviceid = did
        self.modf = modif
        f = open(f"{self.deviceid}.json")
        self.data = json.load(f)
        print(self.deviceid)
        print(self.modf)
    
        
        
