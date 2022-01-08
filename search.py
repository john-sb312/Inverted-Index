import json
import os
from typing import List
from tkinter import *
from nltk.tokenize import word_tokenize
from typing import List
from shuntingyard_implement import *

dictionary_list = json.load(open("dictionary.json"))
posting_list = json.load(open("posting_lists.json"))

def perform_AND(left: List[int], right: List[int]) -> List[int]:
    result = []
    for element in left:
        if element in right:
            result.append(element)
    return result


def perform_OR(left: List[int], right: List[int]) -> List[int]:
    result = []
    result = list(set(left) | set(right))
    return result


def perform_NOT(exclude: List[int], docids) -> List[int]:
    result = list(docids.difference(set(exclude)))
    result.sort(key=lambda x: '{0:0>8}'.format(x))
    return result


def search_function(query):
    while True:        
        if query.lower() == "exit":
            break

        tokens = word_tokenize(query)

        i = 0
        while i < len(tokens) - 1:
            if is_term(tokens[i]) and is_term(tokens[i+1]):
                tokens.insert(i+1, "AND")
            i += 1

        # convert to Reverse Polish notation
        rpn = ShuntingYard(tokens).get_RPN()

        stack = []

        for token in rpn:
            if token not in operators:
                # get documents for term using index (or [] if term not found)
                if token in dictionary_list:
                    id = dictionary_list[token]["ID"]
                    documents = []
                    for key in posting_list["%s" % id].keys(): documents.append(key)
                    documents.sort(key=lambda x: '{0:0>8}'.format(x))
                else:
                    documents = []
                stack.append(documents)
            else:
                if token == "AND":
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    stack.append(perform_AND(left_operand, right_operand))
                elif token == "OR":
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    stack.append(perform_OR(left_operand, right_operand))
                elif token == "NOT":
                    operand = stack.pop()
                    stack.append(perform_NOT(operand, all_document_ids))

        stack[0].sort(key=lambda x: '{0:0>8}'.format(x))
        return (len(stack[0]), stack[0])



### GUI section start  
root = Tk()
root.geometry("800x600")
root.title("Search box")
  
def Take_input():
    INPUT = input_text.get("1.0", "end-1c")
    output.delete('1.0', END)
    
    OUTPUT = search_function(INPUT)
    output.insert(END, OUTPUT)
      
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