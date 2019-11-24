import collections
import heapq
import json
import re
from math import log

f = open('disk.json', 'r')
dict = json.load(f)
f.close()
f= open('doc_length','r')
docLength=json.load(f)

def bm25(q,dict):
    '''
    :param q: input query
    :param dict: database
    :return: query result with score of the document.
    '''
    # split the str removing all punctuations, digits, only focus on lowercase letter
    query = re.findall(r'\w+',q)
    k = 1
    b = 0.5
    score_q = {}
    common_word = 0
    avg_dl = 0
    for item in docLength.values():
        avg_dl+=item
    avg_dl = avg_dl/len(docLength)
    for item in dict.values():
        if len(item) > common_word :
            common_word = len(item)

    for word in query:
        if dict.get(word) == None:
            continue
        # find the top 20 document from the postings list that includes the current query word.
        count = collections.Counter(dict[word])
        postings = heapq.nlargest(20, count.keys(), key=count.get)
        #nw is the number of the documents that the word occurs.
        nw = len(postings)
        for docID in postings:
            dw = 0
            for num in dict[word]:
                if num == docID : dw +=1
            # applying the BM25 formula to find the score for current word in current document.
            score = nw*( (dw*(1+k)) / ( dw + k*((1-b)+(b*docLength[docID])/avg_dl) ) ) * (log( (common_word-nw+0.5) / (nw+0.5) ))
            # round the score to 2 decimal places
            score = round(score,2)
            # adding up the score for all query words, e.g. score(q,doc1) = score(q[0],doc1)+score(q[1],doc1)+......
            if score_q.get(docID) != None:
                score_q[docID] += score
            else:
                score_q[docID] = score
    result = []
    # form the score in reverse order, which is also from higher score to lower score, and controll it to produce only the top 10.
    top_control = 0
    for k in sorted(score_q, key=score_q.get, reverse=True):
        result.append((k,score_q[k]))
        top_control +=1
        if top_control >=10:
            break
    return result

if __name__ == '__main__':
    str = ""
    while True:
        str = input("Please enter a string(enter -1 to exit):")
        if str == '-1':
            break
        try:
            str = re.sub('\d+','',str.lower())
            answer = bm25(str,dict)
            print("query result for \'" + str + "\': [(docID,score)]")
            for item in answer:
                print(item)
        except:
            print("input error")