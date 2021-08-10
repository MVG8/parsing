# Парсинг сайта Кинопоиск
# from bs4 import BeautifulSoup as bs
# import requests
# from pprint import pprint
#
# url = 'https://www.kinopoisk.ru'
# params = {'quick_filters': 'serials',
#           'tab': 'all'}
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
#
# response = requests.get(url + '/popular/films/', params=params, headers=headers)
#
# soup = bs(response.text, 'html.parser')
# serial_list = soup.find_all('div', {'class': 'desktop-rating-selection-film-item'})
#
# print()
# serials = []
# for serial in serial_list:
#     serial_data = {}
# serial_info = serial.find('p', {'class': 'section-film-item-meta__name'}).text
# # ссылка на сериал а href
# serial_name = serial_info.getText()
# serial_url = url + serial_info.parent.get('href')
# # Соберем жанр сериала
# serial_genre = serial.find('spam', {'class': 'selection-film-item-metta__metta-additional-item'}).nextSubling.getText()
#
# # Анализ рейтинга
# serial_raiting = serial.find('spam', {'class': 'rating__value'}).getText()
# serial_data['name'] = serial_name
# serial_data['url'] = serial_url
# serial_data['genre'] = serial_genre
# serial_data['raiting'] = serial_raiting
# serial.append(serial_data)
# pprint(serials)

# Домашняя работа
import requests
from bs4 import BeautifulSoup as bs
import json
import re

class HhScrapper:
    '''Скрапер ресурса hh.ru'''
    def __init__(self, url, search_part_url, headers, params):
        self.url = url
        self.search_part_url = search_part_url
        self.headers = headers
        self.params = params
        self.reselt_list = []
    def run(self):
        """Запуск работы скрапера"""
        self.create_response_obj()
        self.create_parser_obj()
        self.fill_result_list()
    def create_response_obj(self):
        """Создаю обьект Response метода GET библиотеки requests"""
        self.response = requests.get(f'{self.url}{self.search_part_url}',
                                    params=self.params, headers=self.headers)
    def create_parser_obj(self):
        """Создаю обьект класса BeautifulSoup."""
        self.soup = bs(self.response.text, 'html.parser')
    def get_entities_list(self):
        """Получаю список с сущностями"""
        entities_list = self.soup.findAll('div', {'class': 'vacancy-serp-item '})
        return entities_list
    def fill_result_list(self):
        """Заполняю результирующий список сданными вакансий."""
        entities_list = self.get_entities_list()
        for entity in entities_list:
            entity_data_dict = self.create_vacancy_dict(entity)
            self.result_list.append(entity_data_dict)
        self.change_page()

    def change_page(self):
        """Сменить страницу"""
        try:
            update_part_url =self.soup.find('a', {'data-qa': 'pager-next'})['href']
        except TypeError:
            self.write_json()
        else:
            self.respons = requests.get(f'{self.url}{update_part_url}', headers=self.headers)
            self.create_parser_obj()
            self.fill_result_list()
    def create_vacancy_dict(self, entity):
        """Создаю словарь с данными текущей вакансии."""
        entity_dict = dict()

        vacancy_name = self.get_vacancy_name(entity)
        entity_dict['vacancy_name'] = vacancy_name

        salary_data_dict = self.get_salary(entity)
        entity_dict['salary'] = salary_data_dict

        link_of_vacancy = self.get_vacancy(entity)
        entity_dict['link_of_vacancy'] = link_of_vacancy

        site_sours = self.get_site_sours()
        entity_dict['site_sours'] = site_sours

        return entity_dict
    def get_vacancy_name(self, entity):
        """Получаю название вакансии"""
        vacancy_name = entity.find('a', {'class': 'bloco-link'}).text
        return vacancy_name
    def get_salary(self, entity):
        """Получаю данные о зарплате минимальная,максимальная ,в какой валюте."""
        salary_elem = entity.find('spam', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary_elem:
            salary_string = entity.find('spam', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            is_interval = re.match('^\d', salary_string)
            if is_interval:
                min_salary = int(''.join(re.findall('(^\d+)\s(\d*)', salary_string)[0]))
                max_salary = int(''.join(re.findall('-\s(\d+)\s(\d*)', salary_string)[0]))
                currency = re.findall('\s(\D+\.?)$', salary_string)[0]
            else:
                min_salary = None
                max_salary = int(''.join(re.findall('\s(\d+)\s(\d*)', salary_string)[0]))
                currency = re.findall('\s(\D+\.?)$', salary_string)[0]
        else:
            min_salary = None
            max_salary = None
            currency = None
        salary_data_dict = {
            'min_salary': min_salary,
            'max_salary': max_salary,
            'currency': currency
        }
        return salary_data_dict

    def get_link_of_vacancy(self, entity):
        '''Получаю ссылку на вакансию'''
        link_of_vacancy = entity.find('a', {'class': 'bloko-link'})['href']
        return link_of_vacancy
    def get_site_sourse(self):
        """Получаю источник ресурса из которого взята вакансия."""
        site_sours = self.url.split('//')[1]
        return site_sours

    def write_json(self):
        """Записать результирующий список с данными вакансий в json файл."""
        with open('hh/hh_data.json', 'w') as f:
            json.dump(self.result_list, f, sort_keys=True, indent=4, ensure_ascii=False)

# ДЛЯ ОТЛАДКИ СКРАППЕРА:
if __name__ == '__main__':
    hh_url = 'https://hh.ru'
    hh_search_part_url = '/search/vacancy'
    hh_params = {
        "area": '1',
        "fromSearchLine": 'true',
        "st": 'searchVacancy',
        "text": 'python'
        }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
    sj_obj = HhScrapper(hh_url, hh_search_part_url, headers, hh_params)
    sj_obj.run()

