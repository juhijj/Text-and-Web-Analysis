'''
This python file is created to calculate the TF-IDF score
'''
import preprocess
import math
from porter2 import stem
import string
import os
import glob

#calculate document frequency in provided all documents
def df(collection):
    df_ = {}
    for docid, document in collection.get_documents().items():
        for word in document.term_list():
            try:
                df_[word]+=1
            except KeyError:
                df_[word] = 1
    return df_

#calculate document frequency for individual document
def document_df(document):
    df_ = {}
    doc_words = document.term_list()
    for word in doc_words:
        try:
            df_[word] +=1
        except KeyError:
            df_[word] = 1
    return df_

#calculate td-idf score
def tfIdf(collection):
    word_weight = {}
    doc_freq  =df(collection)
    for docid, document in collection.get_documents().items():
        term_frequency = document_df(document)
        term_w = {}
        norm  = 0
        for word, score in term_frequency.items():
            tf = 1+math.log(score)
            idf = math.log(collection.documents_number()/doc_freq[word])

            term_w[word] = (tf *idf)
            norm+=((tf*idf)**2)
        norm = math.sqrt(norm)
        for t,w in term_w.items():
            term_w[t] = w/norm
        word_weight[docid] = term_w
    return word_weight

