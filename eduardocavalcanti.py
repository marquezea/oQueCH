import bs4
import requests
import sqlite3
from urllib.request import urlopen

def parseSite(papel):
    # set URL to be opened
    myUrl = 'https://eduardocavalcanti.com/an_fundamentalista/' + papel + '/'
    print(myUrl)

    # open web page and get HTML data
    myClient = urlopen(myUrl)
    myPage_html = myClient.read()
    myClient.close()

    # html parsing
    mySoup = bs4.BeautifulSoup(myPage_html,'html.parser')

    # decode the parsed html into elements
    #myTable = mySoup.table
    myTable = mySoup.find('table', attrs={ 'class' : 'table table-hover table-condensed table-responsive analise'})
    myHeaders = [header.text for header in myTable.find_all('th')]
    print(myHeaders)

    myRows = []
    for row in myTable.tbody.find_all('tr'):
        myRows.append([paramId] + [val.text for val in row.find_all('td')])

    print(myRows)
    return myRows

retRows = parseSite('tiet')
    
for row in retRows:
    print(row)
    