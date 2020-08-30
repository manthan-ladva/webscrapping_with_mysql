import codecs
from selenium import webdriver
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import os

def web_scrapping(urls):
    #----------------ChromeDriver Function
    def get_browser():
        #----------------ChromeDriver for Selenium
        path_to_chromedriver = ('./chromedriver')
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)
        return browser
    
    #----------------HTML File Saving Function
    def file_saving(url):
        file_name = 'index.html'
        browser = get_browser() #------------1st Function Called Here

        #----------------Join URl to Chromedriver
        url = url
        browser.get(url)

        #----------------Save to local
        file_object = codecs.open(file_name, "w", "utf-8")
        html = browser.page_source
        file_object.write(html)
        browser.close()
        file_object.close()
        return file_name
    
    #----------------Total Scrapping Function
    def scrapping(file_name):

        lis= []

        with open(file_name, encoding="utf-8") as f:
            data = f.read()
            soup = BeautifulSoup(data, 'html.parser')
            page = soup.find("section", {"id":"mc_content", "class":"clearfix"})
            f.close()

        page = page.find("section",{"class":"technical_anl", "id":"pc_technical"})
        page = page.find("div", {"class":"main_wrapper_res"})
        page = page.find("div", {"class":"tab-content"})
        page = page.find("div", {"class":"tab-pane fade in active", "id":"techan_daily"})
        page = page.find("div", {"class":"clearfix mt20"})
        page = page.find("div", {"class":"techrating tecinD"})

        #----------------Heading
        head = page.findAll("div", {"class":"heade14txt"})[0].text
        heading = head.split()[0:2]
        heading = heading[0]+" "+heading[1]
        heading = heading.title()

        #----------------Table
        tabl = page.find("div", {"class":"mt15 CTR pb20"})
        tabl = tabl.find("div", {"class":"mt15"})
        tabl = tabl.find("table", {"class":"mctable1"}).findAll("tr")

        row = {}
        for i in range(0, len(tabl)):
            row.update({tabl[i].findAll("td")[0].text:tabl[i].findAll("td")[1].text})

        #----------------DataFrame
        data = pd.DataFrame(row.items(), columns=(heading,None))
        data = data.set_index(data.columns[0])
        print(data)

        #----------------Save to CSV
        data.to_csv('index.csv')
        
    #----------------Function Calling
    url = urls
    html_name = file_saving(url)
    scrapping(html_name)
    
    #----------------HTML File Delete
    os.remove(html_name)

web_scrapping("https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/yesbank/YB")