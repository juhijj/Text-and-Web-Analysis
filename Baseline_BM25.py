'''
In this python file i have implemented a baseline Bm25 model
'''


import math
from porter2 import stem
import string
import os
import glob

#to find the average document length
def document_len_average(collection):
    total_length = 0
    for docid,document in collection.get_documents().items():
        total_length = total_length + document.get_documentLength()
    return total_length / collection.documents_number()

#to calculate the bm25 score
def bm25_baseline(collection,query,df):
    q = query.translate(str.maketrans('','',string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    sw = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/common-english-words.txt', 'r')
    sw_ = sw.read().split(',')
    score_BM25 = {}
    average_doclength = document_len_average(collection)
    total_docs = collection.documents_number()
    for docid, document in collection.get_documents().items():
        query_word = q.split()
        query_frequency = {}
        for term in query_word:
            t = stem(term.lower())
            if len(t)>2 and t not in sw_:
                try:
                    query_frequency[t]+=1
                except:
                    query_frequency[t] = 1
        k = 1.2 * ((1-0.75) + 0.75 * (document.get_documentLength()/float(average_doclength)))
        bm25 = 0

        for query_term in query_frequency.keys():
            n=0
            R=0
            r=0
            if query_term in df.keys():
                n=df[query_term]
                f = document.word_count(query_term)
                qf = query_frequency[query_term]

                bm  = math.log(1.0/((n+0.5)/(total_docs - n +0.5)),2) * (((1.2+1)*f)/(k+f)) * (((100+1) * qf) / float(100+qf))
                bm25 += bm
        score_BM25[document.docId()] = bm25
    # print(score_BM25)
    return  score_BM25

