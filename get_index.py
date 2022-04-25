import os
from tkinter import filedialog
from tkinter import *
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import re

# root path to the current python script location
abspath = os.path.abspath(__file__)
root = os.path.dirname(abspath)
os.chdir(root)


def get_folder():
    """
    open a GUI to pick the folder of the documents
    :return: the absolute path of the folder
    """
    root = Tk()
    root.withdraw()
    # method in fieldialog to get the directory path
    folder_path = ""
    folder_path = filedialog.askdirectory()
    return folder_path


def get_docDict(path):
    doc_dict = {}
    file_names = os.listdir(path)

    for file in file_names:
        full_path = path + '/' + file
        with open(full_path, 'r', errors='ignore') as f:
            data = f.readlines()
        text = "".join([i for i in data])
        # removes all the "\n" from the text by regex, the re.sub() method
        text = re.sub("\n", " ", text)
        doc_dict[file] = text
    return doc_dict


def clean_text(doc_dict):
    clean_dict = {}
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')

    for name, doc in doc_dict.items():
        text = ""
        # remove extra white space
        text = re.sub(r"\s+", " ", doc)
        # remove extra ...
        text = re.sub(r"\.+", " ", doc)
        # remove hyphen
        text = re.sub(r"-", "", text)
        # convert all letters into lowercase
        text = text.lower()
        text_tokens = []
        # tokenize the text string
        text_tokens = word_tokenize(text)
        text_clean = []

        for word in text_tokens:
            # stem the tokens
            if word not in stopwords_english and word not in string.punctuation:
                stem_word = stemmer.stem(word)
                text_clean.append(stem_word)
        clean_dict[name] = text_clean

    return clean_dict


def corpus_tokenize(doc_dict):
    """
    convert the whole document collection as list of lists of tokens
    :param doc_dict: the clean document dict
    :return: the list of lists of doc tokens
    """
    doc_list = []

    for name, doc in doc_dict.items():
        doc_list.append(doc)
    return doc_list


def build_ranker():
    bm25_ranker = None
    doc_dict = None
    # get the folder path of the document collection
    folder_path = get_folder()
    # document dict
    doc_dict = get_docDict(folder_path)
    # clean the document dict
    clean_dict = clean_text(doc_dict)
    # tokenize the whole corpus
    doc_tokens = corpus_tokenize(clean_dict)
    # create the BM25 ranker object
    bm25_ranker = BM25Okapi(doc_tokens)
    return bm25_ranker, doc_dict
