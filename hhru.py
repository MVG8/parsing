import scrapy
from  scrapy.http import HtmlResponse  #  для определения класса
from jobparser.items import JobparserItem



class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']  #  скобки ограничивают область работы паука
    start_urls = ['https://hh.ru/search/vacancy?area=76&fromSearchLine=true&st=searchVacancy&items_on_page=20&text=python']  # точка входа

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='vacancy-serp-item]")
        next_page = response.xpath("//a[@data-qa='parser-next']/@href").extract_first()

        for link in links:
            name = link.xpath(".//a[@class='bloko-link']/text()").get()
           _link = link.xpath(".a[@class='bloko-link']/@href").get()
            salary = link.xpath(".//span[@data-qa='vacancy-serp__vacansy-compensation']/text()").get()
            site = 'https://hh.ru'
            yield JobparserItem(name=name, _link=_link, salary=salary, site=site)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
