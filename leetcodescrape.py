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
    cur.execute("CREATE TABLE question_list (id KEY, title TEXT, problem TEXT, content TEXT, link TEXT);")
    question_id = 0
    for txt in soup.select("body p a"):
        if not re.search(r'(?<=\").*/(?=\")', str(txt)):
            continue
        link = re.search(r'(?<=href=\").*/(?=\")', str(txt)).group()
        req = requests.get(link, headers=headers)
        insoup = BeautifulSoup(req.content, 'lxml')
        title = insoup.select("h1 a")[0].get_text()
        questionline = 0
        for i,line in enumerate(insoup.select("div.entrybody p")):
            while line.span: #finds the span tags, which contains ads
                line.span.decompose() #removes them
            if line.strong and not questionline: #gets the first strong tag, which usually means it's the answer/analysis
                questionline = i
        problem = "\n".join((x.get_text() for x in insoup.select("div.entrybody p")[:questionline]))
        content = "\n".join((x.get_text() for x in insoup.select("div.entrybody p")[questionline:]))
        #content = re.search(r'[\s\S]*(?=Related posts)', content).group() #removes relatedposts content, but related posts aren't in the p tag so commented out
        cur.execute("INSERT INTO question_list VALUES (?,?,?,?,?);", (question_id, title, problem, content, link))
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
    scrape()
    #for x in generate():
    #    print(x)

# commands for export
# sqlite> .mode list
# sqlite> .separator $
# sqlite> .output test_file_2.txt
# sqlite> SELECT title,problem, content  FROM question_list;
# sqlite> .exit
# perl -pe 's/\n/<br>/g' -i test_file_2.txt
# perl -pe 's/LeetCode – /\n/g' -i test_file_2.txt  
#perl commands make it easier to import to some programs