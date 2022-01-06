import os
import sys
import string
import json
from tkinter import *
from shuntingyard_implement import *

dictionary = json.load(open("dictionary.json"))
postings = json.load(open("posting_lists.json"))







### GUI section start  
root = Tk()
root.geometry("800x600")
root.title("Search box")
  
def Take_input():
    INPUT = input_text.get("1.0", "end-1c")
    output.delete('1.0', END)
    a = "yes"
    output.insert(END, a)
    #check later
      
label = Label(text = "Input your search query")
input_text = Text(root, height = 1,
                width = 50,
                bg = "light yellow",
                font=("Arial", 10)
                )
  
output = Text(root, height = 30, 
              width = 50, 
              bg = "light cyan",
              font=("Arial", 10),
              )
  
display = Button(root, height = 1,
                 width = 20, 
                 text ="Show",
                 command = lambda:Take_input())
  
label.pack()
input_text.pack()
display.pack()
output.pack()
  
mainloop()
###GUI section end
