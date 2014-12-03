#Yazmeen's App, a scouting app for FIRST robotics
#Copyright (C) 2014 Camden County Technical Schools FRC Team 203
#Written by Juliet Summers
# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class _RetrievableText(TextInput):
    def __init__(self,isList,**kwargs):
        super(_RetrievableText,self).__init__(**kwargs)
        self.isList=isList
    def getValue(self):
        if self.isList:
            return self.text.split(',')
        else:
            return self.text

class _CustomBase(GridLayout):
    """The base class for every widget in this module."""
    def __init__(self,**kwargs):
        super(_CustomBase,self).__init__(**kwargs)
        
    def _getInfoDict(self):#overwrite this in subclasses returning a dict of value:type
        pass

    def removeSelf(self):
        self.parent.remove_widget(self)
    
    #XXX work on asking for the info
    #XXX need to fix sizing in the popup
    #XXX DICTIONARIES AREN'T ORDERED AND IT SCREWED EVERYTHING UP FIX THAT
    def askInfo(self):
        close=Button()
        content=StackLayout()
        valueList=[]
        for x,y in self._getInfoDict().iteritems():
            content.add_widget(Label(text=x,size_hint=(None,None),size=(50,50)))
            if y.split()[0]=='text':    #if it's length 1, then it isn't a list
                tmpWidget=_RetrievableText(len(y.split())-1,multiline=False,size_hint=(None,None),
                        size=(50,50))
                valueList.append(tmpWidget.getValue)
                content.add_widget(tmpWidget)
            elif y.split()[0]=='int':
                tmpWidget=_RetrievableText(len(y.split())-1,multiline=False,input_type='number',
                        size_hint=(None,None),size=(50,50))
                valueList.append(tmpWidget.getValue)
                content.add_widget(tmpWidget)
        content.add_widget(close)
                
        askPane=Popup(title='Get Info',content=content,#i hope it doesn't break on attempting to call
                auto_dismiss=False,on_dismiss=lambda x: self._setInfo(valueList))#functions in valueList
        close.bind(on_release=askPane.dismiss)                         #after askPane's been closed
        askPane.open()
        
        #self.askPane.add_widget(Button(text='if you see this then it might be working',
            #on_release=lambda x: self.setInfo()))
        return valueList
        
    def _setInfo(self,valueList):#overwrite this in the subclass using expected values
        pass

class Counter(_CustomBase):
    """A counter widget to be used with Yazmeen's App. Label is what the counter will be labelled
       as, and numList is a list of integers used for the increase/decrease buttons."""
    def __init__(self,**kwargs):#label,numList,**kwargs):
    #50 is a good size for the buttons, so the width should be the number of buttons * 50
        self.label=Label(size_hint_y=None, height=40)
        self.display=Label(text='0',size_hint_y=None, height=40)
        self.counters=GridLayout(rows=2,size_hint_y=None, height=120)
        self.askInfo()
        super(Counter, self).__init__(rows=3,col_force_default=True,height=200,**kwargs)
            #col_default_width=len(numList)*50,width=len(numList)*50,height=200,**kwargs)
        #create all subwidgets
        
        #loop over numList to add the inc/dec buttons
        #for x in numList:
            #self.counters.add_widget(Button(text='+%i'%x,on_release=lambda z,w=x:self.update(w)))
        #for x in numList:
            #self.counters.add_widget(Button(text='-%i'%x,on_release=lambda z,w=-x:self.update(w)))
        #add the subwidgets
        self.add_widget(self.label)
        self.add_widget(self.display)
        self.add_widget(self.counters)
        
    def _getInfoDict(self):
        return {'Label':'text','Buttons':'int list'}
    
    def _setInfo(self,valueList):
        self.col_default_width=len(valueList[1]())*50
        self.width=len(valueList[1]())*50
        self.label.text=valueList[0]()
        self.counters.cols=len(valueList[1]())
        for x in valueList[1]():
            self.counters.add_widget(Button(text='+%i'%int(x),on_release=lambda z,w=int(x):self.update(w)))
        for x in valueList[1]():
            self.counters.add_widget(Button(text='-%i'%int(x),on_release=lambda z,w=-int(x):self.update(w)))
    
    def update(self,change):
        #take the current value, make it an int, add change to it, and turn the new value to a str
        self.display.text=str(int(self.display.text)+change)
