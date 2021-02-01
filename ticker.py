from bs4 import BeautifulSoup
import ssl
import json
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0']
out = open('ticker.txt','w')
for i in list:
    url = "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=%s"%i

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')


    for td in soup.findAll("td"):
        if td.has_attr('align="left"'):
            for a in td.findAll("a", recursive=False):
                out.write('{ label: "'+a.text.strip()+'", ')
        #else:
         #   for b in td.findAll('a'):
          #      if b.findAll('img')!=None:
           #         continue
            #    else:
             #       out.write('value: '+b.text.strip()+'" }\n')



    with open('tickers.html', 'wb') as file:
        file.write(html)

