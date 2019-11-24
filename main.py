import re
import json
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
sw = set(stopwords.words('english'))

dict={}
start_url = "https://www.concordia.ca/research.html"
base = "https://www.concordia.ca"
max_depth = 3
all_links=[]

def getAllLinks(url,depth):
    if depth<=0:
        return 0
    else:
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        all_links.append(url)
        for link in soup.find_all('a'):
            temp = link.get('href')
            if (temp != None) and (len(temp)>0):
                if temp[0] == '/':
                    temp = base+temp
                if (temp not in all_links) and (re.search('https://',temp)):
                    getAllLinks(temp,depth-1)



def extractText(url):
    content=requests.get(url).text
    soup = BeautifulSoup(content,'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    raw = soup.get_text()
    raw = re.sub('\d+','',raw)
    raw = re.findall(r'\w+',raw)
    invertIndex(raw,url)


def invertIndex(text_list,url):
    for term in text_list:
        if term.lower() in sw:
            continue
        if dict.get(term.lower()) != None:
            if url not in dict[term.lower()]:
                dict[term.lower()].append(url)

        else:
            dict[term.lower()] = [url]

def download():
    for item in sorted(dict):
        print (item , ":",dict[item])
    f = open('disk.json','w')
    json.dump(dict,f)
    return 0

if __name__ == '__main__':
    getAllLinks(start_url,max_depth)
    for link in all_links:
        extractText(link)
    download()

    print(all_links)

