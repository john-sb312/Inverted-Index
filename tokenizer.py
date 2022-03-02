import os
import sys
import string
import json
from nltk.corpus import stopwords
from collections import defaultdict
from glob import glob



def word_split(text):
    """
    Function này để tách từ, load nó vào list word_list theo dạng tuple ở trong list
    [(từ 1, vị trí 1), (từ 2, vị trí 2)]
    đoạn sơ khai nhất nằm ở đây
    """
    word_list = []
    word_current = []
    word_index = None
    for i, c in enumerate(text):
        if c.isalnum():
            word_current.append(c)
            word_index = i
        elif word_current:
            word = u''.join(word_current)
            word_list.append((word, word_index - len(word) + 1))
            word_current = []
    if word_current:
        word = u''.join(word_current)
        word_list.append((word, word_index - len(word) + 1))
    return word_list

def words_cleanup(words):
    """
    Function loại bỏ từ thừa trong bộ từ điển có sẵn của nltk và loại bỏ tất cả các thể loại từ dưới 3 chữ cái
    """
    stop_words = set(stopwords.words("english"))
    cleaned_words = []
    for word, index in words:
        if len(word) < 3 or word in stop_words:
            continue
        cleaned_words.append((word, index))
    return cleaned_words

def words_normalize(words):
    """
    Function để biến chữ Hoa thành chữ thường
    """
    normalized_words = []
    for word, index in words:
        word_normalized = word.lower()
        normalized_words.append((word_normalized, index))
    return normalized_words

def words_duplication(words):
    '''
    '''
    duplication_words = defaultdict(list)
    for word, index in words:
        duplication_words[word].append(index)
    return sorted(duplication_words.items())

def word_index(text):
    #Function này gọi tất cả những function trên
    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words)
    words = words_duplication(words)
    return words


def helper_method():
    '''
    Function này lấy tất cả file txt có trong folder raw data của thư mục hiện tại
    folder chứa file tokenize.py phải có folder con raw_data và processed_data và raw_data phải chứa dữ liệu dạng txt 
    Sau khi xử lý xong nội dung của các file tương ứng sẽ được lưu và giữ nguyên tên tại processed_data
     '''
    path1 = os.getcwd() + '\\raw_data\\'
    path2 = os.getcwd() + '\\processed_data\\'
    docids = {}
    i = 0
    for filename in glob(os.path.join(path1, '*.txt')):
        i +=1
        read_content = open(filename, 'r', encoding='utf-8').read().split('\n')
        doc_content = ''.join(map(str, read_content))
        doc = word_index(doc_content)
        f = open(os.path.join(path2, os.path.basename(filename)), 'w')
        f.write(str(doc))
        
        docids[os.path.basename(filename)] = i
        with open(os.path.join(os.getcwd(), "docids.json"), 'w') as outfile:
            json.dump(docids, outfile)
helper_method()