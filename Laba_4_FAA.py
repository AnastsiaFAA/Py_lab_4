#Используя Python  и библиотеки Queue и Thread, а так же код из 3 задания, 
#написать скрипт, который создает фоновый поток и в нем периодично обновляет страницу 
#новостного агенства и отслеживает новые новости(которые ещё не выводились). 
#Фоновый поток использует объект очередь для передачи в основной поток новый новостей. 
#Новости выводятся на печать из основного потока.
import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
import time
import datetime


def get_posts(url, queue):
    while True:

        PageHTML = requests.get(url).text          #получить инфу со страницы в виде текста
        Soup = BeautifulSoup(PageHTML, "html.parser") #представить как вложенную структуру данных
        posts = []      #создается список "посты"

        for i in Soup.find_all("div", "story__main"):
                      #ищет в html-коде класс "story_main"             
            tagos = []
            title = []
            author = []
            for titles in i.find_all("a", "story__title-link "):
                title = titles.text
            for tags in i.find_all("a", "story__tag"): #ищет теги
                tag = tags.get_text()                  #изклекает текст из класса теги
                tagos.append(tag[9:-8])                #добавляет в список, обрезая лишнее
            for authors in i.find_all("a", "story__author"):
                author = authors.get_text()
            #в список "посты" для каждого класса "story_main" добавляется словарь с такими ключами:
            posts.append({'Title:': title, "Tags:": tagos, "Author:": author})
            #обработка исключения
            try:                        #предложение-инструкция
                if title not in all_titles:
                    all_titles.add(title)

                    queue.put({'Author:': author,
                               'Title:': title,
                               'Tags:': tagos})
            except TypeError:   #операция применена к объекту несоответствующего типа
                pass       #остановка

        time.sleep(10)  #каждые 10сек обновляет новости


if __name__ == "__main__":
    queue = Queue()
    url = 'https://pikabu.ru/'
    thread = Thread(target=get_posts, args=(url, queue))
    thread.start()
    all_titles = set()

    while True:
        if queue.empty():
            
            pass
        else:
            while not queue.empty():
                print(queue.get())
                print(datetime.datetime.now())
        time.sleep(0)  
        
