'''
In this python file i have implemented  the designed testing IF model algorithm
'''
#testing algorithm for IF model
def BM25test(collection,feature):
    rank = {}
    for docid, document in collection.get_documents().items():
        for word in feature.keys():
            if word in document.term_list():
                try:
                    rank[docid] += feature[word]
                except:
                    rank[docid] = feature[word]
    return rank
