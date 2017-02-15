#!/bin/python3
from bs4 import BeautifulSoup
import requests
import re

website = input('Enter a website to Spider: ')
new = []
visited = []
if 'https://' not in website:
    tmp = website.strip('http://')
    sslwebsite = 'https://' + tmp
else:
    sslwebsite = website
    tmp = website.strip('https://')
    website = 'http://' + tmp

raw = requests.get(website, verify=False)
soup = BeautifulSoup(raw.content, 'html.parser')

for a in soup.find_all('a'):
    new.append(a.get('href'))
#    print(a.get('href'))

while(len(new) != 0):
    link = new[0]
    visited.append(link)

    #add all the new links and stuff
    if website in link:
        print('Non-SSL: ',link)
        link = link.replace(website,'')
    elif sslwebsite in link:
        print('SSL: ',link)
        link = link.replace(sslwebsite,'')
    elif tmp in link:
        print('TMP: ', link)
        link = link.replace(tmp,'')
    else:
        #not in scope
        if(link != '/'):
            if link.startswith('http://'):
                new.remove(new[0])
                continue
            elif link.startswith('https://'):
                new.remove(new[0])
                continue

    #now lets get ready to visit new sites
    newwebsite = website + link
    sslnewwebsite = sslwebsite + link


#    print(newwebsite)
#    print(sslnewwebsite)
    if(requests.get(newwebsite).status_code == 200):
        raw = requests.get(newwebsite, verify=False)
        soup = BeautifulSoup(raw.content, 'html.parser')
        for a in soup.find_all('a'):
            test = a.get('href')
            if test not in new:
                if test not in visited:
                    new.append(a.get('href'))
        new.remove(new[0])

    elif(requests.get(sslnewwebsite).status_code == 200):
        raw = requests.get(sslnewwebsite, verify=False)
        soup = BeautifulSoup(raw.content, 'html.parser')
        for a in soup.find_all('a'):
            test = a.get('href')
            if test not in new:
                if test not in visited:
                    new.append(a.get('href'))
        new.remove(new[0])

print(visited)
