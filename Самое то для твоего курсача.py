#!/usr/bin/env python
# coding: utf-8

# # ИНСТРУКЦИЯ
# 
# данный парсер в существующей модификации работает с киберленинкой
# 
# все, что тебе нужно поменять для успешного парсинга это:
# путь к драйверу браузера, через который будешь парсить(в моем случае гугл хром)
# и ссылку на киберленинку с готовым тематическим поисковым запросом
# (для наглядного понимания, вставь мою ссылку с киберленинки в поисковик, 
# поймешь что нужно сделать сразу же:))) я парсил тему "криптоэкономика"
# 
# готово! теперь у тебя есть табличка с краткой характеристикой каждой тематической
# статьи + таблица рейтинга популярности ключевых слов в рамках всех спарсеных статей
# 
# *последняя таблица тебе будет нужна для оценки качества своего тематического запроса,
# проверь, подходит ли сформированный рейтинг под твои требования, прежде чем начинать 
# работу с полученными статьями, может быть тебе потребуется изменить свой поисковой запрос)

# In[ ]:



from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from tqdm.notebook import tqdm
import time
from random import uniform
from selenium.webdriver.common.by import By

chromedriver = '/Users/user/Desktop/chromedriver' #укажи путь к драйверу(например для парсинга через хром)
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
browser = webdriver.Chrome(ChromeDriverManager().install(), options = options)

pages_inf = []

index = 0

#ставь ссылку на главную страницу киберленинки при введеном нужном поисковом запросе#
link = 'https://cyberleninka.ru/search?q=%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0&page=1'
browser.get(link)
time.sleep(uniform(1,3))
browser.find_element(By.XPATH,'//*[@id="search-box-full"]/div[1]/fieldset/input[2]').click()
time.sleep(uniform(2,3))

index = 2

for x in tqdm(range(0, 153)):
    pages_inf.append(BeautifulSoup(browser.page_source))
    #ту же ссылку что и выше, но после page= оборви ее#
    link = 'https://cyberleninka.ru/search?q=%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0&page=' + str(index)
    browser.get(link)
    time.sleep(uniform(1.5,2.5))
    index += 1
    
art_links = []

for page in tqdm(pages_inf):
    art_links.extend(['https://cyberleninka.ru' + x.find('a').get('href') for x in page.findAll('h2', {'class':'title'})])

from collections import Counter

titles = []
spechialitis = []
authers = []
views = []
jurnals = []
keywords = []
all_keywords = []
years = []
abstacts = []

chromedriver = '/Users/user/Desktop/chromedriver'#снова путь к драйверу
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

for link in tqdm(sorted(art_links)):
    try:
        browser.get(link)
        time.sleep(uniform(2,3))
        inf = browser.page_source
        title = BeautifulSoup(inf).find('div',{'class':'main'}).find('h1').find('i').text.lower().strip()
        spechialiti = BeautifulSoup(inf).find('div',{'class':'main'}).find('div', {'class':'half-right'}).find('a').text.lower().strip()
        auther = BeautifulSoup(inf).find('div',{'class':'main'}).find('li', {'itemprop':'author'}).text.lower().strip()
        view = BeautifulSoup(inf).find('div',{'class':'main'}).find('div', {'class':'statitem views'}).text.lower().strip()
        jurnal = BeautifulSoup(inf).find('div',{'class':'main'}).find('div', {'class':'half'}).find('span').text.lower().strip()
        keyword = [x.text.lower().strip() for x in BeautifulSoup(inf).find('div',{'class':'main'}).find('div', {'class':'full keywords'}).find('i').findAll('span')]
        year = BeautifulSoup(inf).find('div',{'class':'main'}).find('div', {'class':'label year'}).find('time').text.lower().strip()
        abstact = BeautifulSoup(inf).find('div',{'class':'main'}).find('div', {'class':'full abstract'}).find('p').text.lower().strip()
        titles.append(title)
        spechialitis.append(spechialiti)
        authers.append(auther)
        views.append(view)
        jurnals.append(jurnal)
        keywords.append(keyword)
        all_keywords.extend(keyword)
        years.append(year)
        abstacts.append(abstact)
    except:
        continue
#ну вот и итог, получаем две таблицы в ек
df_1 = pd.DataFrame(list(zip(titles,spechialitis,authers,views,jurnals,keywords,years,abstacts)))
df_1.to_excel('Научные_статьи_криптоэкономика.xlsx')

df_2 = pd.DataFrame(dict(Counter(all_keywords)).items())
df_2.to_excel('Ключевые_слова_статей_криптоэкономика.xlsx

