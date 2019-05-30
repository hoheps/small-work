from bs4 import BeautifulSoup
import re
import collections

with open('steam.txt', 'r') as f:
    data = f.read()

soup = BeautifulSoup(data,"lxml")

owner_username = soup.find_all('a',limit=2)[-1].text

matches = soup.tr.find_next_siblings()
winlose = {"W":[],"L":[],"T":[]}
for match in matches:
    userinfo = match.td.find_next_sibling().find_all("td")
    #not the prettiest
    team1 = [re.sub("\n", "", userinfo[playerseed].text)[1:] for playerseed in range(0,40,8)]
    team1score,_,team2score = userinfo[40].text.split()
    team1score = int(team1score)
    team2score = int(team2score)
    team2 = [re.sub("\n", "", userinfo[playerseed].text)[1:] for playerseed in range(41,80,8)]
    #basically takes the name from userinfo[0] and removes the newlines, and the first space. quick and dirty
    if team1score == team2score:
        print("tie")
        if owner_username in team1:
            winlose["L"].append(team1)
        if owner_username in team2:
            winlose["L"].append(team2)
    #ties are basically losses... right
    elif (owner_username in team1 and team1score > team2score) or (owner_username in team2 and team2score > team1score):
        print("win")
        if owner_username in team1:
            winlose["W"].append(team1)
        if owner_username in team2:
            winlose["W"].append(team2)
    else:
        print("lose")
        if owner_username in team1:
            winlose["L"].append(team1)
        if owner_username in team2:
            winlose["L"].append(team2)
lose = collections.Counter([item for list in winlose["L"] for item in list])
win = collections.Counter([item for list in winlose["W"] for item in list])
for x in set(win).intersection(lose):
    print(x, win[x]/(win[x]+lose[x]), win[x]+lose[x])
#tie = collections.Counter([item for list in winlose["T"] for item in list])

#future data processing

"""maptitle = soup.tr.find_next_siblings()[0].td.find_all()[4]
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
score = userinfo[7].text"""
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
        self.matchid = matchid
    def __str__(self):
        pass#return matchtime
    def add_player(self, Player, team):
        pass
    def mapname(self):
        pass#return mapname
    def teammates(self):
        pass
    def players(self):
        pass#return players

class Player:
    def __init__(self, name, id):
        self.name
        self.id
    def __str__(self):
        return self.name
    def __repr__(self):
        return "player({})".format(self.name)
