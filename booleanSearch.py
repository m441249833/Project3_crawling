import json
import re

def intersecting_list(l,dict):
    ll = []
    for item in l :
        if dict.get(item.lower()) != None:
            ll.append(item.lower())
        else:
            print("word \'"+item+"\' is no in the database")

    if len(ll) == 0:
        return []
    ele = ll[0]
    result=[]
    for i in dict[ele.lower()]:
        count = 1
        for j in ll[1:]:
            if i in dict[j.lower()]:
                count +=1
        if count == len(ll):
            result.append(i)
    return result


def union_list(l,dict):
    if dict.get(l[0].lower()) != None:
        result = dict[l[0].lower()]
    else:
        print("word \'" + l[0] + "\' is no in the database")
        result = []
    for i in range(1,len(l)):
        if dict.get(l[i].lower()) != None:
            result += dict[l[i].lower()]
        else:
            result +=[]
            print("word \'" + l[i] + "\' is no in the database")
    order_dict= {}
    for item in result:
        if order_dict.get(item) != None:
            order_dict[item] +=1
        else:
            order_dict[item] = 1
    result = []

    # put the document id union from the query, but sorted by its frequency
    print("OR operator detected, sorting by document frequency......")
    for k in sorted(order_dict, key=order_dict.get, reverse=True):
        result.append(k)


    return result

def single_list(word,dict):
    if dict.get(word.lower()) == None:
        print("word \'" + word + "\' is no in the database")
        return []
    else:
        return dict[word.lower()]


f = open('disk.json','r')
dict = json.load(f)

def boolean_query(str,dict):
    if re.search(" AND ",str):
        str = str.split(" AND ")
        return intersecting_list(str,dict)
    elif re.search(" OR ",str):
        str = str.split(" OR ")
        return union_list(str,dict)
    else:
        return single_list(str,dict)


if __name__ == '__main__':

    while True:
        str = input("Please enter a string(enter -1 to exit):")
        if str == '-1':
            break
        try:
            answer = boolean_query(str, dict)
            print("query result for \'" + str + "\':")
            for item in answer:
                print(item)
        except:
            print("input error")