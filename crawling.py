import datetime
import threading

import pandas
import requests
from bs4 import BeautifulSoup

MAX_CRAWLING_COUNT = 300


class Economic_Article:
    def __init__(self, option_dict):
        super().__init__()

        self.option_dict = option_dict
        self.url = 'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm'

        self.crawling_list = {}

    def start(self):
        today = datetime.date.today()
        delta_datetime = datetime.timedelta(days=365)

        if self.option_dict['start'] is None:
            self.option_dict['start'] = today - delta_datetime
        if self.option_dict['end'] is None:
            self.option_dict['end'] = today

        dt_index = pandas.date_range(start=str(self.option_dict['start']), end=str(self.option_dict['end']))
        dt_list = dt_index.strftime('%Y%m%d').tolist()

        redundance_list = []
        for date in dt_list:
            self.make_list(date, redundance_list)

    def make_list(self, date, redundance_list):
        crawler_threads = []
        articles = []

        if self.option_dict['pages'] is None or self.option_dict['pages'] == "":
            count = 1
            while count < MAX_CRAWLING_COUNT:
                if self.crawling(date, count, articles, redundance_list, crawler_threads):
                    break
                count += 1
        else:
            for page in range(1, self.option_dict['pages'] + 1):
                self.crawling(date, page, articles, redundance_list, crawler_threads)

        for crawler_thread in crawler_threads:
            crawler_thread.join()

        self.crawling_list[date] = articles

    def crawling(self, date, page, articles, redundance_list, crawler_threads):
        naver_html = requests.get(self.url + "&date=" + date + "&page=" + str(page)).text
        naver_article_list = BeautifulSoup(naver_html, 'html.parser')

        last_page = naver_article_list.find('div', {'class': 'paging'}).text.split("\n")[-2]
        if self.option_dict['pages'] is None or self.option_dict['pages'] == "":
            if last_page != "다음":
                if int(last_page) < page:
                    return True

        for naver_article in naver_article_list.select('dt > a'):
            crawler_thread = threading.Thread(target=self.get_article,
                                              args=(date, naver_article, redundance_list, articles))
            crawler_threads.append(crawler_thread)
            crawler_thread.start()

        return False

    def get_article(self, date, naver_article, redundance_list, articles):
        article_url = naver_article['href']

        if article_url in redundance_list:
            return

        redundance_list.append(article_url)

        article_html = requests.get(article_url).text
        article_soup = BeautifulSoup(article_html, 'html.parser')

        article_title = article_soup.find('h3', {'id': 'articleTitle'}).text

        article_body = article_soup.find('div', {'id': 'articleBodyContents'}).text
        article_body = article_body.split("flash_removeCallback() {}")[1].strip()
        article_body = article_body.split("@")[0].split(".")
        del (article_body[-1])
        article_body = "".join(article_body) + "."
        article_body = article_body.split("▶")[0]

        article_media = article_soup.find('meta', {'property': 'me2:category1'})['content']

        article = {
            'title': article_title,
            'body': article_body,
            'media': article_media,
            'url': article_url
        }

        print("[{0}]{1}".format(date, article['title']))

        articles.append(article)
