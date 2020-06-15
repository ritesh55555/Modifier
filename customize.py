import kivy
import json 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen , ScreenManager


class customizePage(BoxLayout):

    def __init__(self, did , modif   , **kwargs):
        super().__init__(**kwargs)
        self.deviceid = did
        self.modf = modif
        f = open(f"devices\{self.deviceid}.json")
        self.data = json.load(f)
        #self.newData = self.data.copy()
        self.newData = {"mapType" : {"capability":[], "resourceType":[],"resourceHref":[]} , "mapData" : {}}
        
        self.orientation = "vertical"

        #data required to display
        
        #title box
        content = BoxLayout(orientation = 'horizontal', size_hint_y = .2  )
        content.add_widget(Label(text='OCF Resource Tool' , font_size = 30))
        self.add_widget(content)

        #second title box
        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1)
        content.add_widget(Label(text='Customize Selected Resource type for ' + self.deviceid , font_size = 20))
        self.add_widget(content)

        #scrollbox
        scroll = ScrollView()
        content = GridLayout(cols = 1 , padding = (10,10) , spacing = (10,10) ,size_hint_y = None  , row_default_height = 35)
        content.bind(minimum_height=content.setter('height'))
        for i in range(len(self.data['mapType']['resourceType'])):
            string1 = self.data['mapType']['resourceType'][i][0]
            string2 = self.data['mapType']['capability'][i][0]
            if self.modf[i][0] == True :
                self.newData["mapType"]["capability"].append(self.data["mapType"]["capability"][i])
                self.newData["mapType"]["resourceType"].append(self.data["mapType"]["resourceType"][i])
                self.newData["mapType"]["resourceHref"].append(self.modf[i][1])
                self.newData["mapData"][string2] =  self.data["mapData"][string2]
            
                if "valueMap" in self.data['mapData'][string2] :
                    minContent = BoxLayout(orientation="horizontal")
                    minContent.add_widget(Label(text = string1 + self.modf[i][1] , size_hint_x = .5 ))
                    content.add_widget(minContent)
                    arr1 = self.data['mapData'][string2]["valueMap"][0]["STValue"]
                    arr2 = self.data['mapData'][string2]["valueMap"][0]["OCFValue"]
                    for j in range(len(arr1)):
                        minContent = BoxLayout(orientation="horizontal")
                        minContent.add_widget(CheckBox())
                        minContent.add_widget(Label(text=arr1[j]))
                        minContent.add_widget(Label(text = "OIC Resource Mapping value"))
                        minContent.add_widget(TextInput(text = str(arr2[j])))
                        content.add_widget(minContent)

        scroll.add_widget(content)
        self.add_widget(scroll)
        
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
        print (json.dumps(self.newData, sort_keys=True, indent=4))
        popup = Popup(title='JSON file',size_hint=(.9, .9))
        popup.content = BoxLayout(orientation="vertical")
        popup.content.add_widget(Label(text="Click Download button to save the updated JSON file in the current folder"))
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