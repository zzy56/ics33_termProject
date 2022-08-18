import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Gui(tk.Tk):

    def __init__(self, width, height):
        super().__init__()
        self.title('title')
        self.geometry(str(width)+"x"+str(height))
        self.resizable(0, 0)
        self.labels = []
        #self.strings = []
        self.buttons = []

    def createButton(self, nOfButtons):
        for i in range(nOfButtons):
            newButton = ttk.Button(self, text="newButton", command=None)
            self.buttons.append(newButton)
    
    def createLabel(self, nOfNewLabels):
        for i in range(nOfNewLabels):
            newLabel = ttk.Label(self, text = "newLabel", relief=FLAT)
            self.labels.append(newLabel)

    def getButton(self, index):
        return self.buttons[index]
    def getLabel(self, index):
        return self.labels[index]

    def showIndex(self):
        for i in range(len(self.labels)):
            self.labels[i].config(text=str(i))
        for i in range(len(self.buttons)):
            self.buttons[i].config(text=str(i))

    def doNothing_CallBack(self):
        pass

    def showMsg_CallBack(self):
        messagebox.showinfo("message")

    def setUp(self):

        self.createButton(5)
        self.createLabel(6)

        l1 = app.getLabel(0)
        l1.config(text = "Texas Hold'em", font=("Arial", 25))
        l1.place(relx = 0.5, rely = 0.1, anchor = CENTER)

        l2 = app.getLabel(1)
        l2.config(text = "-----Game 1-----")
        l2.place(relx = 0.5, rely = 0.15, anchor = CENTER)

        l3 = app.getLabel(2)
        l3.config(text = "-----Round 1-----")
        l3.place(relx = 0.5, rely = 0.2, anchor = CENTER)

        l4 = app.getLabel(3)
        l4.config(text = "Player's Hand: ")
        l4.place(relx = 0.5, rely = 0.25, anchor = CENTER)

        b = app.getButton(0)
        b.config(command = self.showMsg_CallBack)
        b.config(text = "confirm")
        b.place(relx = 0.5, rely = 0.9, anchor = CENTER)


        betCheckBox = ttk.Checkbutton(app, text='bet')
        betCheckBox.place(relx = 0.5, rely = 0.85, anchor = CENTER)
    

app = Gui(800, 600)
app.setUp()
#app.showIndex()
app.mainloop()

