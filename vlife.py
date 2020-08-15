#!/usr/bin/python
from __future__ import division
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import json


                
verticallifeurls=["https://gyms.vertical-life.info/en/the-climbing-works/counter"]                

walls={}

class Wall:
    def __init__(self, fname):
        self.fancyname="fname"  #name of wall
        self.identifier="ident" #3-letter identifier
        self.capacity=""        #capacity
        self.lastupdated=""     #last update string
        self.count=""           #the prize
        self.subLabel=""        #because it's there
        self.city=""            #filled only if it's in the list above

    def barcolour(self): #return red, amber, or green
        if self.capacity==0:
            return(0) #dodge div/0 error
        
        fullness=100*int(self.count)/int(self.capacity)
        if fullness < 30:
            return("#238823")
        if fullness > 30 and fullness < 80:
            return("#FFBF00")
        if fullness > 80:
            return("#D2222D")
        return("#000000")
    

    

for i in verticallifeurls:   
    #cracked it. shityeah:
    session = HTMLSession()
    r = session.get(i)
    r.html.render()
    soup=BeautifulSoup(r.html.html, 'html.parser')  #why you gotta say it twice??? dunno but you do.

    cnt=soup.find("span","display-1").contents[0]
    cap=soup.find("span","display-4").contents[0].replace("/","")
    tm=soup.find_all("div","small")
    lastactivity=soup.find_all("div","small")
    wname="The Climbing Works"
    a=Wall(wname)
    a.identifier="WKS"
    a.fancyname=wname
    a.capacity=cap
    a.count=cnt
    a.lastupdated=tm[0].contents[0]+" "+tm[1].contents[0]
    walls[wname]=a




    
bigfatjson={}
#dump data to terminal
for k in walls.keys():
    #print(k, walls[k].identifier, walls[k].count, "of", walls[k].capacity, walls[k].lastupdated, walls[k].city)
    bigfatjson[k]=walls[k].__dict__



print(json.dumps(bigfatjson, indent=4, sort_keys=True))    
    
 
    
   
       

    
    
 
