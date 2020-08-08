import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

#Connecting Driver
driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.maximize_window()

#URL and Xpaths
companyDetailurl = "https://www.indeed.co.in/Top-Rated-Workplaces/2019-IN-Technology"
indeedUrl = "https://www.indeed.co.in/"

driver.get("https://www.indeed.co.in/cmp/SAP?attributionid=discovery")
companyDetails = BeautifulSoup(driver.page_source,"lxml")
print(companyDetails)