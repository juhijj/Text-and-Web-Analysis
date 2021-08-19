'''
This algorithm is implemented to identify the complete training set.
'''

import math
from porter2 import stem
import string
import os
import glob
import documentFrequency

#to calculate the cosine measure score
def CosineMeasure(collection,query):
    cosine_score = {}
    score_df = documentFrequency.tfIdf(collection)
    sw = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/common-english-words.txt', 'r')
    sw_ = sw.read().split(',')
    for docid, document in collection.get_documents().items():
        qf = {}
        for word in query.split():
            word = word.translate(str.maketrans('', '', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            word = stem(word.lower()).strip()
            if len(word) > 2 and word not in sw_:
                try:
                    qf[word] += 1
                except KeyError:
                    qf[word] = 1

        vector1 = 0
        vector2 = 0
        nm = 0
        for qw in qf:
            if qw in score_df[docid]:
                nm += qf[qw]*score_df[docid][qw]
        for k, v in score_df[docid].items():
            vector1 += v**2
        for k, v in score_df[docid].items():
            vector2 += v**2
        denominator = math.sqrt(vector1 * vector2)
        cosine_score[docid] = nm/denominator
    return cosine_score


