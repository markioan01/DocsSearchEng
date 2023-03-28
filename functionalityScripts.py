import pandas as pd
import json
import math
from tqdm import tqdm

DOC_SIZE = 0
fromIdxGLB = 0
toIdxGLB = 0
punc = '''!()-[]{};:'"\, <>./?@#$%^&*_`~'''
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


def readDocuments(fromIdx, toIdx):
    fromIdxGLB = fromIdx
    toIdxGLB = toIdx
    #print(toIdx)
    DOC_SIZE = int(toIdx) - int(fromIdx)
    docs = pd.read_csv("D:/dataForInfRetr/file.csv", skiprows=fromIdx,
                           nrows=toIdx, encoding='utf-8')
    # Documents size (in rows) = 1280918 (1,280,918)
    # Columns = 11


    file = []
    for i in range(fromIdxGLB, toIdxGLB):
        file.append(docs.loc[i]['speech'])

    
    # Remove the punctuation marks.
    
    for i,line in enumerate(file):
        for ele in line: 
            if ele in punc: 
                line = line.replace(ele, " ") 
                
        file[i] = line

    

    merged = ""
    for line in tqdm(file):
        merged += line
    merged = merged.lower()
    merged = " ".join(file)
    
    listStops = stopwords.words()
    #print(listStops)
    # Creating the inversed Cataloge

    text_tokens = word_tokenize(merged)
    text_tokens = list(dict.fromkeys(text_tokens))

    def wordTokenizer(merged):
        quantity = 10000000
        times = (int)(len(merged) / quantity) + 1

        text_tokens = word_tokenize(merged[:quantity])
        text_tokens = list(dict.fromkeys(text_tokens))

        for i in range(1,times):
            v0 = i*(quantity)-100
            v1 = (i+1)*(quantity)
            tt = word_tokenize(merged[v0:v1])
            tt[0] = ""
            tt[len(tt)-1] = ""
            tt = list(dict.fromkeys(tt))
            text_tokens = text_tokens + tt
            text_tokens = list(dict.fromkeys(text_tokens))
        return text_tokens



    tokens_without_sw = [
        word for word in text_tokens if not word in stopwords.words()]
    tokens_without_sw = list(dict.fromkeys(tokens_without_sw))
    
    '''
    # Reading the json files saved
    f = open('D:/dataForInfRetr/tokens.txt','r')
    jsonStr = f.read()
    tokens_without_sw = json.loads(jsonStr)
    '''
    
    #tokens_without_sw = list(dict.fromkeys(tokens_without_sw))

    # for 100 files, like 25 secs of running
    dict1 = {}

    for i in range(fromIdxGLB, toIdxGLB):
        check = file[i].lower()
        for item in tokens_without_sw:
     
            if item in check:
                if item not in dict1:
                    dict1[item] = []

                if item in dict1:
                    #dict1[item].append(i+1)

                    fileTokenized = word_tokenize(check)
                    counter = 0
                    for word in fileTokenized:
                        if(item==word):
                            counter += 1

                    if(counter>0):
                        dict1[item].append((i,counter))
    return file, dict1, docs

# Tok-k mmethod
def topK(q,dict1,k,file):
    s = []
    docIndex = []
    #print(q)
    #print(dict1)
    #print(file)
    for t in q:
        if t in dict1:
            listOfT = dict1[t]
            nt = len(listOfT)
            idf = math.log(1+(DOC_SIZE/nt))

            for f in listOfT:
                if f[0] in docIndex:
                    idx = docIndex.index(f[0])
                    tf = 1 + math.log(f[1])
                    s[idx] = s[idx] + tf*idf
                else:
                    s.append(0)
                    docIndex.append(f[0])
                    idx = docIndex.index(f[0])
                    #print(f[1])
                    tf = 1 + math.log(f[1])
                    s[idx] = s[idx] + tf*idf
    
    
    for i in range(len(s)):
        s[i] = s[i]/len(file[docIndex[i]-1])

    #sort
    n = len(s)
    swapped = False

    for i in range(n-1):
        for j in range(0, n-i-1):
            if s[j] < s[j + 1]:
                swapped = True
                s[j], s[j + 1] = s[j + 1], s[j]
                docIndex[j], docIndex[j + 1] = docIndex[j + 1], docIndex[j]                
        if not swapped:
            break;

    topk = []
    if(k > len(docIndex)):
        k = len(docIndex)
    for i in range(k):
        topk.append(docIndex[i])

    return topk



def clearQuery(q,file):
    #katharizi to query
    for i,line in enumerate(file):
        for ele in q: 
            if ele in punc: 
                q = q.replace(ele, " ")

    q = word_tokenize(q)

    q_without_sw = []
    for i,word in enumerate(q):
        if not word in stopwords.words():
            q_without_sw.append(word)
    q = q_without_sw
    return q
