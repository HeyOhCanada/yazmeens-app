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
from kivy.uix.togglebutton import ToggleButton
from string import whitespace

class _RetrievableText(TextInput):
    """TextInput that has a getValue function to, well, get its value. Inputs that should be lists
        must be separated by commas without spaces."""
    def __init__(self,isList,autoNewline=False,**kwargs):
        super(_RetrievableText,self).__init__(**kwargs)
        self.isList=isList

        if autoNewline: #only define this function if automatic newlines are desired
            def insert_text(substring,from_undo=False):#max cols 10
                if self.cursor_col+len(substring) > 10:
                    space=substring.rfind(whitespace)
                    if space != -1: #rfind returns -1 when not found
                        return super(_RetrievableText,self).insert_text(
                            substring[:space]+'\n'+substring[space+1:],from_undo=from_undo)
                    else:
                        return super(_RetrievableText,self).insert_text('\n'+substring,
                            from_undo=from_undo)
                else:
                    return super(_RetrievableText,self).insert_text(substring, from_undo=from_undo)
            self.insert_text=insert_text

    def getValue(self):
        if self.isList:
            return self.text.split(',')
        else:
            return self.text

class _CustomBase(GridLayout):
    """The base class for every widget in this module."""
    def __init__(self,**kwargs):
        super(_CustomBase,self).__init__(**kwargs)

    def removeSelf(self):
        self.parent.remove_widget(self)

    def askInfo(self,requiredInfo):
        #the button size is wrong on my laptop but right on the tablet so
        close=Button(text='Add')
        cancel=Button(text='Cancel')

        buttonGrid=GridLayout(cols=2,size_hint_y=.5)
        buttonGrid.add_widget(close)
        buttonGrid.add_widget(cancel)
        content=StackLayout(spacing=5)
        valueList=[]#empty list that gets filled with the inputs' getValue functions
        for x,y in requiredInfo:
            content.add_widget(Label(text=x,size_hint=(None,None),size=(50,32)))

            if y.split()[0]=='text':    #v if it's length 1, then it isn't a list
                tmpWidget=_RetrievableText(len(y.split())-1,multiline=False,size_hint=(None,None),
                        write_tab=False,size=(100,32))
                #^ height 32 bc font size defaults to 10 and y padding defaults to 12
                valueList.append(tmpWidget.getValue)
                content.add_widget(tmpWidget)

            elif y.split()[0]=='int':
                tmpWidget=_RetrievableText(len(y.split())-1,multiline=False,input_type='number',
                        write_tab=False,size_hint=(None,None),size=(100,32))
                #^ height 32 bc font size defaults to 10 and y padding defaults to 12
                valueList.append(tmpWidget.getValue)
                content.add_widget(tmpWidget)
        #buttonGrid.height=.5*content.height #size_hint_y=.5 should do this but i guess not
        content.add_widget(buttonGrid)
        self.askPane=Popup(title='Get Info',content=content,size_hint=(.5,None),
            height=1.5*content.height,
                auto_dismiss=False,)#on_dismiss=lambda x: self._setInfo(valueList))
        close.bind(on_release=lambda x: self._setInfo(valueList,False))#askPane.dismiss)
        cancel.bind(on_release=lambda x: self._setInfo(valueList,True))
        self.askPane.open()

    def _setInfo(self,valueList):#overwrite this in the subclass using expected values
        pass

    def _cancelled(self):#call when cancelled is true in _setInfo
        self.parent.parent.parent.previewedWidgets.remove(self)
        self.removeSelf()

    def _addHeight(self):
        if self.parent.parent.parent.rowSize+self.width >= 1024:
            self.parent.height+=210
            self.parent.parent.parent.rowSize = self.width
        else:
            self.parent.parent.parent.rowSize+=self.width

