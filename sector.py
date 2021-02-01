from bs4 import BeautifulSoup
import ssl
import json
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Input from the user
url = input('Enter Yahoo Finance Company Url- ')
# Making the website believe that you are accessing it using a Mozilla browser
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
# Creating a BeautifulSoup object of the HTML page for easy extraction of data.

soup = BeautifulSoup(webpage, 'html.parser')
html = soup.prettify('utf-8')
company_json = {}

for span in soup.findAll("span", attrs={"class":"Fw(600)", "data-reactid":"21"}):
    company_json["SECTOR"] = span.text.strip()

with open("data3.json", "w") as outfile:
    json.dump(company_json, outfile, indent=4)

with open("sector_output.html", "wb") as file:
    file.write(html)