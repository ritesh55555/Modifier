import kivy
import json 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen , ScreenManager


class customizePage(BoxLayout):

    def __init__(self, did , modif   , **kwargs):
        super().__init__(**kwargs)
        self.deviceid = did
        self.modf = modif
        f = open(f"{self.deviceid}.json")
        self.data = json.load(f)
        self.newData = self.data.copy()
        
        self.orientation = "vertical"

        #data required to display
        self.resource = []
        for i in range(len(self.data['mapType']['resourceType'])):
            if self.modf[i][0] == True :
                self.resource.append(i)

        #title box
        content = BoxLayout(orientation = 'horizontal', size_hint_y = .2  )
        content.add_widget(Label(text='OCF Resource Tool' , font_size = 30))
        self.add_widget(content)

        #second title box
        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1)
        content.add_widget(Label(text='Customize Selected Resource type for ' + self.deviceid , font_size = 20))
        self.add_widget(content)

        #scrollbox
        content = BoxLayout(orientation="vertical" , padding = 20)
        for i in range(len(self.resource)):
            #each resuorce type box
            string1 = self.data['mapType']['resourceType'][self.resource[i]][0]
            string2 = self.data['mapType']['capability'][self.resource[i]][0]
            self.newData['mapType']['resourceHref'][self.resource[i]] = self.modf[self.resource[i]][1]

            minContent = BoxLayout(orientation="horizontal")
            minContent.add_widget(Label(text = string1 + self.modf[self.resource[i]][1] , size_hint_x = .5 ))
            content.add_widget(minContent)
            if "valueMap" in self.data['mapData'][string2] :
                arr1 = self.data['mapData'][string2]["valueMap"]["STValue"]
                arr2 = self.data['mapData'][string2]["valueMap"]["OCFValue"]
                for j in range(len(arr1)):
                    minContent = BoxLayout(orientation="horizontal")
                    minContent.add_widget(CheckBox())
                    minContent.add_widget(Label(text=str(arr2[j])))
                    minContent.add_widget(Label(text = "OIC Resource Mapping value"))
                    minContent.add_widget(TextInput(text = arr1[j]))
                    content.add_widget(minContent)

            else :
                minContent = BoxLayout(orientation="horizontal")
                minContent.add_widget(CheckBox())
                minContent.add_widget(Label(text="Minimum Value"))
                minContent.add_widget(TextInput())
                content.add_widget(minContent)
                minContent = BoxLayout(orientation="horizontal")
                minContent.add_widget(CheckBox())
                minContent.add_widget(Label(text="Maximunm Value"))
                minContent.add_widget(TextInput())
                content.add_widget(minContent)
        
        self.add_widget(content)
        
        #Generate button
        content  = FloatLayout(size_hint_y = .2)
        back = Button(text = "Back" , size_hint = (.2,.4) , pos_hint = {'x':.3 , 'y' : .4})
        back.bind(on_release =lambda x:self.goBack())
        content.add_widget(back)
        generate = Button(text = "Generate" , size_hint = (.2,.4) , pos_hint = {'x':.5 , 'y' : .4})
        generate.bind(on_release = lambda x:self.generateJSON())
        content.add_widget(generate)
        self.add_widget(content)

    def goBack(self):
        App.get_running_app().screenManager.transition.direction = 'right' 
        App.get_running_app().screenManager.current = 'device'

    def generateJSON(self):
        popup = Popup(title='JSON file',size_hint=(.9, .9))
        popup.content = BoxLayout(orientation="vertical")
        popup.content.add_widget(Label(text="hi there"))
        layout = FloatLayout(size_hint_y = .2)
        button = Button(text=' Close ', size_hint = (.2,.4) , pos_hint = {'x':.3 , 'y' : .4} )
        button.bind(on_press=popup.dismiss)
        layout.add_widget(button)
        downld = Button(text = "Download" , size_hint = (.2,.4) , pos_hint = {'x':.5 , 'y' : .4})
        downld.bind(on_press = lambda x:self.downloadFile())
        layout.add_widget(downld)
        popup.content.add_widget(layout)
        popup.open()

    def downloadFile(self):
        with open('newData.json', 'w') as fp:
            json.dump(self.newData, fp,  indent=2)