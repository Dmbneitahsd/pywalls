def pagefetch():
    import requests
    from bs4 import BeautifulSoup
    import re
    import json
    from datetime import datetime
    #static business for the counters
    RGPcounterurls="d0f355e237dda999f3112d94d3c762c7" # TCA
    urlstart="https://portal.rockgympro.com/portal/public/"
    urlend="/occupancy"

    newwallids={}
    geturl=urlstart+RGPcounterurls+urlend
    print("getting "+geturl)
    
    #visit the page and fetch the data for munging
    page = requests.get(geturl).text

    #timestamp
    today = datetime.now()
    timestamp = {"timechecked" : str(today)}

    #read that data in
    soup=BeautifulSoup(page, 'html.parser')

    #find all the scripts on the page
    for dat in soup.find_all('script'):
    #look for the one we are interested in
    #define the regex to only match the bit which is useful
    regex = r"var data(.*)},    };"
    #change the object into a string for searching
    usefulbits = str(dat)
    
    #just pull out the bit we need
    matches = re.search(regex, usefulbits, re.DOTALL | re.IGNORECASE)
    #sort it out into usable format
    if matches:
        datastr=matches.group(0).replace("var data = ","")
        datastr=datastr.replace("\n", "")
        datastr=datastr.replace("  ", "")
        datastr=datastr.replace("\'", "\"")
        datastr=datastr.replace("},};", "}}") 
        
        jsondata = json.loads(datastr)
        jsondata.update(timestamp)
        
return jsondata

def database_insert(jsondata)
    from google.cloud import bigquery
    import io
    #i had terrible trouble getting bq to accept it as a string, so stream to a file like object first
    data_as_file = io.StringIO(str(jsondata))

    #instantiate the client - auth handled by service account 
    client = bigquery.Client()

    #variables
    dataset_id = 'walldata'
    table_id = 'howfullismywall'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.autodetect = True

    #send stuff to bq
    job = client.load_table_from_file(
        data_as_file,
        table_ref,
        job_config=job_config,
    )

    #output
    job.result()

    print("loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))

#entry point
def hello_world(request):
    
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        results = pagefetch()
        database_insert(results)
