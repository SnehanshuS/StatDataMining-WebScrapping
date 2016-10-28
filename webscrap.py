# In Python 
import requests
#import bs4 # import main module first
from bs4 import BeautifulSoup, SoupStrainer
import os, csv

def get_raw_html(url):
    # Given a raw url, returns the html of the page.
    r = requests.get(url)
    ad_page_html = r.text
    return ad_page_html
page = 4000
count_per_page = 28
os.chdir("C:\Users\sneh\Desktop\python_intro")
with open("BoatDetails.csv", "wb") as toWrite:
    writer = csv.writer(toWrite)
    writer.writerow(["BOAT URL", "PRICE", "MAKE", "CONTACT","BOAT CLASS", "BOAT CATEGORY","YEAR"])
    
    while page <= 9000:
        print page 
        url_boat = "http://www.boattrader.com/search-results/NewOrUsed-any/Type-any/Category-all/Zip-33613/Radius-4000/Sort-Length:DESC/Page-%s,28?" %page
        raw_html = get_raw_html(url_boat) 
        soup = BeautifulSoup(raw_html, "html.parser")
        for boat in soup.find_all('a', {'data-reporting-click-listing-type': 'standard listing'}): 
            # followed by finding the <a> for each of the <a>
            links = boat.find_all('a', href=True)
            if len(links) != 0: # Check for data availability.
                link = links[0]
                url = link['href'].encode('utf-8')
                print "----------Page"+str(page)+"------------"
                print url
                individual_page_html= get_raw_html("http:"+url)
                soup1 = BeautifulSoup(individual_page_html, "html.parser")
                make = soup1.find_all('span', {'class': 'bd-make'})
                if len(make) !=0:
                    makeBoat = make[0].get_text().strip()
                else:
                    makeBoat = "NA"     
                year = soup1.find_all('span', {'class': 'bd-year'})
                if len(year)!=0:
                    yearBoat = year[0].get_text().strip()
                else:
                    yearBoat = "NA"
                indvDetailContact = soup1.find_all('a', {'class': 'phone'})
                if len(indvDetailContact) !=0:
                    contact = indvDetailContact[0].get_text().strip()
                else:
                    contact = "NA"
                sellerPrice = soup1.find_all('span', {'class': 'bd-price contact-toggle'})
                if len(sellerPrice)!=0:
                    price = sellerPrice[0].get_text().strip()
                else:
                    price = "NA"
                boattype = soup1.find_all('div', {'class':'collapsible open'})
                if len(boattype) !=0:
                    tab = boattype[0].find_all('td')
                    boatClass = tab[0].get_text().strip()
                    boatCategory = tab[1].get_text().strip()
                else:
                    boatClass = "NA"
                    boatCategory = "NA"
                model = "Make :" + makeBoat+ " / Year :" + yearBoat
                print boatClass
                print boatCategory
                print makeBoat
                print yearBoat
                print contact
                print price
                writer.writerow([url,price,makeBoat, contact, boatClass,boatCategory,yearBoat])
        page = page + 1
