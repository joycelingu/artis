from bs4 import BeautifulSoup
import ssl
import json
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Input from the user
ticker = input('Enter company ticker: ')
url1 = "https://finance.yahoo.com/quote/%s/profile?p=%s"%(ticker, ticker)
url2 = "https://finance.yahoo.com/quote/%s?p=%s"%(ticker, ticker)
url3 = "https://finance.yahoo.com/quote/&s/sustainability?p=%s"%(ticker, ticker)

# Making the website believe that you are accessing it using a Mozilla browser
req1 = Request(url1, headers={'User-Agent': 'Mozilla/5.0'})
req2 = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
req3 = Request(url3, headers={'User-Agent': 'Mozilla/5.0'})
webpage1 = urlopen(req1).read()
webpage2 = urlopen(req2).read()
webpage3 = urlopen(req3).read()
# Creating a BeautifulSoup object of the HTML page for easy extraction of data.

soup1 = BeautifulSoup(webpage1, 'html.parser')
soup2 = BeautifulSoup(webpage2, 'html.parser')
soup3 = BeautifulSoup(webpage3, 'html.parser')
html1 = soup1.prettify('utf-8')
html2 = soup2.prettify('utf-8')
html3 = soup3.prettify('utf-8')
company_json = {}

#from profile section
for span in soup1.findAll("span", attrs={"class":"Fw(600)", "data-reactid":"21"}):
    company_json["SECTOR"] = span.text.strip()

#from summary section
for span in soup2.findAll('span',attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'}):
    company_json['PRESENT_VALUE'] = span.text.strip()
for div in soup2.findAll('div', attrs={'class': 'D(ib) Va(t)'}):
    for span in div.findAll('span', recursive=False):
        company_json['PRESENT_GROWTH'] = span.text.strip()

for td in soup2.findAll('td', attrs={'data-test': 'TD_VOLUME-value'}):
    for span in td.findAll('span', recursive=False):
        company_json['TD_VOLUME'] = span.text.strip()
for td in soup2.findAll('td', attrs={'data-test': 'MARKET_CAP-value'}):
    for span in td.findAll('span', recursive=False):
        company_json['MARKET_CAP'] = span.text.strip()

for td in soup2.findAll('td',attrs={'data-test': 'ONE_YEAR_TARGET_PRICE-value'}):
    for span in td.findAll('span', recursive=False):
        company_json['ONE_YEAR_TARGET_PRICE'] = span.text.strip()

#from sustainability section
for span in soup3.findAll("span", attrs={"class":"Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)"}):
    company_json["ESG"] = span.text.strip()

for div in soup3.findAll("div", attrs={"class":"D(ib) smartphone_D(b)", "data-reactid":"36"}):
    for span in div.findAll("span", recursive=False):
        company_json["ENVIRONMENT"] = span.text.strip()

for div in soup3.findAll("div", attrs={"class":"D(ib) smartphone_D(b)", "data-reactid":"46"}):
    for span in div.findAll("span", recursive=False):
        company_json["SOCIAL"] = span.text.strip()

for div in soup3.findAll("div", attrs={"class":"D(ib) smartphone_D(b)", "data-reactid":"56"}):
    for span in div.findAll("span", recursive=False):
        company_json["GOVERNANCE"] = span.text.strip()

with open('data.json', 'w') as outfile:
    json.dump(company_json, outfile, indent=4)

with open('output_file.html', 'wb') as file:
    file.write(html1)
