import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import random

def scrape():
    #grab the questions from this website
    headers = requests.utils.default_headers()
    headers['user-agent'] = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    r = requests.get('https://www.programcreek.com/2013/08/leetcode-problem-classification/', headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    con = sqlite3.connect('leetcodeq.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS question_list")
    cur.execute("CREATE TABLE question_list (id KEY, title TEXT, content TEXT, link TEXT);")
    question_id = 0
    for txt in soup.select("body p a"):
        if not re.search(r'(?<=\").*/(?=\")', str(txt)):
            continue
        link = re.search(r'(?<=href=\").*/(?=\")', str(txt)).group()
        req = requests.get(link, headers=headers)
        insoup = BeautifulSoup(req.content, 'lxml')
        title = insoup.select("h1 a")[0].get_text()
        for line in insoup.select("div.entrybody p"):
            while line.span:
                line.span.decompose()
        content = "\n".join((x.get_text() for x in insoup.select("div.entrybody")))
        content = re.search(r'[\s\S]*(?=Related posts)', content).group()
        cur.execute("INSERT INTO question_list VALUES (?,?,?,?);", (question_id, title, content, link))
        question_id += 1
        con.commit()
    con.close()

def generate():
    #return random id, title, question
    con = sqlite3.connect('leetcodeq.db')
    cur = con.cursor()
    c = str(random.randint(0,333))
    cur.execute('SELECT * FROM question_list WHERE id == (?);', (c,))
    return cur.fetchone()

if __name__ == '__main__':
    # scrape()
    for x in generate():
        print(x)
