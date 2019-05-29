from bs4 import BeautifulSoup
import re

with open('steam.html', 'r') as f:
    data = f.read()

soup = BeautifulSoup(data,"lxml")
matches = soup.tr.find_next_siblings()

maptitle = soup.tr.find_next_siblings()[0].td.find_all()[4]
date = soup.tr.find_next_siblings()[0].td.find_all()[6]
waittime = soup.tr.find_next_siblings()[0].td.find_all()[8]
matchlength = soup.tr.find_next_siblings()[0].td.find_all()[10]

userinfo = soup.tr.find_next_siblings()[0].td.find_next_sibling().find_all("td")

username = userinfo[0].text
steamid3 = userinfo[0].img['data-miniprofile']
#to differentiate between different users
ping = userinfo[1].text
k = userinfo[2].text
a = userinfo[3].text
d = userinfo[4].text
#keep in mind the next 2 can be blank
mvp = userinfo[5].text
hsp = userinfo[6].text
score = userinfo[7].text
for playerseed in range(0,40,8):
    pass
score = userinfo[40].text

for playerseed in range(41,80,8):
    pass

#convert into csv?
#identify player by name on the top
#initially i wanted to do player in all games... but what if player only plays with a friend


#this feels like a databases problem
#maybe I should make sql for this lmao
class Match:
    def __init__(self, matchid):
        self.matchid = 
    def __str__(self):
        return matchtime
    def add_player(self, Player, team):

    def mapname(self):
        return mapname
    def teammates(self):

    def players(self):
        return players

class Player:
    def __init__(self, name, id):
        self.name
        self.id = 

    def __str__(self):
        return self.name

    def __repr__(self):
        return "player({})".format(self.name)