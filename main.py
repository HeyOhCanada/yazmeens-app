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


#PABLO THE PYTHON!!!

#                    uJ$$$$$$',J <$$h.                  .,J+.
#                 ,J$$$$$$$"z$F,J$$??$$h- =<$$C$$$>-.zJ"J?? $$ccc,.
#               .r$$$$$$$$$$$$$$$$$F "?$$$hJ$$$$$'zJ$$$P" ,$z$$P$$F$hu
#              J$h?$$$$$$$$$$$$$$$$$$$. ``$$$$$$$$$$$"" ,J$x$$$<$$L$$$N
#            .P$$$$F"""   ' `"??$$$h?$$$ucd$$$$$$$$$hcr$P"J?$$P""??$Lc$F
#            J$JF                `?$C`?$$$$$$"$"$$$$$$P",JP"       `$$$F
#            ?$F                   `?h..`"?$$$$$$$F" .,zP           $$$$
#            cc         u  ..        `$$P   `""""  J$$"   -c    "   $$$F
#            ?F       ,$ z$$$,ccu.,.  `?$h        ,J$'.    $    .  ,$$F
#            ;h       ????$$$$$$$$$$$u   "h. p"  u$" JF   =     " ;PP"
#           `?      <$hcr. `"""????$$r   `;d"  ,$" `"           JP"
#             $r      $$$$$$$$$$hccccc   ,P",, ,P" J$$$       .P"
#              ?      """""""???"      ,p"   """  J$$P"     >'
#               `c     hcc,,.      -=="F          "      uF
#                `=    `?$$$$-<$$h    j'      .,J$$$  .'"
#                  `\.    ""?h.`$$$C  "     z$$$P"   $$"
#                     "  .   .`""""""     ,cL..,,,cc,h
#                       `"$h,`$$$$$F ?$C `$$$$$$$$""<$
#                          "?hu`"?$$F $$h. `???"  .. ?
#                             "?hu cccccccccd$$$$$$$$
#                                "?h."$$$$$$$$$$????"
#                                  `?hu` zccccccd$$$$$$u
#                                        `?h.' .;ccccd$$$$$c
#                                           "$h."$$$$$$$$$$$$c
#                                             "$h.?$$$??????""
#                           .,zcccccccccccu.   `?$u ,cc$$$$$$$$$c
#             ,cc$$$P",cd$$$$$$$$$$$$P"""".zc$$$,?$h $$$$$$$$$$$$.
#         ,J$$$$P",cd$$$$$$$$??"".,ccd$$$$$$$$$$$ $$h`"""""".,,,,,
#h      ;J$$$P",c$$$$$$?"",ccc$$$$$$$$$$$$$$$$$$$ $$$ $$$$$$$$$$$$
#`$    x$$?",d$$$$?",cd$$$$$$$$$$$$$$$$$P". .  .`;$$',$$$$$$$$$$$F;,
# ?h.__,zc$$??",cd$$$$$$$$$$$$$$$$$P" zc<$$'$F',J$$F,cccccccccccc J$$$u
#  `"""""",zc$$$$$$$$$$$$$$$$$P"",;J$r"" ",uccd$$$F J$$$$$$$$$$P J$$$$$h
#      `$$$$$$$$$$$$$$$$$??",zc $$F .uJ$$$$$$$$$P'..""""""""""",$$$$$$$$
#        "?$$$$$$$??""",cr$$??""'c$$$$$$$$$$$$P" <$$$$$$$$$$",J$$$$$$$P"
#                `"`?? ??"      `"?$$$$$$$$$",ccc,.```"???".,c,""?CLz>
#                                    "??""' J$$$$$$$$$$"  ?????????"

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
from ConfigParser import ConfigParser
from widgets import *
Builder.load_file('layout-creator.kv')
class LayoutCreator(FloatLayout):
    def __init__(self, **kwargs):
        super(LayoutCreator, self).__init__(**kwargs)
        self.rowSize=0 #counter for current width of widgets on the current row
        self.previewedWidgets=[]#list to be filled with all the widgets added
        self.deleteMode=False#when set to true, allows widgets to be deleted on touch
        self.config = ConfigParser()

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
        elif widgetToAdd == 'textbox':
            self.previewedWidgets.append(TextBox(size_hint=(None,None)))
        preview.add_widget(self.previewedWidgets[-1])

class AppThing(App):
    def build(self):
        self.title="Yazmeen's App"
        return LayoutCreator()

if __name__=='__main__':
    AppThing().run()
