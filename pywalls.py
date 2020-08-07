#!/usr/bin/python
from __future__ import division
import requests
from bs4 import BeautifulSoup
import re
import json

RGPcounterurls=["4f7e4c65977f6cd9be6d61308c7d7cc2", # Depot
                "a67951f8b19504c3fd14ef92ef27454d", # *owall
                "7489d57c01f2949270a79fe4287f25b4", # Foundry   !!! This one has no pretty name. needs a special case
                "c770b48889885c4843912a6bea432680", # Kendal      !!! This one has no pretty name. needs a special case
                "c3b9019203e4bc4404983507dbdf2359", # Dunne's lot
                "d0f355e237dda999f3112d94d3c762c7", # TCA
                "95faeefedaecb6935caa7958706f8249", # Flashpoint Swindon
                "f5388d62ad88ab759edac8b861d585b7", # High Sports Brighton
                "92d94d22394b00c6d3f6f2c90c402db1", # Awesome Walls
                "51b34d29708b17d6270dbfee783f7375", # Here Yonder  !!! This one has no pretty name. needs a special case
                ]
                
verticallifeurls=["https://gyms.vertical-life.info/en/the-climbing-works/counter"]                


Edenrockurls=["https://wallmarket.herokuapp.com/eden-rock-edinburgh/entries"]

urlstart="https://portal.rockgympro.com/portal/public/"
urlend="/occupancy"


#7/8/20 - the 3-letter id things are NOT unique. Arsecakes. Gonna have to store by full name.




walls={}

class Wall:
    def __init__(self, fname):
        self.fancyname="fname"  #name of wall
        self.identifier="ident" #3-letter identifier
        self.capacity=""        #capacity
        self.lastupdated=""     #last update string
        self.count=""           #the prize
        self.town=""            #can store city name so we can group and sort (not implemented)
        self.subLabel=""        #because it's there

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
    


for i in RGPcounterurls:
    newwallids={}
    geturl=urlstart+i+urlend
    #print "getting "+geturl
    page = requests.get(geturl).text
    soup=BeautifulSoup(page, 'html.parser')

    for opt in soup.find_all('option'):
        if (opt.get('value')):
            wid=opt.get('value')
            nm=opt.text     
            newwallids[wid] = nm
            
            
    if i=='51b34d29708b17d6270dbfee783f7375':#Here yonder has no option/value bit. Any others???
        #print "Here Yonder"
        wid="AAA"
        nm="Here Yonder"          
        newwallids[wid] = nm
        
    if i=='c770b48889885c4843912a6bea432680':#Here yonder has no option/value bit. Any others???
        #print "Kendal"
        wid="AAA"
        nm="Kendal"          
        newwallids[wid] = nm     
        
    if i=='7489d57c01f2949270a79fe4287f25b4':#Here yonder has no option/value bit. Any others???
        #print "Foundry"
        wid="AAA"
        nm="Foundry"          
        newwallids[wid] = nm          
        
        

    for dat in soup.find_all('script'):
        if (re.search('var(.*)};',dat.text,re.DOTALL)):
            x=re.search('var(.*?)};',dat.text,re.DOTALL)    
            datastr=x.group(0).replace("var data = ","")
            datastr=datastr.replace("\n", "")
            datastr=datastr.replace("  ", "")
            datastr=datastr.replace("\'", "\"")
            datastr=datastr.replace("},};", "}}") 
            #print datastr

    vardata = json.loads(datastr)
    
    
    for j in newwallids.keys():
        print j, newwallids[j]
        a=Wall(j)
        walls[newwallids[j]]=a
        a.fancyname=newwallids[j]
        a.identifier=j
        a.capacity=vardata[j]["capacity"]
        a.count=vardata[j]["count"]
        a.subLabel=vardata[j]["subLabel"]
        a.lastupdated=vardata[j]["lastUpdate"].replace("&nbsp"," ")
        


    #print d["CNW"]["count"]
for i in Edenrockurls:
    newwallids={}
    geturl=i
    #print "getting "+geturl
    page = requests.get(geturl).text
    soup=BeautifulSoup(page, 'html.parser')
    
    cn=soup.find("h1", "display-4")
    ca=soup.find("small", "text-muted")
    #print cn.contents[0],"of",ca.contents[0].replace("/ ","")
    a=Wall("Eden Rock")
    a.fancyname="Eden Rock"
    a.identifier=j
    a.capacity=ca.contents[0].replace("/ ","")
    a.count=cn.contents[0]
    a.lastupdated=""
    walls["Eden"]=a
    
    

for i in verticallifeurls:   
    #ugh. where's the number?
    geturl=i
    page = requests.get(geturl).text
    soup=BeautifulSoup(page, 'html.parser')
    #print soup
    
    #can't find the data here. Help?
    
    

#dump data to terminal
for k in walls.keys():
    print k, walls[k].identifier, walls[k].count, "of", walls[k].capacity, walls[k].lastupdated
    
    
    
#going off piste now. Beyond here is just spitting out a webpage for testing. bits of it may come in useful.  
    
    
sitecode="<html>"
sitehead="""<head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Load the Visualization API and the corechart package.
      google.charts.load('current', {'packages':['corechart']});\n\n"""
sitebody=""
sitetable=""

chartiterator=0
for k in walls.keys():
    chartiterator+=1
    sitehead+="google.charts.setOnLoadCallback(drawchart"+str(chartiterator)+");\n"
    sitehead+="function drawchart"+str(chartiterator)+"() {\n"
    #sitehead+="var data = new google.visualization.DataTable();\n"
    #sitehead+="data.addColumn('string', '"+str(k)+"');\n"
    #sitehead+="data.addColumn('number', 'Climbers');\n"
    #sitehead+="data.addRows([\n['',"+str(walls[k].count)+"],\n]);\n"
    sitehead+="var data = google.visualization.arrayToDataTable([\n"
    sitehead+="['Wall', 'Climbers',{ role: 'style' }, { role: 'annotation' }],\n"
    sitehead+="['', "+str(walls[k].count)+",'color: "+walls[k].barcolour()+"' , '"+str(walls[k].count)+"of"+str(walls[k].capacity)+"'],\n"
    sitehead+="]);\n"
    sitehead+="var options = {height:50, width:300, legend: 'none', theme: 'maximized', hAxis: {gridlines:{count:0},\n"
    sitehead+="ticks: [0,"+str(walls[k].capacity)+"],\n"
    sitehead+="viewWindow: {min:0, max:"+str(walls[k].capacity)+"}}};\n"
    sitehead+="var barchart = new google.visualization.BarChart(document.getElementById('"+str(chartiterator)+"'));\n"
    sitehead+="barchart.draw(data, options);\n}\n\n"


    
    sitetable+='<tr><td>'+str(k)+'</td><td><div id='+str(chartiterator)+'></div></td><td>'+str(walls[k].count)+' of '+str(walls[k].capacity)+'</td><td>'+str(walls[k].lastupdated)+'</td></tr>'


      
      
   
      
sitebody="""</script>
  </head><body><table style=\"width:80%\">"""

    
    
    
    





sitecode=sitehead+sitebody+sitetable


sitecode+="</table></body></html>"

wpage=open('site.html','w')
wpage.write(sitecode)    
wpage.close()    
    




    
    
