import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.graphics.instructions import Canvas
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen , ScreenManager

from device import devicePage 

class home(BoxLayout ):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        #self.device = ['oic.d.airconditioner' , 'oic.d.airpurifier']
        self.DevicePage = None
        
    device_name = ListProperty(['oic.d.airconditioner' , 'oic.d.airpurifier','oic.d.dishwasher','oic.d.dryer','oic.d.light','oic.d.oven','oic.d.refrigerator','oic.d.robotcleaner','oic.d.sensor','oic.d.smartlock' , 'oic.d.smartplug', 'oic.d.switch','oic.d.thermostat','oic.d.tv','oic.d.washer'])
    device = [ObjectProperty(True),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False)]
    selectedDevice = StringProperty()

    def deviceSelect(self , n):
        self.selectedDevice = self.device_name[n]

    def goToDevicePage(self):
        self.DevicePage = devicePage(self.selectedDevice)
        screen = Screen(name='device')
        screen.add_widget(self.DevicePage)
        modifier.screenManager.add_widget(screen)
        modifier.screenManager.transition.direction = 'left' 
        modifier.screenManager.current = 'device'
        

class myApp(App):
    def build(self):
        self.screenManager = ScreenManager()
        self.homePage = home()
        screen = Screen(name='home')
        screen.add_widget(self.homePage)
        self.screenManager.add_widget(screen)

        return self.screenManager


if __name__ == "__main__":
    modifier = myApp()
    modifier.run()