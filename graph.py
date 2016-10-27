import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

news_idG = []
views_numberG =[]
comment_numberG =[]

def graphics(news_idG, views_numberG, comment_numberG):
    print(news_idG)
    print(views_numberG)
    print(comment_numberG)

    f, (ax1) = plt.subplots(1, 1, figsize=(12, 8), sharex=True)
    sns.barplot(news_idG, views_numberG, palette="BuGn_d", ax=ax1)
    ax1.set_ylabel("Просмотры")

    sns.despine(bottom=True)
    plt.setp(f.axes, yticks=[])
    plt.tight_layout(h_pad=4)

    f, (ax2) = plt.subplots(1, 1, figsize=(12, 8), sharex=True)
    sns.barplot(news_idG, comment_numberG, palette="RdBu_r", ax=ax2)
    ax2.set_ylabel("Коментарии")

    sns.despine(bottom=True)
    plt.setp(f.axes, yticks=[])
    plt.tight_layout(h_pad=2)

    plt.show()


conn = sqlite3.connect('pars.sqlite')
c = conn.cursor()

#получаем данные из sqlite
def select_data_news_for_graph(id_theme):
    c.execute("SELECT * FROM pars WHERE id_theme = '%s'" % id_theme)
    row = c.fetchone()
    while row is not None:
        news_idG.append(str(row[0]))
        views_numberG.append(int(row[9]))
        comment_numberG.append(int(row[10]))

        row = c.fetchone()
    graphics(news_idG, views_numberG, comment_numberG)

select_data_news_for_graph(37)
c.close()
conn.close()
