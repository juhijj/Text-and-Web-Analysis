import math
import glob
import porter2
'''
This python file is created to conduct a T-test
'''
def Ttest(y,z):
    diff=[]
    for docid,score in y.items():
        diff.append(float(z[docid][0]) - float(score[0]))

    mean = sum(v for v in diff) / len(diff)

    sd = math.sqrt(sum((v-mean) **2 for v in diff) / len(diff))

    tscore = mean/sd * math.sqrt(len(diff))

    print("##################################")
    print("Mean " + str(mean))
    print('Standard Deviation ' + str(sd))
    print("T-test Score " + str(tscore))
    print("#################################")
