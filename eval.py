'''
This python file is used to evaluate the baseline model and IF model
'''
def eval(score, test):
    c = 0
    benchmarkFile = open(test)
    b_file = benchmarkFile.readlines()
    benchmark = {}
    for line in b_file:
        line = line.strip()
        line_s = line.split()
        benchmark[line_s[1]] = float(line_s[2])
        if float(line_s[2]) == 1.0:
            c += 1
    benchmarkFile.close()

    rank = {}
    j = 1
    # print(score)
    for line in open(score):
        # print(line)
        line = line.strip()
        l = line.split()
        rank[str(j)] = l[0]
        j += 1

    recall = 0
    precision = 0
    fmeasure = 0
    z=0

    for(number,docid) in sorted(rank.items(),key=lambda x:int(x[0])):
        if (benchmark[docid] == 1):
            z += 1
            precision = float(z)/float(int(number))
        if (number=='10'):
            recall  = float(z)/min(10, c)
            break
    if precision !=0:
        fmeasure = (2*precision*recall)/(precision + recall)
    return precision,recall,fmeasure

