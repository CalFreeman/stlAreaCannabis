import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from random import randint

chromedriver_path = "/usr/bin/chromedriver"
service = Service(chromedriver_path)
options = Options()
# options.headless = Tree #makes it not pop up
options.add_argument("--incognito")
options.add_argument("--start-maximized")
driver = webdriver.Chrome()
driver.maximize_window()

url = "https://dutchie.com/embedded-menu/swade-cannabis-dispensary-st-peters/products/flower"

driver.get(url)
sleep(3)

last_height = driver.execute_script("return document.body.scrollHeight")
sleep(1)

while True:
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
  new_height = driver.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
      break
  last_height = new_height
  sleep(0.5)

driver.execute_script("document.body.style.zoom='50%'")
sleep(1)
driver.execute_script("document.body.style.zoom='100%'")

sleep(1)
html_source = driver.page_source
driver.quit()

soup = BeautifulSoup(html_source, 'html.parser')
##Prints Name
for divs in soup.find_all("span", {"class": 'desktop-product-list-item__ProductName-sc-8wto4u-7'}):
  find_all=divs
  print(find_all.text)

###Prints Name
# for divs in soup.find_all("span", {"class": 'product-list__Container-sc-1arkwfu-1'}):
#   find_all=divs
#   print(find_all.text)
#   a = soup.find_all("span", {"class": 'desktop-product-list-item__ProductBrand-sc-8wto4u-6'})
#   b = divs.find_all("div", {"class": 'desktop-product-list-item__PotencyInfo-sc-8wto4u-14'})
#   print(a.text)
#   print(b.text)


###Prints Brand
for spans in soup.find_all("span", {"class": 'desktop-product-list-item__ProductBrand-sc-8wto4u-6'}):
  find_all=spans
  print(find_all.text)

# ###Prints Potency
# for divs2 in soup.find_all("div", {"class": 'desktop-product-list-item__PotencyInfo-sc-8wto4u-14'}):
#   find_all=divs2
#   print(find_all.text)

# ##Prints Weight
# for divs in soup.find_all("span", {"class": "weight-tile__Label-otzu8j-4"}):
#  find_all=divs
#  print(find_all.text)

##Prints prices
for divs in soup.find_all("span", {"class": "weight-tile__PriceText-otzu8j-5"}):
 find_all=divs
 print(find_all.text)

# for tag in soup.find_all("div", {"class": 'desktop-product-list-item__Container-sc-8wto4u-0 jTzrhU'}):
#   print(tag.text)
#   a = div
  #for element in tag.find_all("div", {"class": "desktop-product-list-item__Container-sc-8wto4u-0 jTzrhU"}):
    #print(element.text)
        # for divEle in element.findAll('div')
        #     a = divEle.find("span", {"class": "caption"}).text
        #     b = divEle.find("span", {"class": "as-of-date"}).text
        #     c = divEle.find("span", {"class": "data"}).text