import threading
from collections import Counter

from konlpy.tag import Kkma

exceptions = ["기자"]


class Noun_Extractor:
    def __init__(self, articles):
        super().__init__()

        self.articles = articles
        self.title_nouns = {}
        self.body_nouns = {}
        self.title_counter = {}
        self.body_counter = {}

    def start(self):
        spliter = Kkma()

        for date in sorted(self.articles.keys()):
            title_nouns = {}
            body_nouns = {}
            title_counter = []
            body_counter = []

            extract_threads = []
            for article in self.articles[date]:
                self.article_extract(date, spliter, article, title_nouns,
                                     title_counter, body_nouns, body_counter, extract_threads)

            for extract_thread in extract_threads:
                extract_thread.join()

            self.title_nouns[date] = title_nouns
            self.body_nouns[date] = body_nouns

            self.counting(date, title_counter, self.title_counter)
            self.counting(date, body_counter, self.body_counter)

    def article_extract(self, date, spliter, article, title_nouns,
                        title_counter, body_nouns, body_counter, extract_threads):
        title_extract_thread = threading.Thread(target=self.extract,
                                                args=(date, spliter, article, 'title', title_nouns, title_counter))
        body_extract_thread = threading.Thread(target=self.extract,
                                               args=(date, spliter, article, 'body', body_nouns, body_counter))
        extract_threads.append(title_extract_thread)
        extract_threads.append(body_extract_thread)
        title_extract_thread.start()
        body_extract_thread.start()

    def extract(self, date, spliter, article, target, nouns_list, counter):
        extracted = spliter.nouns(article[target])

        if article['media'] in extracted:
            extracted = list(filter(lambda word: word != article['media'], extracted))

        for exception in exceptions:
            extracted = list(filter(lambda word: word != exception, extracted))

        counter.extend(extracted)

        if article['media'] in nouns_list.keys():
            nouns_list[article['media']].extend(extracted)
        else:
            nouns_list[article['media']] = extracted

        print("[{0}]추출 중... {1}".format(date, article['title']))

    def counting(self, date, nouns, list):
        count = Counter(nouns)
        list[date] = count
