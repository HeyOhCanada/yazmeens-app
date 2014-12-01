#!/usr/bin/python
#Yazmeen's App, a scouting app for FIRST robotics
#Copyright (C) 2014 FRC Team 203
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
from widgets import Counter
Builder.load_file('layout-creator.kv')

#class CountingButton(GridLayout):
    #def callback(self, numChange, display):
#take the currently displayed number, change it to an int, add numChange, and make it a string
        #display.text=str(int(display.text)+numChange)

class LayoutCreator(PageLayout):
    def __init__(self, **kwargs):
        super(LayoutCreator, self).__init__(**kwargs)
        self.previewedWidgets=[]#list to be filled with all the widgets added
        self.deleteMode=False#when set to true, allows widgets to be deleted on touch
    def on_touch_up(self, touch):
        if self.page: #page is 0 if the thing is closed, 1 if open
            if Widget(pos=(51.2, 0), size=(51.2,768)).collide_point(*touch.pos):#position when open
                self.page=0
                return True #clicked on the button; swallow the touch
            else:
                return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate
        else: #page is closed
            if Widget(pos=(972.8,0), size=(51.2,768)).collide_point(*touch.pos):#position when closed
                self.page=1
                return True #clicked on the button; swallow the touch
            elif self.deleteMode:#if page is closed and delete mode is on and the button wasn't clicked
                for x in self.previewedWidgets[:]:#loop through the list of widgets
                    if x.collide_point(*touch.pos):#if you touched a widget,
                        x.removeSelf()#call its removeSelf method
                        self.previewedWidgets.remove(x)#and remove it from our list of widgets
                        return True
                return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate
            else:#we didn't click on any widgets or the button
                return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate

    def clickEdit(self,widgetToAdd,preview):#preview is the stacklayout that shows the preview
        if widgetToAdd == 'counter':
            self.previewedWidgets.append(Counter('test',[1,7,10],size_hint=(None,None)))
            preview.add_widget(self.previewedWidgets[-1])
    
    def removePreview(self,toRemove,preview):
        preview.remove_widget(self.previewedWidgets[toRemove])

class AppThing(App):
    def build(self):
        self.title="Yazmeen's App"
        return LayoutCreator()

if __name__=='__main__':
    AppThing().run()
