# entry_example.py
from tkinter import *

class EntryDemo:
  def __init__(self, rootWin):
    #Create a entry and button to put in the root window!
    self.entry = Entry(rootWin)
    #Add some text:
    self.entry.delete(0,END)
    self.entry.insert(0, "Change this text!")
    self.entry.pack()

    self.button = Button(rootWin, text="Click Me!", command=self.clicked)
    self.button.pack()



  def clicked(self):
    print("Button was clicked!")
    eText = self.entry.get()
    print("The Entry has the following text in it:", eText)


#Create the main root window, instantiate the object, and run the main loop!
rootWin = Tk()
app = EntryDemo( rootWin )
rootWin.mainloop()