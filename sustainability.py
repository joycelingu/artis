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

for title in soup.find("title"):
    company_json["TITLE"] = title.strip()

for span in soup.findAll("span", attrs={"class":"Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)"}):
    company_json["ESG"] = span.text.strip()

for div in soup.findAll("div", attrs={"class":"D(ib) smartphone_D(b)", "data-reactid":"36"}):
    for span in div.findAll("span", recursive=False):
        company_json["ENVIRONMENT"] = span.text.strip()

for div in soup.findAll("div", attrs={"class":"D(ib) smartphone_D(b)", "data-reactid":"46"}):
    for span in div.findAll("span", recursive=False):
        company_json["SOCIAL"] = span.text.strip()

for div in soup.findAll("div", attrs={"class":"D(ib) smartphone_D(b)", "data-reactid":"56"}):
    for span in div.findAll("span", recursive=False):
        company_json["GOVERNANCE"] = span.text.strip()

with open("data2.json", "w") as outfile:
    json.dump(company_json, outfile, indent=4)

with open("sustain_output.html", "wb") as file:
    file.write(html)