class Counter(_CustomBase):
    """A counter widget to be used with Yazmeen's App. Label is what the counter will be labelled
       as, and numList is a list of integers used for the increase/decrease buttons."""
    def __init__(self,**kwargs):
        #create subwidgets

        self.label=Label(size_hint_y=None, height=40,halign='center',split_str=' ')
        self.display=Label(text='0',size_hint_y=None, height=40)
        self.counters=GridLayout(rows=2,size_hint_y=None, height=120)

        self.askInfo((('Label','text'),('Buttons','int list')))


        super(Counter, self).__init__(size_hint_y=None,rows=3,
            col_force_default=True,height=200,**kwargs)

    def _setInfo(self,valueList,cancelled):
        if cancelled:
            self._cancelled()
            self.askPane.dismiss()
            return None #return to exit the function
        for x in valueList:
            if x() == '':
                #add a more descriptive message later
                Popup(title='Error',content=Label(text='Empty value'),size_hint=(.5,.5)).open()
                return True #returning true prevents the popup from closing

        for x in valueList[1]():#may not need this, check the tablet keyboard, consider keeping it tho
            if not x.isdigit():
                #add a more descriptive message later
                Popup(title='Error',content=Label(text='Invalid integer'),size_hint=(.5,.5)).open()
                return True #not a number, don't close

        self.askPane.dismiss()

        #50 is a good size for the buttons, so the width should be the number of buttons * 50
        self.col_default_width=len(valueList[1]())*50
        self.width=len(valueList[1]())*50
        self.label.text_size=(len(valueList[1]())*50,40)
        self.label.text=valueList[0]()
        self.counters.cols=len(valueList[1]())
        for x in valueList[1]():
            self.counters.add_widget(Button(text='+%i'%int(x),
                on_release=lambda z,w=int(x):self.update(w)))
        for x in valueList[1]():
            self.counters.add_widget(Button(text='-%i'%int(x),
                on_release=lambda z,w=-int(x):self.update(w)))

        #add the subwidgets
        self.add_widget(self.label)
        self.add_widget(self.display)
        self.add_widget(self.counters)

        self._addHeight()
        #i wish i could do this a better way but i can't be bothered to think of it
        #if self.parent.parent.parent.rowSize+self.width >= 1024:
            #self.parent.height+=210
            #self.parent.parent.parent.rowSize = self.width
        #else:
            #self.parent.parent.parent.rowSize+=self.width

    def update(self,change):
        #take the current value, make it an int, add change to it, and turn the new value to a str
        self.display.text=str(int(self.display.text)+change)

class YesNo(_CustomBase):
    def __init__(self,**kwargs):
        super(YesNo, self).__init__(size_hint_y=None,rows=2,height=200,**kwargs)
        self.label=Label(size_hint_y=None,height=100,text_size=(100,100),halign='center',split_str=' ')
        self.checkbox=ToggleButton(text='NO',size_hint_y=None,height=100)
        self.checkbox.bind(state=lambda x,y: self.setText())

        self.askInfo((('Label','text'),))

    def _setInfo(self,valueList,cancelled):
        if cancelled:
            self._cancelled()
            self.askPane.dismiss()
            return None #exit the function
        if valueList[0]() == '':
            #add a more descriptive message later
            Popup(title='Error',content=Label(text='Empty value'),size_hint=(.5,.5)).open()
            return None #exit without closing the first popup

        self.label.text=valueList[0]()
        self.add_widget(self.label)
        self.add_widget(self.checkbox)
        self.askPane.dismiss()

        self._addHeight()
        #i wish i could do this a better way but i can't be bothered to think of it
        #if self.parent.parent.parent.rowSize+self.width >= 1024:
            #self.parent.height+=210
            #self.parent.parent.parent.rowSize = self.width
        #else:
            #self.parent.parent.parent.rowSize+=self.width

    def setText(self):
        if self.checkbox.text == 'YES':
            self.checkbox.text = 'NO'
        else:
            self.checkbox.text = 'YES'

class TextBox(_CustomBase):
    def __init__(self, **kwargs):
        super(TextBox, self).__init__(rows=2, height=200, **kwargs)
        self.label=Label(height=50,text_size=(100,50),halign='center',split_str=' ')
        self.input=_RetrievableText(False,autoNewline=True)
        self.askInfo((('Label','text'),))

    def _setInfo(self,valueList,cancelled):
        if cancelled:
            self._cancelled()
            self.askPane.dismiss()
            return None #exit the function
        if valueList[0]() == '':
            #add a more descriptive message later
            Popup(title='Error',content=Label(text='Empty value'),size_hint=(.5,.5)).open()
            return None #exit without closing the first popup

        self.label.text=valueList[0]()
        self.add_widget(self.label)
        self.add_widget(self.input)
        self.askPane.dismiss()

        self._addHeight()
