import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
import time
import datetime


def get_posts(url, queue):
    while True:

        PageHTML = requests.get(url).text
        Soup = BeautifulSoup(PageHTML, "html.parser")
        posts = []

        for i in Soup.find_all("div", "story__main"):
            # print("\n\t\t\t***\n")
            # print(i)
            tagos = []
            title = []
            author = []
            for titles in i.find_all("a", "story__title-link "):
                title = titles.text
            for tags in i.find_all("a", "story__tag"):
                tag = tags.get_text()
                tagos.append(tag[9:-8])
            for authors in i.find_all("a", "story__author"):
                author = authors.get_text()

            posts.append({'Title:': title, "Tags:": tagos, "Author:": author})

            try:
                if title not in all_titles:
                    all_titles.add(title)

                    queue.put({'Author:': author,
                               'Title:': title,
                               'Tags:': tagos})
            except TypeError:
                pass

        time.sleep(10)  # every 10 sec update news


if __name__ == "__main__":
    queue = Queue()
    url = 'https://pikabu.ru/'
    thread = Thread(target=get_posts, args=(url, queue))
    thread.start()
    all_titles = set()

    while True:
        if queue.empty():
            # print("Новых новостей нет! Проверьте чуть позже" + "\n\n\t\t\t\t\t *******")
            pass
        else:
            while not queue.empty():
                print(queue.get())
                print(datetime.datetime.now())
        time.sleep(0)
        # time.sleep(10) # print one new every 10 secods from queue