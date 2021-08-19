import os
import string
import glob
from porter2 import stem

class BowDocument:
    ''' Bag of words class of a document '''

    def __init__(self, documentId):

        self.documentId = documentId  #set ID of the document
        self.words = {}  #create an empty dictionary
        self.documentLen = 0

# To add word to the BowDocument - It is called each time a word occurs
    def word_addition(self, word):
        try:
            self.words[word] +=1
        except:
            self.words[word] =1

# To get word count
    def word_count(self, word):
        try:
            return self.words[word]
        except KeyError:
            return 0

# To get a dictionary of term:freq pairs
    def term_frequency_dict(self):
        return self.words

# To get the list of terms in a document
    def term_list(self):
        return sorted(self.words.keys())

# To get the document ID of document
    def docId(self):
        return self.documentId

# To sort the dictionary
    def __iter__(self):
        return iter(sorted(self.words.items(), key=lambda x: x[1], reverse=True))

    def get_documentLength(self):
        return self.documentLen

    def set_documentLength(self, documentLen):
        self.documentLen = documentLen


class Collection_Documents:
    ''' This class is used for collection of documents '''

# Create an empty collection
    def __init__(self):
        self.documents = {}

# Add document to the collection
    def document_add(self, document):
        self.documents[document.docId()] = document

# To get document ID of the document
    def get_document(self, documentId):
        return self.documents[documentId]

# To get a full list of documents
    def get_documents(self):
        return self.documents  # Returns key value pairs as documentId:documents

    def iterate(self):
        return Collection_Iterator(self)

# To get the number of documents in the collection
    def documents_number(self):
        return len(self.documents)

    def __iter__(self):
        return self.iterate()


class Collection_Iterator:
    ''' This class is used to iterate over the collection of documents '''

    def __init__(self, collection):
        self.collection = collection
        self.keys = sorted(collection.get_documents().keys())
        self.j = 0


    def __iter__(self):
        return self

    def upcoming(self):
        if self.j >=len(self.keys):
            raise StopIteration

        document = self.collection.get_documents(self.keys[self.j])

        self.j += 1
        return document

''' method defined for text-processing for each provided documents '''
def parse_collection(filepath):
    collection = Collection_Documents()
    os.chdir(filepath)
    sw = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/common-english-words.txt', 'r')
    sw_ = sw.read().split(',')
    for file in glob.glob("*xml"):
        curr_doc = None
        start_end = False
        wc = 0
        for line in open(file):
            line = line.strip()
            if start_end == False:
                if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            documentId = part.split("=")[1].split("\"")[1]
                            curr_doc = BowDocument(documentId)
                            break
                    continue
                if line.startswith("<text>"):
                    start_end = True
            elif line.startswith("<text>"):
                break
            elif curr_doc is not None:
                line = line.replace("<p>","").replace("</p>","")
                line = line.translate(str.maketrans('','',string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))

                for word in line.split():
                    wc+=1
                    word = stem(word.lower())
                    if len(word) >2 and word not in sw_:
                        curr_doc.word_addition(word)
        if curr_doc is not None:
            curr_doc.set_documentLength(wc)
            collection.document_add(curr_doc)
    sw.close()
    return collection





