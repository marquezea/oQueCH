import bs4
import requests
import sqlite3
from urllib.request import urlopen

def parseSite(paramId):
    # set URL to be opened
    myUrl = 'http://fundamentus.com.br/resultado.php?setor=' + str(paramId)

    # open web page and get HTML data
    myClient = urlopen(myUrl)
    myPage_html = myClient.read()
    myClient.close()

    # html parsing
    mySoup = bs4.BeautifulSoup(myPage_html,'html.parser')

    # decode the parsed html into elements
    #myTable = mySoup.table
    myTable = mySoup.find('table', attrs={ 'id' : 'resultado'})
    myHeaders = [header.text for header in myTable.find_all('th')]

    myRows = []
    myRows.append(myHeaders)
    for row in myTable.tbody.find_all('tr'):
        myRows.append([paramId] + [val.text for val in row.find_all('td')])

    return myRows

# create SQLITE DB
cmd = """INSERT INTO STOCKS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

with sqlite3.connect("stocks.db") as conn:
    # Create the table if it doesn't exist.
    conn.execute(
        """CREATE TABLE IF NOT EXISTS STOCKS(
                ID_SETOR int,
                PAPEL string,
                COTACAO number,
                P_L number,
                P_VP number,
                PSR number,
                DIV_YIELD number,
                P_ATIVO number,
                P_CAP_GIRO number,
                P_EBIT number,
                P_ATIV_CIRC_LIQ number,
                EV_EBIT number,
                MRG_EBIT number,
                MRG_LIQ number,
                LIC_CORR number,
                ROIC number,
                ROE number,
                LIQ_2MESES number,
                PATRIM_LIQ number,
                DIV_BRUT_PATRIM number,
                CRESC_REC_5A number
            );"""
        )

    # delete previous data
    conn.execute('DELETE FROM STOCKS')

    f = open('stocks.csv','w', newline='', encoding='utf-8')
    writer = csv.writer(f, dialect='myDialect')
    for row in retRows:
        writer.writerow(row)
    f.close()

    # loop all sectors
    for i in range(45):
        retRows = parseSite(str(i+1))
    
        for row in retRows:
            conn.execute(cmd, row)



