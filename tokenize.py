import os
from nltk.corpus import stopwords
import sys
from glob import glob
import string

def word_split(text):

    word_list = []
    word_current = []
    word_index = None

    for i, c in enumerate(text):
        if c.isalnum():
            word_current.append(c)
            word_index = i
        elif word_current:
            word = u''.join(word_current)
            word_list.append((word_index - len(word) + 1, word))
            word_current = []

    if word_current:
        word = u''.join(word_current)
        word_list.append((word_index - len(word) + 1, word))

    return word_list

def words_cleanup(words):

    stop_words = set(stopwords.words("english"))
    cleaned_words = []
    for index, word in words:
        if len(word) < 3 or word in stop_words:
            continue
        cleaned_words.append((index, word))
    return cleaned_words

def words_normalize(words):

    normalized_words = []
    for index, word in words:
        word_normalized = word.lower()
        normalized_words.append((index, word_normalized))
    return normalized_words

def word_index(text):
    #helper method; process text
    
    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words)
    return words


def helper_method():
    path1 = os.getcwd() + '\\raw_data\\'
    path2 = os.getcwd() + '\\processed_data\\'
    contents = []
    for filename in glob(os.path.join(path1, '*.txt')):
        read_content = open(filename, 'r', encoding='utf-8', errors="surrogateescape").read().split('\n')
        doc_content = ''.join(map(str, read_content))
        doc = word_index(doc_content)
        f = open(os.path.join(path2, os.path.basename(filename)), 'w')
        f.write(str(doc))
        
helper_method()