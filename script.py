'''
I have used Pycharm to implement the designed algorithm in python language
This is main script file. By running this file the all requirements as described in Assignment will run
'''
import itertools
import glob
import string
import os
import Baseline_BM25
import BM25_test
import BM25_train
import cosine
import documentFrequency
import eval
import preprocess
import query
import TTest

baseline_model = {}

IF_model = {}

'''
The below code is used to answer Question No.2 given in assignment. 
For this question, i have used title and description as query
'''
documents = glob.glob("/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/dataset101-150/*")
for dir in documents:
    details = dir.split("/")
    tr = details[len(details)-1].split("\\")
    # print(tr)
    documentId = tr[0].replace('Training', '')

    # print(documentId)
    collection_ = preprocess.parse_collection("/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/dataset101-150/" +
                                               str(tr[0]))
    for k,v in query.topic_description().items():
        digit = k.split('R')
        # print(digit[1])
        if digit[1] == documentId:
            calculate = cosine.CosineMeasure(collection_, v)
            print('Search query ' + v)
            writeFile = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Baseline_results/TFIDF_R' +
                             str(documentId)+ '.dat', 'w')
            for (key, value) in sorted(calculate.items(), key=lambda z:z[1], reverse=True):
                writeFile.write(key + ' ' + str(value) + '\n')
            writeFile.close()

            C_av = sum(va for (ke,va) in calculate.items())/collection_.documents_number()
            result = {}
            wf = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Tr_Set/Tr_R'+str(documentId) + '.txt', 'w')
            df = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Baseline_results/TFIDF_R' +
                      str(documentId) + '.dat')
            f_ = df.readlines()
            for line in f_:
                line = line.strip()
                l1 = line.split()
                if float(l1[1]) > C_av + 0.0011:
                    wf.write('R' + str(documentId) + " " + str(l1[0]) + ' 1 ' + '\n')
                    result[l1[0]] =1
                else:
                    wf.write('R' + str(documentId) + ' ' + str(l1[0]) + ' 0 ' + '\n')
            wf.close()
            df.close()


'''
The below code is used to answer Question No.5 given in assignment. For this question i have used only title as query
'''


for dir in documents:
    details = dir.split("/")
    tr = details[len(details)-1].split("\\")
    # print(tr)
    documentId = tr[0].replace('Training','')
    # print(tr[0])

    collection_ = preprocess.parse_collection("/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/dataset101-150/" +
                                              str(tr[0]))
    docfreq = documentFrequency.df(collection_)
    for k, v in query.getQuery().items():
        digit = k.split('R')
        # print(digit[1])
        if digit[1] == documentId:
            bm25 = Baseline_BM25.bm25_baseline(collection_,v,docfreq)
            print('Search Query ' + str(v))
            os.chdir('..')
            wf = open("/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/BM25_base/B_Result" +
                      str(digit[1]) + '.dat','w')
            for (key,value) in sorted (bm25.items(),key=lambda z:z[1], reverse=True):
                wf.write(key + ' ' + str(value) + '\n')
            wf.close()


'''
The below code is used to answer Question No.5 given in assignment. 
This script code is used for designed training algorithm.
'''

train = glob.glob('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Tr_Set/*')
for dir in documents:
    details = dir.split("/")
    tr = details[len(details)-1].split("\\")
    # print(tr)
    documentId = tr[0].replace('Training','')

    collection_ = preprocess.parse_collection("/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/dataset101-150/" +
                                              str(tr[0]))

    for file in train:
        train_file = file.split("/")
        tf = train_file[len(train_file)-1].split('\\')
        file_num = tf[0].replace('Tr_R','')
        get_num = file_num.replace('.txt','')
        if get_num == documentId:
            os.chdir('..')
            bf= open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Tr_Set/Tr_R'+str(get_num)+'.txt')
            f_ = bf.readlines()
            result = {}
            for line in f_:
                line=line.strip()
                l1 = line.split()
                result[l1[1]]= float(l1[2])
            bf.close()
            t = 3.5
            result = dict(itertools.islice(result.items(),5))
            bm25_score = BM25_train.w4(collection_,result,t)
            wf = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Train/feature_R'+ str(documentId) + '.dat','w')
            for (key,value) in sorted(bm25_score.items(),key=lambda z:z[1], reverse=True):
                wf.write(key + ' ' + str(value) + '\n')
            wf.close()


