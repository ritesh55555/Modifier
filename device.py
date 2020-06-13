import kivy
import json 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen , ScreenManager

 
class devicePage(BoxLayout):
    #print(self.selectedDevice)
    #Builder.load_file('device.kv')
    def __init__(self ,deviceId , **kwargs):
        super().__init__(**kwargs)
        self.id = deviceId
        self.selected = {}
        self.orientation = 'vertical'
        try :
            f = open(f"{self.id}.json")
        except :
            self.add_widget(Label(text="File not found",font_size = 30))
            b_button = Button(text='Back' )
            b_button.bind(on_release = lambda x:self.goToHomepage())
            self.add_widget(b_button)
            return
        data = json.load(f)
        print(data)
        content = BoxLayout(orientation = 'horizontal', size_hint_y = .2  )
        content.add_widget(Label(text='OCF Resource Tool' , font_size = 30))
        self.add_widget(content)

        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1)
        content.add_widget(Label(text=f'Select valid OCF Resources types for the device {self.id}' , font_size = 20))
        self.add_widget(content)

        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1  )
        content.add_widget(Label(text='Resource Type                           Resource Href' ,font_size = 20))
        self.add_widget(content)
    
        content = BoxLayout(orientation='vertical' , spacing = 10 , padding = [70,20,100,20])
        resources =  data['mapType']['resourceType']
        href = data['mapType']['resourceHref']
        for i in range(len(resources)):
            minContent = BoxLayout(orientation='horizontal')
            self.selected[resources[i][0]] = CheckBox(active=False,size_hint_x = .3)
            minContent.add_widget(self.selected[resources[i][0]])
            minContent.add_widget(Label(text=resources[i][0] , size_hint_x= .4))
            var = TextInput(text=href[i] , multiline=False)
            minContent.add_widget(var)
            content.add_widget(minContent)
        self.add_widget(content)

        content = FloatLayout(size_hint_y = .2)
        b_button = Button(text='Back' , size_hint = (.1,.5) , pos_hint = {'x':.35 , 'y' : .2})
        b_button.bind(on_release = lambda x:self.goToHomepage())
        content.add_widget(b_button)
        n_button = Button(text='Next' , size_hint = (.1,.5) , pos_hint = {'x':.55 , 'y' : .2})
        content.add_widget(n_button)
        self.add_widget(content)


    def goToHomepage(self):
        App.get_running_app().screenManager.current = 'home'
