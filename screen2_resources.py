import kivy
import json 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen , ScreenManager

from screen3_customizeResource import customizeScreen
 
class resourceScreen( BoxLayout):
    
    def __init__(self ,deviceid , cnt ,  **kwargs):
        super().__init__(**kwargs)
        self.id = deviceid
        self.cnt = cnt 
        self.cnt1 = 0

        #self.selected will store the values of selected resources
        self.selected = {}

        #layout property
        self.orientation = 'vertical'

        # Error handling if you have not selected anything or if file not present 
        try :
            f = open(f"devices\{self.id}.json")
        except :
            self.add_widget(Label(text="You have not selected any device",font_size = 30))
            b_button = Button(text='Back', size_hint = (.1,.1) , pos_hint ={'x':.45, 'y':.5} )
            b_button.bind(on_release = lambda x:self.goToDevicepage())
            self.add_widget(b_button)
            return

        #data store the device json file
        data = json.load(f)

        ################  layouts for title and heading   #############
        content = BoxLayout(orientation = 'horizontal', size_hint_y = .2  )
        content.add_widget(Label(text='OCF Resource Tool' , font_size = 30))
        self.add_widget(content)

        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1)
        content.add_widget(Label(text=f'Select valid OCF Resources types for the device {self.id}' , font_size = 20))
        self.add_widget(content)

        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1  )
        content.add_widget(Label(text='Select                   Capability                       Resource Type                      Resource Href' ,font_size = 20))
        self.add_widget(content)
        ##################################################################


        ##########   loop to control the number of resoruce typr for specific device  #########
        content = GridLayout(cols = 1 , padding = (10,10) , spacing = (10,10) ,size_hint_y = None ,height = self.minimum_height , row_default_height = 35)
        
        #variable for storing device resouceType and href 
        self.resources =  data['mapType']['resourceType']
        href = data['mapType']['resourceHref']
        capability = data['mapType']['capability']
        self.modf = {}

        #initializing every checkbox to False(not selected)
        for i in range(len(self.resources)):
            self.modf[i] = [False,""]

        for i in range(len(self.resources)):
            #layout for each resourceType and checkbox and input box
            minContent = BoxLayout(orientation='horizontal')

            self.selected[i] = CheckBox(size_hint_x = .5)
            minContent.add_widget(self.selected[i])

            minContent.add_widget(Label(text=capability[i][0] ))
            
            minContent.add_widget(Label(text=self.resources[i][0] ))

            self.selected[-(i+1)] = TextInput(text=href[i] , multiline=False) 
            minContent.add_widget(self.selected[-(i+1)])

            content.add_widget(minContent)

        scroll = ScrollView()
        scroll.add_widget(content)
        self.add_widget(scroll)

        #buttons for next(n_button) and back(b_button)
        content = FloatLayout(size_hint_y = .2)

        b_button = Button(text='Back' , size_hint = (.1,.5) , pos_hint = {'x':.35 , 'y' : .2})
        b_button.bind(on_release = lambda x:self.goToDevicepage())
        content.add_widget(b_button)

        n_button = Button(text='Next' , size_hint = (.1,.5) , pos_hint = {'x':.55 , 'y' : .2})
        n_button.bind(on_release = lambda x:self.goToCustomizepage())
        content.add_widget(n_button)

        self.add_widget(content)
     
    ######################################################################################


    #function that changes screen to starting screen
    def goToDevicepage(self):
        App.get_running_app().screenManager.transition.direction = 'right' 
        App.get_running_app().screenManager.current = 'deviceScreen'
    

    ########## IMPORTANT MESSAGE ( TO DO ) ###############
    ##  back button or goToDevicepage not working properly

    #function that changes screen to custoimze screen
    def goToCustomizepage(self ):
        #storing the resources datas that were selected and updated in self.modf
        #and will be passed as a parameter for customize screen class
        for i in range(len(self.resources)):
            self.modf[i][0] = self.selected[i].active
            self.modf[i][1] = self.selected[-(i+1)].text
        
        #making customize screen and changing screen
        self.CustomizeScreen = customizeScreen(self.id ,self.modf , self.cnt )
        self.cnt1 += 1
        screen = Screen(name=f'customizeScreen{self.cnt1}')
        screen.add_widget(self.CustomizeScreen)
        App.get_running_app().screenManager.add_widget(screen)
        App.get_running_app().screenManager.transition.direction = 'left' 
        App.get_running_app().screenManager.current = f'customizeScreen{self.cnt1}'
        

