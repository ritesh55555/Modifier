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
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen , ScreenManager

#importing second screen class
from screen2_resources import resourceScreen 

class deviceScreen(BoxLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        
        self.ResourceScreen = None
        self.cnt = 0 

    #storing all the device's json file name to use later   
    device_name = ListProperty(['oic.d.airconditioner' , 'oic.d.airpurifier','oic.d.dishwasher','oic.d.dryer','oic.d.light','oic.d.oven','oic.d.refrigerator','oic.d.robotcleaner','oic.d.sensor','oic.d.smartlock' , 'oic.d.smartplug', 'oic.d.switch','oic.d.thermostat','oic.d.tv','oic.d.washer'])
    device = [ObjectProperty(True),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False),ObjectProperty(False)]
    
    #selectedDevice will store the name of device selected in checkbox
    selectedDevice = StringProperty()


    #function gets triggered when check box is selected , stores the last selected checkbox device name
    def deviceSelect(self , n):
        self.selectedDevice = self.device_name[n]


    #function to go to resourceScreen
    #uses screenManager.current function 
    def goToResourcePage(self):

        # making a new screen of select resource with the help of imported clas
        # pass the device name parameter in the class 
        self.cnt += 1
        self.ResourceScreen = resourceScreen(self.selectedDevice , self.cnt )
        screen = Screen(name=f'resourceScreen{self.cnt}')
        screen.add_widget(self.ResourceScreen)
        #changing screen to resource screen
        modifier.screenManager.add_widget(screen)
        modifier.screenManager.transition.direction = 'left' 
        modifier.screenManager.current = f'resourceScreen{self.cnt}'
        
        

class screen1_deviceApp(App):
    #program starts from here
    def build(self):
        self.screenManager = ScreenManager()
        self.DeviceScreen = deviceScreen()
        screen = Screen(name='deviceScreen')
        screen.add_widget(self.DeviceScreen)
        self.screenManager.add_widget(screen)
        return self.screenManager


if __name__ == "__main__":
    modifier = screen1_deviceApp()
    modifier.run()