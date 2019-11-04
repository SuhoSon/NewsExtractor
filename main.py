import pickle
import time

import crawling
import excel_maker
import noun_extractor
import option_parser

option_dict = option_parser.Option_Parser().start()

start = time.time()
print(">> 분석 시작... 페이지 수: {0}, 시작 날짜: {1}, 종료 날짜: {2}, 크롤링 파일: \"{3}\""
      .format(option_dict['pages'], option_dict['start'], option_dict['end'], option_dict['crawler']))

print(">> 크롤링 시작...")
crawling_start = time.time()
if option_dict['crawler'] is None:
    enews = crawling.Economic_Article(option_dict)
    enews.start()

    crawling_list = enews.crawling_list
else:
    print("Skipped...(\"{0}\")".format(option_dict['crawler']))
    with open(option_dict['crawler'], 'rb') as handle:
        crawling_list = pickle.load(handle)
print(">> 크롤링 종료. " + "걸린 시간: {0:.2f}s\n".format(time.time() - crawling_start))

if option_dict['crawler'] is None:
    filename = "[{0}_{1}_{2}]crawler.dict".format(option_dict['pages'],
                                                  option_dict['start'], option_dict['end'])
    with open(filename, 'wb') as handle:
        pickle.dump(enews.crawling_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

extract_start = time.time()
print(">> 명사 추출 시작...")
noextractor = noun_extractor.Noun_Extractor(crawling_list)
noextractor.start()
print(">> 명사 추출 종료. " + "걸린 시간: {0:.2f}s\n".format(time.time() - extract_start))

filename = "[{0}_{1}_{2}]title_counter.dict".format(option_dict['pages'],
                            option_dict['start'], option_dict['end'])
with open(filename, 'wb') as handle:
    pickle.dump(noextractor.title_counter, handle, protocol=pickle.HIGHEST_PROTOCOL)

filename = "[{0}_{1}_{2}]body_counter.dict".format(option_dict['pages'],
                            option_dict['start'], option_dict['end'])
with open(filename, 'wb') as handle:
    pickle.dump(noextractor.body_counter, handle, protocol=pickle.HIGHEST_PROTOCOL)

excel_start = time.time()
print(">> 엑셀 저장 시작...")
exmaker = excel_maker.Excel_Maker(noextractor, option_dict)
exmaker.start()
print(">> 엑셀 저장 끝. " + "걸린 시간: {0:.2f}s\n".format(time.time() - excel_start))

print(">> 분석 끝. 페이지 수: {0}, 시작 날짜: {1}, 종료 날짜: {2}\n"
      .format(option_dict['pages'], option_dict['start'], option_dict['end'])
      + ">> 걸린 시간: {0:.2f}s\n".format(time.time() - start))
