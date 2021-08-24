# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import hashlib
from random import getrandbits
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client['vacansy_hhry']
    def process_item(self, item, spider):
        vacancy_info = dict()
        vacancy_info = ['name'] = item['name']  #  имя
        vacancy_info = ['_link'] = item['_link']  #  ссылка на вакансию
        vacancy_info = ['salary_min'] = 0  #  минимальная зарплата
        vacancy_info = ['salary_max'] = 0 #  максимальная зарплата
        vacancy_info = ['salary_valuta'] = ''  #  валюта з/п
        vacancy_info = ['site'] = item['site']

        vacancy_salary = item['salary'].split()
        if vacancy_salary[0] == 'от':
            vacancy_info['salary_min'] = int(f'{vacancy_salary[1]}{vacancy_salary[2]}')
        elif vacancy_salary[0] == 'до':
            vacancy_info['salary_max'] = int(f'{vacancy_salary[1]}{vacancy_salary[2]}')
        else:
            vacancy_info['salary_min'] = int(f'{vacancy_salary[0]}{vacancy_salary[1]}')
            vacancy_info['salary_max'] = int(f'{vacancy_salary[3]}{vacancy_salary[4]}')
        vacancy_info['salary_valuta'] = vacancy_salary[-1]
        vacancy_info['_id'] = hashlib.sha1(str(vacancy_info.encode()).hexdigest())
        # сложим все в базу
        collections = self.mongobase[spider.name]
        collections.update_one({'_id': {'$eq': vacancy_info['_id']}}, {'$set': vacancy_info}, upsert=True)
        return vacancy_info
