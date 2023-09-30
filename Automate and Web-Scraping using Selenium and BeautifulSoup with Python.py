from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import requests
import html5lib
import pandas as pd


#AUTOMATION USING SELENIUM WITH PYTHON............................

options = Options()
s = Service(r'C:\Users\My PC\Documents\Projects_Python\chromedriver.exe')
driver = webdriver.Chrome(service=s,options=options)
driver.get('https://imdb.com')

wait = WebDriverWait(driver, 10)
dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ipc-icon.ipc-icon--arrow-drop-down.ipc-btn__icon.ipc-btn__icon--post.navbar__flyout__text-button-post-icon")))
dropdown.click()
sleep(1)

link = driver.find_element(By.LINK_TEXT, "Advanced Search")
link.click()
sleep(1)

Search = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/div[2]/div[1]/a")
Search.click()
sleep(1)

Tv_movie = driver.find_element(By.ID, "title_type-1")
Tv_movie.click()
sleep(1)

Video = driver.find_element(By.ID, "title_type-2")
Video.click()
sleep(1)

Release_date_min = driver.find_element(By.NAME, "release_date-min")
Release_date_min.click()
Release_date_min.send_keys('1990')
sleep(1)

Release_date_min = driver.find_element(By.NAME, "release_date-max")
Release_date_min.click()
Release_date_min.send_keys('2020')
sleep(1)

min_rate = driver.find_element(By.NAME, "user_rating-min")
min_rate.click()
dropdown_2 = Select(min_rate)
dropdown_2.select_by_visible_text('1.1')
sleep(1)

max_rate = driver.find_element(By.NAME, "user_rating-max")
max_rate.click()
dropdown_3 = Select(max_rate)
dropdown_3.select_by_visible_text('10')
sleep(1)

Oscar = driver.find_element(By.ID, "groups-7")
Oscar.click()
sleep(1)

Color = driver.find_element(By.ID, "colors-1")
Color.click()
sleep(1)

language = driver.find_element(By.NAME, "languages")
dropdown_5 = Select(language)
dropdown_5.select_by_visible_text('English')
sleep(1)

Display = driver.find_element(By.NAME, "count")
dropdown_6 = Select(Display)
dropdown_6.select_by_index(2)
sleep(1)

submit = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/form/div/p[3]/button")
submit.click()
sleep(1)

current_url = driver.current_url


#WEB-SCRAPING OF AUTOMATED-DATA BY BEAUTIFULSOUP WITH PYTHON......................

Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
data = requests.get(current_url, headers=Headers)
soup = BeautifulSoup(data.text, "html.parser")

list_items = soup.find_all('div',{'class':'lister-item'})
len(list_items)

title = [result.find('h3').find('a').get_text() for result in list_items]
year = [result.find('h3').find('span',class_='lister-item-year').get_text().strip('()') for result in list_items]
duration = [result.find('span',class_='runtime').get_text() for result in list_items]
genre = [result.find('span',class_='genre').get_text().strip() for result in list_items]
rating = [result.find('div',class_='ratings-imdb-rating').get_text().strip() for result in list_items]

imdb_df = pd.DataFrame({'Movie Title':title,'Year':year,'Duration':duration,'Genre':genre,'Rating':rating})
imdb_df.to_excel("IMDB_Search_Result.xlsx",index=False)