'''
The below code is used to answer Question No.5 given in assignment. 
This script code is used for designed testing algorithm.
'''

train = glob.glob('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Train/*')
for dir in documents:
    details = dir.split("/")
    tr = details[len(details)-1].split("\\")
    # print(tr)
    documentId = tr[0].replace('Training','')

    collection_ = preprocess.parse_collection("/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/dataset101-150/" +
                                              str(tr[0]))
    docfreq = documentFrequency.df(collection_)
    for file in train:
        train_file = file.split("/")
        tf = train_file[len(train_file) - 1].split('\\')
        file_num = tf[0].replace('feature_R', '')
        get_num = file_num.replace('.dat', '')
        if get_num == documentId:
            os.chdir('..')
            bf = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Train/feature_R' + str(get_num) + '.dat')
            f_ = bf.readlines()
            features = []
            features_dict = {}
            for line in f_:
                line = line.strip()
                l1 = line.split()
                features.append(l1[0])
                features_dict[l1[0]] =float(l1[1])
            bf.close()
            query_add = " ".join(str(z) for z in features[:5])
            fea = dict(itertools.islice(features_dict.items(),5))

            order = BM25_test.BM25test(collection_,fea)
            wf = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Test/IF_Result' +
                      str(documentId) + '.dat','w')
            for (key,value) in sorted(order.items(), key=lambda z:z[1],reverse=True):
                wf.write(key + ' ' + str(value) + '\n')
            wf.close()




'''
The below code is used to answer Question No.6 given in assignment. 
This script code is used to evaluate the designed baseline model and Information Filtering model (IF model).
'''

baseline_model_result = glob.glob('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/BM25_base/*')
IF_model_result = glob.glob('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Test/*')
topics = glob.glob('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Relevance_judgments/*')
for dir in topics:
    details = dir.split("/")
    tr = details[len(details)-1].split("\\")
    documentId = tr[0].replace('Training', '')
    documentNo = documentId.replace('.txt', '')
    # print(documentNo)

    relevance_judgement = ('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Relevance_judgments/Training' +
                           str(documentNo) + '.txt')
    base = ('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/BM25_base/B_Result' + str(documentNo) + '.dat')
    baseline_evaluation = eval.eval(base, relevance_judgement)

    wf = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Evaluation_results/EResult2.dat', 'a')
    wf.write("DocID" + '\t' + "Precision" + '\t' +"Recall" + '\t' +"FMeasure" +'\t')
    wf.write(documentNo +'\t' + str(baseline_evaluation[0]) + '\t' + str(baseline_evaluation[1]) +'\t' +
             str(baseline_evaluation[2]) + "\n")
    #wf.write(documentNo + "Precision" + str(baseline_evaluation[0]) + "Recall" + str(baseline_evaluation[1]) + "F-measure" + str(baseline_evaluation[2]) + "\n")
    wf.close()

    IF_result = glob.glob('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Test/IF_Result' + str(documentNo) + '.dat')
    IF_model_evaluation = eval.eval(IF_result[0],relevance_judgement)

    wf = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Evaluation_results/EResult1.dat', 'a')
    wf.write("DocID" +'\t' + "Precision" + '\t' +"Recall" + '\t' +"FMeasure"+'\t')
    wf.write(documentNo + '\t' +str(IF_model_evaluation[0]) +'\t' + str(IF_model_evaluation[1])
             + '\t' +str(IF_model_evaluation[2]) + "\n")
    #wf.write(documentNo + "Precision" + str(IF_model_evaluation[0]) + "Recall" + str(IF_model_evaluation[1]) +
    # "F-measure" + str(IF_model_evaluation[2]) + "\n")
    wf.close()

    '''
    The below code is used to answer Question No.7 given in assignment. 
    This script code is used to conduct a T-test
    '''

    baseline_model[documentNo] = baseline_evaluation
    IF_model[documentNo] = IF_model_evaluation

TTest.Ttest(baseline_model, IF_model)




