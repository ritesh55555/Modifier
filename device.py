import kivy
import json 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.graphics.instructions import Canvas
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen , ScreenManager

#import oic.d.airconditioner.json

class devicePage(BoxLayout):
    #print(self.selectedDevice)
    #Builder.load_file('device.kv')
    def __init__(self ,deviceId , **kwargs):
        super().__init__(**kwargs)
        self.id = deviceId
        try :
            f = open(f"{self.id}.json")
            self.add_widget(Label(text="hii"))
        except :
            self.add_widget(Label(text="File not found",font_size = 30))
            return
        data = json.load(f)
        print(data)