import os
import sys
import string
import json
import re
from nltk.corpus import stopwords
from glob import glob
from ast import literal_eval

word_dictionary_dict = {}
word_posting_dict = {}

# Build Inverted-Index for documents
path = os.getcwd() + '\\processed_data\\'
path2 = os.getcwd()
docids = json.load(open("docids.json"))

def init_dict_posting():
    i = 1
    for filename in glob(os.path.join(path, '*.txt')):
        filename_read = open(filename, 'r').read()
        data = literal_eval(filename_read)
        for x in data:
            word_dictionary_dict.update({
                x[0]: {
                    "frequency": 0,
                    "ID": 0
                }
            })
    for key, value in word_dictionary_dict.items():
        value["ID"] = i 
        i+=1
    for value in word_dictionary_dict.values():
        word_posting_dict.update({
            value["ID"]: {}
        })
        

def update_dict_postings():
    for filename in glob(os.path.join(path, '*.txt')):
        filename_read = open(filename, 'r').read()
        data = literal_eval(filename_read)
        for x in data:
            #dict
            if x[0] in word_dictionary_dict:
                word_dictionary_dict[x[0]]["frequency"] +=1

            #posting
            k = word_dictionary_dict[x[0]]["ID"]
            fn = os.path.splitext(os.path.basename(filename))[0]
            word_posting_dict[k].update({
                "%s" % docids[fn]: x[1]
            })

init_dict_posting()
update_dict_postings()

with open(os.path.join(path2, "dictionary.json"), 'w') as outfile:
    json.dump(word_dictionary_dict, outfile)
with open(os.path.join(path2, "posting_lists.json"), 'w') as outfile:
    json.dump(word_posting_dict, outfile)
