import requests
from bs4 import BeautifulSoup
import threading
import re

number = 1
url_list = list()
email_regex = re.compile("[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")

email_list = []
import re
while True:
    rq_ = requests.get('https://www.python.org.ar/trabajo/?page='+str(number))
    if rq_.status_code != 200:
        break
    else:
        number += 1
    soup = BeautifulSoup(rq_.text,'html.parser')
    jobs_div = soup.find('div','col-md-8')
    h4_titles = soup.findAll('h4')
    for title in h4_titles:
        url_list.append('https://www.python.org.ar'+title.find('a').get('href'))
def thread_scraping():
    while url_list != []:
        url = url_list.pop()
        rq_ = requests.get(url)
        soup = BeautifulSoup(rq_.text,'html.parser')
        article = soup.find('article','list-group-item')
        dd_list = article.findAll('dd')
        for dd in dd_list:
            if email_regex.search(dd.text):
                if email_regex.search(dd.text).group() not in email_list:
                    email_list.append(email_regex.search(dd.text).group())

t_1 = threading.Thread(target=thread_scraping,name="t_1")
t_2 = threading.Thread(target=thread_scraping,name="t_2")
t_3 = threading.Thread(target=thread_scraping,name="t_3")
t_4 = threading.Thread(target=thread_scraping,name="t_4")

t_1.start()
t_2.start()
t_1.join()
t_2.join()
with open('emails.txt','a') as f:
    for element in email_list:
        f.write(element+', ')
