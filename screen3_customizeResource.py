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


class customizeScreen(BoxLayout):

    def __init__(self, did , modif   , **kwargs):
        super().__init__(**kwargs)
        #storing parameter from previous class
        self.deviceid = did
        self.modf = modif
        f = open(f"devices\{self.deviceid}.json")

        #unmodified json data
        self.data = json.load(f)

        #new dictionary to store modified values
        self.newData = {"mapType" : {"capability":[], "resourceType":[],"resourceHref":[]} , "mapData" : {}}
        
        #layout design 
        self.orientation = "vertical"
        self.padding = [20,20,20,20]

        #title box
        content = BoxLayout(orientation = 'horizontal', size_hint_y = .2  )
        content.add_widget(Label(text='OCF Resource Tool' , font_size = 30))
        self.add_widget(content)

        #second title box
        content = BoxLayout(orientation = 'horizontal' , size_hint_y = .1)
        content.add_widget(Label(text='Customize Selected Resource type for ' + self.deviceid , font_size = 20))
        self.add_widget(content)

        #####################scrollbox for customizing items########################
        scroll = ScrollView()
        content = GridLayout(cols = 1 , padding = (10,10) , spacing = (10,10) ,size_hint_y = None  , row_default_height = 35)
        content.bind(minimum_height=content.setter('height'))

        #dictionary to store updated command
        self.updatedCommand = {}
        #dictionary for checkbox to check if command is selected
        self.checkbox = {}

        cnt = 0 
        for i in range(len(self.data['mapType']['resourceType'])):

            resourceType = self.data['mapType']['resourceType'][i][0]
            capability = self.data['mapType']['capability'][i][0]
            
            #only include resources that were previuosly selected
            if self.modf[i][0] == True :

                #store updated values in new dictionary
                self.newData["mapType"]["capability"].append([capability])
                self.newData["mapType"]["resourceType"].append([resourceType])
                self.newData["mapType"]["resourceHref"].append(self.modf[i][1])
                self.newData["mapData"][capability] =  self.data["mapData"][capability]
            
                if "valueMap" in self.data['mapData'][capability] :
                    cnt = cnt + 1
                    #creating layout for commands that need to be customized

                    minContent = BoxLayout(orientation="horizontal")
                    minContent.add_widget(Label(text = resourceType + "   " + self.modf[i][1] ,font_size = 18 ))
                    content.add_widget(minContent)
                    
                    #add the capability in updatedCommand and checkbox
                    self.updatedCommand[capability] = []
                    self.checkbox[capability] = []
                    
                    #data of map Values
                    arr1 = self.data['mapData'][capability]["valueMap"][0]["STValue"]
                    arr2 = self.data['mapData'][capability]["valueMap"][0]["OCFValue"]
                    for j in range(len(arr1)):
                        #layout for each command
                        minContent = BoxLayout(orientation="horizontal")

                        #adding checkbox
                        self.checkbox[capability].append( CheckBox(size_hint_x = .2) )
                        minContent.add_widget(self.checkbox[capability][j])
                        
                        #adding required mapping labels
                        minContent.add_widget(Label(text=arr1[j]))
                        minContent.add_widget(Label(text = "OIC Resource Mapping value"))
                        
                        #adding boxes
                        self.updatedCommand[capability].append(TextInput(text = str(arr2[j]) ))
                        minContent.add_widget(self.updatedCommand[capability][j])
                        content.add_widget(minContent)
        
        if cnt == 0 :
            content.add_widget(Label(text = "There are no resources to be customize",font_size = 30))
            content.add_widget(Label(text = "click on generate button to produce required JSON file"))

        scroll.add_widget(content)
        self.add_widget(scroll)

        ############################################################################

        
        #Generate button and back button
        content  = FloatLayout(size_hint_y = .2)

        back = Button(text = "Back" , size_hint = (.2,.4) , pos_hint = {'x':.3 , 'y' : .4})
        back.bind(on_release =lambda x:self.goBack())
        content.add_widget(back)

        generate = Button(text = "Generate" , size_hint = (.2,.4) , pos_hint = {'x':.5 , 'y' : .4})
        generate.bind(on_release = lambda x:self.generateJSON())
        content.add_widget(generate)

        self.add_widget(content)



    #function to go to previous page
    def goBack(self):
        App.get_running_app().screenManager.transition.direction = 'right' 
        App.get_running_app().screenManager.current = 'resourceScreen'



    #function to open a popup that has option to download modified file
    def generateJSON(self):
        
        ##### update the self.newData with customized command   ######

        for i in range(len(self.data['mapType']['resourceType'])):
            capability = self.data['mapType']['capability'][i][0]
            if (self.modf[i][0] == True) and ("valueMap" in self.data['mapData'][capability]):
                for j in range(len(self.checkbox[capability])) :
                    if self.checkbox[capability][j].active == True:
                        self.newData['mapData'][capability]["valueMap"][0]["OCFValue"][j] = self.updatedCommand[capability][j].text
        
        ###############################################################
        
    
        # adding popup
        popup = Popup(title='JSON file',size_hint=(.9, .9))
        popup.content = BoxLayout(orientation="vertical")
        popup.content.add_widget(Label(text="Click Download button to save the updated JSON file in the current folder"))
        
        #back button
        layout = FloatLayout(size_hint_y = .2)
        button = Button(text=' Close ', size_hint = (.2,.4) , pos_hint = {'x':.3 , 'y' : .4} )
        button.bind(on_press=popup.dismiss)
        layout.add_widget(button)
        
        #download button
        downld = Button(text = "Download" , size_hint = (.2,.4) , pos_hint = {'x':.5 , 'y' : .4})
        downld.bind(on_press = lambda x:self.downloadFile())
        layout.add_widget(downld)
        popup.content.add_widget(layout)
        popup.open()



    #function to download the file in the same folder
    def downloadFile(self):
        with open(f'new_{self.deviceid}.json', 'w') as fp:
            json.dump(self.newData, fp,  indent=2)