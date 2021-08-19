#to get title and description as query.
# this is used to parse a query from implemented cosine measure model
def topic_description():
    topic_desc = {}
    statements = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Topic_definitions.txt', 'r')
    topic_ = statements.readlines()
    query = ""
    querystart = False

    for line in topic_:
        line = line.strip()
        if querystart == False:
            if line.startswith("<num"):
                for word in line.split():
                    if word.startswith("R"):
                        qu = word
                        querystart = True
        if querystart == True:
            if line.startswith("<title"):
                query = line.replace("<title>", "")
            elif line.startswith("<narr"):
                query.replace("<desc> Description:", "")
                topic_desc[qu] = query
                querystart = False
            else:
                if line.startswith("<desc"):
                    continue
                else:
                    query = query + " " + line

    return topic_desc


#to get only title as query. This is used to parse a query from implemented baseline BM25 model
def getQuery():
    topic = {}
    statements = open('/Users/juhi/Desktop/Sem4/IFN647/Ass2/Ass2 Solution/Topic_definitions.txt', 'r')
    topic_ = statements.readlines()
    for line in topic_:
        line = line.strip()
        if line.startswith("<num"):
            for word in line.split():
                if word.startswith("R"):
                    query = word
        if line.startswith("<title"):
            topic[query] = line.replace("<title>", '')
    return topic

