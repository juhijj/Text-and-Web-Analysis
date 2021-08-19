'''
In this python file i have implemented  the designed training IF model algorithm
'''
#testing algorithm for IF model

import glob
import string

#to find the average document length
def document_len_average(collection):
    total_length = 0
    for docid,document in collection.get_documents().items():
        total_length = total_length + document.get_documentLength()
    return total_length / collection.documents_number()

#training algorithm for IF model
def w4(collection, benchmark, t):
    P = {}
    for docid, document in collection.get_documents().items():
        if docid not in benchmark:
            continue
        if benchmark[docid] > 0:
            for word,frequency in document.words.items():
                try:
                    P[word] += 1
                except KeyError:
                    P[word] = 1

    Q={}
    for docid,document in collection.get_documents().items():
        for word in document.term_list():
            try:
                Q[word] += 1
            except KeyError:
                Q[word] =1

    total_documents = collection.documents_number()

    R = 0
    for docid,frequency in benchmark.items():
        if benchmark[docid] > 0:
            R += 1

    for docid,r in P.items():
        P[docid] = ((r+0.5)/(R-r+0.5))/((Q[docid]-r+0.5)/(total_documents-Q[docid]-R+r+0.5))

    m = 0
    for docid,r in P.items():
        m += r
    m = m/len(P)

    F = {term: r for term, r in P.items() if r > m + t}
    return F