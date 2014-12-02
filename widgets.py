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

class CustomBase(GridLayout):
    """The base class for every widget in this module."""
    def __init__(self,**kwargs):
        super(CustomBase,self).__init__(**kwargs)

    def removeSelf(self):
        self.parent.remove_widget(self)
    
    #XXX work on asking for the info
    #def askInfo(self, infoDict):
        #self.askPane=StackLayout()
        #valueList=[]
        #for x in infoDict.keys():
            #self.askPane.add_widget

class Counter(CustomBase):
    """A counter widget to be used with Yazmeen's App. Label is what the counter will be labelled
       as, and numList is a list of integers used for the increase/decrease buttons."""
    def __init__(self,label,numList,**kwargs):
    #50 is a good size for the buttons, so the width should be the number of buttons * 50
        super(Counter, self).__init__(rows=3,col_force_default=True,
            col_default_width=len(numList)*50,width=len(numList)*50,height=200,**kwargs)
        #create all subwidgets
        self.label=Label(text=label,size_hint_y=None, height=40)
        self.display=Label(text='0',size_hint_y=None, height=40)
        self.counters=GridLayout(cols=len(numList),rows=2,size_hint_y=None, height=120)
        #loop over numList to add the inc/dec buttons
        for x in numList:
            self.counters.add_widget(Button(text='+%i'%x,on_release=lambda z,w=x:self.update(w)))
        for x in numList:
            self.counters.add_widget(Button(text='-%i'%x,on_release=lambda z,w=-x:self.update(w)))
        #add the subwidgets
        self.add_widget(self.label)
        self.add_widget(self.display)
        self.add_widget(self.counters)
    
    def update(self,change):
        #take the current value, make it an int, add change to it, and turn the new value to a str
        self.display.text=str(int(self.display.text)+change)
