# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД
# Минимум один сайт, максимум - все три
from lxml import html
import requests
from pymongo import MongoClien
###################################-new.mail.ru-#####################################

def get_news_mail_ru():

    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
    news_mail = []
    response = requests.get('https://news.mail.ru', headers=headers)
    dom = html.fromstring(response.text)
    news_photo = dom.xpath("//div[contains(@class, 'daynews__item')]")
    mnews = []
    for news in news_photo:
        new_link = news.xpath(".//a/@href")
        mnews.append(new_link)
    news_txt = dom.xpath(".//li[@class = 'list__item']")
    for news in news_txt:
        new_link = news.xpath(".//a/@href")
        mnews.append(new_link)
    for link in mnews:
        response_link = requests.get(link[0], headers=headers)
        dom = html.fromstring(response_link.text)
        news_page = dom.xpath("//div[@class='article js-article js-module']")
        for news in news_page:
            news_dict = {}
            news_dict['source'] = news.xpath("//span[@class= 'link__text']/text()")[0]
            news_dict['title'] = news.xpath(".//h1/text()")[0].replace("\xa0", " ")
            news_dict['link'] = link[0]
            news_dict['date'] = news.xpath(".//span/@datetime")[0]
            news_mail.append(news_dict)
    return news_mail

####################################-lenta.ru-#####################
def get_news_lenta_ru():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
    news_lenta = []
    response = requests.get('https://lenta.ru/', headers=headers)
    dom = html.fromstring(response.text)
    new_dom = dom.xpath("//section[contains(@class, 'for-main')]//a[not(@class)]")

    for news in new_dom:
        news_dict = {}
        news_dict['sourse'] = 'lenta.ru'
        news_dict['title'] = news.xpath(".text()")[1].replace("\xa0", " ")
        news_dict['link'] = "https://lenta.ru/" + news.xpath(".//time/@datetime")[0]
        news['date'] = news.xpath(".//time/@datetime")[0]
        news_lenta.append(news_dict)
    return news_lenta
#
# ###########################-yandex.news-##################
def get_news_yandex_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
    news_lenta = []
    response = requests.get('https://news.yandex.ru/news/', headers=headers)
    dom = html.fromstring(response.text)
    news_dom = dom.xpath("//article[contains(@class, 'mg-card')]")
    for news in news_dom:
        news_dict = {}
        news_dict['source'] = news.xpath(".//a[@class='mg-card__source-link']/text()")[0]
        news_dict['title'] = news.xpath(".//h2/text()")[0].replace("\xa0", " ")
        news_dict['link'] = news.xpath(".//a[@class='mg-card__link']/@href")[0]
        news_dict['data'] = news.xpath(".//span[@class='mg-card-sours__time']/text()")[0]
        news_lenta.append(news_dict)
    return news_lenta

#################-Сложить собранные данные в базу данных-#############
def db_news_add_new(db, *new_block):
    n = 0
    for news in new_block:
        if db.find_one({'link': news['link']}):
            continue
        else:
            db.insert_one(news)
            n += 1
    print(f'Новостей добавлено {n}')
news_block = []
news_block.extend(get_news_mail_ru())
news_block.extend(get_news_lenta_ru())
news_block.extend(get_news_yandex_news())
client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news = db.news

db_news_add_new(news, *news_block)


#
# from lxml import html
# import requests
# from pymongo import MongoClient
#
#
# def get_new_mail_ru():
#     url = 'https://news.mail.ru'
#     headers = {
#        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
#     news_mail = []
#     response = requests.get('https://news.mail.ru', headers=headers)
#     dom = html.fromstring(response.text)
#     news_photo = dom.xpath("//div[contains(@class, 'daynews__item')]")
#     mnews = []
#     for news in news_photo:
#         new_link = news.xpath(".//a/@href")
#         mnews.append(new_link)
#     news_txt = dom.xpath(".//li[@class = 'list__item']")
#     for news in news_txt:
#         new_link = news.xpath(".//a/@href")
#         mnews.append(new_link)
#     for link in mnews:
#         response_link = requests.get(link[0], headers=headers)
#         dom = html.fromstring(response_link.text)
#         news_page = dom.xpath("//div[@class='article js-article js-module']")
#         for news in news_page:
#             news_dict = {}
#             news_dict['source'] = news.xpath(".//span[@class= 'link__text']/text()")[0]
#             news_dict['title'] = news.xpath(".//h1/text()")[0].replace("\xa0", " ")
#             news_dict['link'] = link[0]
#             news_dict['date'] = news.xpath(".//span/@datetime")[0]
#             news_mail.append(news_dict)
#    # print(1)
#     return news_mail
#
#
# def db_news_add_new(db, *new_block):
#     n = 0
#     for news in new_block:
#         if db.find_one({'link': news['link']}):
#             continue
#         else:
#             db.insert_one(news)
#             n += 1
#     print(f'Новостей добавлено {n}')
#
#
# news_block = []
# news_block.extend(get_new_mail_ru())
# client = MongoClient('127.0.0.1', 27017)
# db = client['news_db']
# news = db.news
#
# db_news_add_new(news, *news_block)