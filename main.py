#!/usr/bin/python
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


import kivy
from kivy.core.window import Window
from kivy.lang import Builder, Parser
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from widgets import *
Builder.load_file('layout-creator.kv')

#class CountingButton(GridLayout):
    #def callback(self, numChange, display):
#take the currently displayed number, change it to an int, add numChange, and make it a string
        #display.text=str(int(display.text)+numChange)

class LayoutCreator(FloatLayout):
    def __init__(self, **kwargs):
        super(LayoutCreator, self).__init__(**kwargs)
        self.rowSize=0 #counter for current width of widgets on the current row
        self.previewedWidgets=[]#list to be filled with all the widgets added
        self.deleteMode=False#when set to true, allows widgets to be deleted on touch
        
    def on_touch_up(self, touch):
        if self.closed and self.deleteMode:#if delete mode is on and the sidebar is closed
            for x in self.previewedWidgets[:]:#loop through the list of widgets
                if x.collide_point(*x.to_widget(*touch.pos,relative=True)):#if you touched a widget,
                    self.rowSize -= x.width #subtract its width from the current row width
                    x.removeSelf()#call its removeSelf method
                    self.previewedWidgets.remove(x)#and remove it from our list of widgets
                    return True
            return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate
        else:#we didn't click on any widgets
            return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate

    def clickEdit(self,widgetToAdd,preview):#preview is the stacklayout that shows the preview
        if widgetToAdd == 'counter':
            self.previewedWidgets.append(Counter(size_hint=(None,None)))
        elif widgetToAdd == 'checkbox':
            self.previewedWidgets.append(YesNo(size_hint=(None,None)))
        preview.add_widget(self.previewedWidgets[-1])
        print preview.size
        print self.rowSize
        
class Test(ScrollView):
    def __init__(self):
        super(Test, self).__init__(size_hint=(None,None),size=(400,400))
        self.layout = GridLayout(cols=1,spacing=10,size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for i in xrange(30):
            btn = Button(text=str(i),size_hint_y=None,height=40)
            self.layout.add_widget(btn)
        self.add_widget(self.layout)

class AppThing(App):
    def build(self):
        self.title="Yazmeen's App"
        return LayoutCreator()

if __name__=='__main__':
    AppThing().run()
