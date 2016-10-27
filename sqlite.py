import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('pars_b.sqlite')
c = conn.cursor()

#Получаем название категории по её id
def pars_theme_name(id_theme):
    url_theme = 'http://www.e1.ru/news/spool/section_id-%s.html' % (id_theme)
    news = requests.get(url_theme)
    soup = BeautifulSoup(news.text, 'html.parser')
    soup.prettify()

    name_theme = soup.findAll('strong', {"class": "block_title"})
    #print(name_theme[2].get_text())
    name_theme = name_theme[2].get_text()
    return name_theme

#pars_theme_name(151)

'''
def add_data(id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number):
    c.execute("INSERT INTO pars (id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id_theme, url_news, words_in_title, words_in_article, words_in_description, images_number, links_number, views_number, comments_number))
    conn.commit()

#add_data('37', 'http://www.e1.ru/news/spool/news_id-443300-section_id-37.html', '11', '177', '52', '1', '0', '12978', '78')
'''
def select_data_in_consol(id_theme):
    c.execute("SELECT * FROM pars WHERE id_theme = '%s'" %id_theme)
    row = c.fetchone()
    while row is not None:
        print('id: \t\t\t',str(row[0]))
        print('id_theme: \t\t\t', str(row[1]))
        print('url_news: \t\t\t', str(row[2]))
        print('слов в заголовке: \t\t\t', str(row[3]))
        print('слов в статье: \t\t\t\t', str(row[4]))
        print('слов в описании: \t\t\t', str(row[5]))
        print('количество изображений: \t', str(row[6]))
        print('количетсво ссылок: \t\t\t', str(row[7]))
        print('количество просмотров: \t\t', str(row[8]))
        print('количество комментариев: \t', str(row[9]))
        print('\n')

        row = c.fetchone()
#select_data_in_consol(73)

def select_count_news_all():
    c.execute("SELECT COUNT(*) FROM pars")
    row = c.fetchone()
    return row[0]
#print(select_count_news_all())

def select_count_news(id_theme):
    c.execute("SELECT COUNT(*) FROM pars WHERE id_theme = '%s'" % id_theme)
    row = c.fetchone()
    return row[0]
#print(select_count_news(157))

def select_count_news_in_consol(id_theme):
    c.execute("SELECT COUNT(*) FROM pars WHERE id_theme = '%s'" % id_theme)
    row = c.fetchone()
    print('Новостей в категории', pars_theme_name(id_theme), ': ', row[0])
#select_count_news_in_consol(157)


def count_news_in_theme():
    select_count_news(37) #технологии и интернет
    select_count_news(73) #автоновости
    select_count_news(158) #бизнес
    select_count_news(15) #в верхах
    select_count_news(96) #вкусно сегодня
    select_count_news(105) #город
    select_count_news(143) #дом
    select_count_news(157) #дороги
    select_count_news(168) #дорожное видео
    select_count_news(9) # здоровье
    select_count_news(147) # интервью
    select_count_news(162) # конкурс
    select_count_news(1) # культура
    select_count_news(117) # осень
    select_count_news(151) # мнение
    select_count_news(144) # недвижимость
    select_count_news(164) # неизвестный екб
    select_count_news(88) # новости сообщества е1
    select_count_news(150) # обзор
    select_count_news(33) # образование и работа
    select_count_news(17) # общество
    select_count_news(7) # отдых
    select_count_news(160) # подробности
    select_count_news(142) # покупки
    select_count_news(13) # происшествия
    select_count_news(149) # расследования
    select_count_news(140) # репортаж
    select_count_news(5) # спорт
    select_count_news(141) # стиль
    select_count_news(86) # страна и мир
    select_count_news(87) # суды и криминал
    select_count_news(185) # тесты
    select_count_news(11) # экономика
    select_count_news(161) # эксклюзив
    select_count_news(148) # эксперимент
    select_count_news(181) # фоторепортаж

def count_news_in_theme_in_consol():
    select_count_news_in_consol(37)  # тех	нологии и интернет
    select_count_news_in_consol(73)  # автоновости
    select_count_news_in_consol(158)  # бизнес
    select_count_news_in_consol(15)  # в верхах
    select_count_news_in_consol(96)  # вкусно сегодня
    select_count_news_in_consol(105)  # город
    select_count_news_in_consol(143)  # дом
    select_count_news_in_consol(157)  # дороги
    select_count_news_in_consol(168)  # дорожное видео
    select_count_news_in_consol(9)  # здоровье
    select_count_news_in_consol(147)  # интервью
    select_count_news_in_consol(162)  # конкурс
    select_count_news_in_consol(1)  # культура
    select_count_news_in_consol(117)  # осень
    select_count_news_in_consol(151)  # мнение
    select_count_news_in_consol(144)  # недвижимость
    select_count_news_in_consol(164)  # неизвестный екб
    select_count_news_in_consol(88)  # новости сообщества е1
    select_count_news_in_consol(150)  # обзор
    select_count_news_in_consol(33)  # образование и работа
    select_count_news_in_consol(17)  # общество
    select_count_news_in_consol(7)  # отдых
    select_count_news_in_consol(160)  # подробности
    select_count_news_in_consol(142)  # покупки
    select_count_news_in_consol(13)  # происшествия
    select_count_news_in_consol(149)  # расследования
    select_count_news_in_consol(140)  # репортаж
    select_count_news_in_consol(5)  # спорт
    select_count_news_in_consol(141)  # стиль
    select_count_news_in_consol(86)  # страна и мир
    select_count_news_in_consol(87)  # суды и криминал
    select_count_news_in_consol(185)  # тесты
    select_count_news_in_consol(11)  # экономика
    select_count_news_in_consol(161)  # эксклюзив
    select_count_news_in_consol(148)  # эксперимент
    select_count_news_in_consol(181)  # фоторепортаж


#count_news_in_theme()
count_news_in_theme_in_consol()
c.close()
conn.close()


'''
37  # технологии и интернет
73  # автоновости
158 # бизнес
15  # в верхах
96  # вкусно сегодня
105 # город
143 # дом
157 # дороги
168 # дорожное видео
9   # здоровье
147 # интервью
162 # конкурс
1   # культура
117 # осень
151 # мнение
144 # недвижимость
164 # неизвестный екб
88  # новости сообщества е1
150 # обзор
33  # образование и работа
17  # общество
7   # отдых
160 # подробности
142 # покупки
13  # происшествия
149 # расследования
140 # репортаж
5   # спорт
141 # стиль
86  # страна и мир
87  # суды и криминал
185 # тесты
11  # экономика
161 # эксклюзив
148 # эксперимент
181 # фоторепортаж

'''