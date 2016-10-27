# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from multiprocessing import Pool
import time

#замеряем время работы скрипта
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print ("Время выполнения скрипта: {:.3f} секунд".format(time.time() - self._startTime))

#write_to_base = "on"
write_to_base = "off"

conn = sqlite3.connect('pars.sqlite')
c = conn.cursor()
# функция парсинга новости
def pars_news_page(url_news):
    #получаем код страницы
    news = requests.get(url_news)
    soup = BeautifulSoup(news.text, 'html.parser')
    soup.prettify()
    if(soup.find('div', {"id": "newscontent"})):
        #количество слов в заголовке
        words_in_title = len(soup.html.head.title.string.split())

        #получаем количество слов в статье
        news_sourse = soup.find('div', {"id": "newscontent"}).get_text()
        words_in_article = len(news_sourse.split())

        #получаем количество слов в дескрипшне
        words_in_description = len(soup.find('meta', {"property": "og:description"}).get('content').split())

        #Получаем количество картинок в новости
        images_number = len(soup.findAll('img', {"class": "m-box-news__photo js-m-photo-image"}))

        #Получаем количество ссылок на похожие новости
        if soup.findAll('blockquote'):
            links_number = soup('blockquote')[0]
            links_number = len(links_number.findAll('a', {"class": "news", "title": True}))
        else:
            links_number = 0

        #получаем количество просмотров
        views_number = soup.findAll('strong', {"class": "small_black"})
        views_number = views_number[1].get_text()

        # получаем количество комментариев
        comments_number = soup.findAll('strong', {"class": "small_black"})
        if (len(comments_number) <= 2):
            comments_number = 0
        else:
            comments_number=comments_number[2].get_text()
            comments_number = re.split(r'[()]', comments_number)[1]

        return 1, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number
    else:
        words_in_title = 0
        words_in_article = 0
        words_in_description = 0
        images_number = 0
        links_number = 0
        views_number = 0
        comments_number = 0
        return 404, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number

#функция добавления данных в БД
def add_data(id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number):
        c.execute("INSERT INTO pars (id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number))
        conn.commit()

# функция отрисовки в консоли результатов парсинга новости, запись данных в sqlite
def get_data_pars_news_page(url_news, id_theme):
    status, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number = pars_news_page(url_news)
    if (status!=404):
        print('id_theme: \t\t\t', id_theme)
        print('url_news: \t\t\t', url_news)
        print('слов в заголовке: \t\t\t', words_in_title)
        print('слов в статье: \t\t\t\t', words_in_article)
        print('слов в описании: \t\t\t', words_in_description)
        print('количество изображений: \t', images_number)
        print('количетсво ссылок: \t\t\t', links_number)
        print('количество просмотров: \t\t', views_number)
        print('количество комментариев: \t', comments_number)
        print('\n')
        if(write_to_base=="on"):
            add_data(id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number)
        elif(write_to_base=="off"):
            print("write_to_base = off")
    else:
        print('нет контента или это не страница с новостью')

# функция парсинга ссылок со страниц со ссылками
def pars_link_on_page(news_url_page, id_theme):
    r = requests.get(news_url_page)
    soup = BeautifulSoup(r.text, 'html.parser')

    if(soup.findAll('a', {"class": "news", "title": True})):
        a_news = soup.findAll('a', {"class": "news", "title": True})
        for n_link in range(len(a_news)):
            link = a_news[n_link].get('href')
            url_news = 'http://www.e1.ru%s' % (link)
            get_data_pars_news_page(url_news, id_theme)

# функция генерации ссылок на страницы со ссылками на новости
def get_link_page(id_theme):
    year = range(15, 16)
    month = range(5, 11)
    day = range(1, 32)
    id_theme = str(id_theme)
    for y in year:
        y=str(y)
        for m in month:
            if (m < 10):
                m1 = '0%d' % (m)
            else:
                m1 = m
                m1 = str(m1)
            for d in day:
                if (d < 10):
                    d1 = '0%d' % (d)
                elif (d >= 10):
                    d1 = d
                    d1 = str(d1)
                news_url_page = 'http://www.e1.ru/news/daily/2016/%s/%s/list-section_id-%s.html' % (m1, d1, id_theme)
                print(news_url_page)
                pars_link_on_page(news_url_page, id_theme)

#функция запуска парсинга
def PARS(id_theme):
    get_link_page(id_theme)

#PARS(37)

def pars_all_theme():
    PARS(37)    # технологии и интернет
    PARS(73)    # автоновости
    PARS(158)   # бизнес
    PARS(15)    # в верхах
    PARS(96)    # вкусно сегодня
    PARS(105)   # город
    PARS(143)   # дом
    PARS(157)   # дороги
    PARS(168)   # дорожное видео
    PARS(9)     # здоровье
    PARS(147)   # интервью
    PARS(162)   # конкурс
    PARS(1)     # культура
    PARS(117)   # осень
    PARS(151)   # мнение
    PARS(144)   # недвижимость
    PARS(164)   # неизвестный екб
    PARS(88)    # новости сообщества е1
    PARS(150)   # обзор
    PARS(33)    # образование и работа
    PARS(17)    # общество
    PARS(7)     # отдых
    PARS(160)   # подробности
    PARS(142)   # покупки
    PARS(13)    # происшествия
    PARS(149)   # расследования
    PARS(140)   # репортаж
    PARS(5)     # спорт
    PARS(141)   # стиль
    PARS(86)    # страна и мир
    PARS(87)    # суды и криминал
    PARS(185)   # тесты
    PARS(11)    # экономика
    PARS(161)   # эксклюзив
    PARS(148)   # эксперимент
    PARS(181)   # фоторепортаж

#pars_all_theme()   #Азтунг! Не запускать просто так! парсится 4695 новостей, около 2х часов!

### ---------- TESTS/trash ---------- ###
#get_data_pars_news_page("http://www.e1.ru/news/spool/news_id-452348-section_id-37.html")
#get_data_pars_news_page("http://www.e1.ru/news/spool/news_id-453572-section_id-37.html")    #0 commetn and 0 links
#get_data_pars_news_page("http://www.e1.ru/news/spool/news_id-0-section_id-37.html")         #infalid page/ not news

#test
#pars_link_on_page('http://www.e1.ru/news/spool/section_id-37.html')

#get_link_page(157) #дороги
#get_link_page(168) #дорожное видео
c.close()
conn.close()
'''
if __name__ == '__main__':
    with Pool(processes=8) as pool:
        with Profiler() as p:
            PARS(148)
'''
with Profiler() as p:
    PARS(148)
