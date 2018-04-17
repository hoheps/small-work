import random
answer_list=[]
while len(set(answer_list))!=3:
  answer_list.append(random.randint(1,9)) #generates until at least 3 unique
answer_list = list(set(answer_list)) #makes sure the list only has 3 elements
possible_sets = []
for x in range(1,10):
  for y in range(1,10):
    if y!=x:
      for z in range(1,10):
        if z!=x and z!=y:
          possible_sets.append([x,y,z]) #generates full set with digits 1-9
#gross 
turns = 0
turn_ary = []

def reset():
  global answer_list,turns,possible_sets
  answer_list=[]
  while len(set(answer_list))!=3:
    answer_list.append(random.randint(1,9)) #generates until at least 3 unique
  answer_list = list(set(answer_list)) #makes sure the list only has 3 elements
  possible_sets = []
  for x in range(1,10):
    for y in range(1,10):
      if y!=x:
        for z in range(1,10):
          if z!=x and z!=y:
            possible_sets.append([x,y,z]) #generates full set with digits 1-9
  turns = 0

  
def checker(): #standalone program to run
  while 1:
    guess = raw_input("guess?: ")
    circle = 0
    triangle = 0
    u = 0
    guess_list=[]
    try:
      guess_list=[int(i) for i in guess]
    except ValueError:
      print "NO WEIRD CHARACTERS PLEASE"
      continue
    if len(set(guess_list))!=3:
      print "THREE DIFFERENT NUMBERS PLEASE"
      continue
    if len(guess_list)>3:
      print "FEWER NUMBERS PLEASE"
      continue
    for x in guess_list:
      u+=1
      j=0
      for y in answer_list:
        j+=1
        if x==y and u==j:
          circle+=1
        elif x==y and u!=j:
          triangle+=1
    if circle == 3:
      return "you solved it"
    else:
      print str(circle)+" circles "+str(triangle)+" triangles"

def checker2(guess_list):
  global turns
  circle = 0
  triangle = 0
  u=0
#  guess_list=[int(i) for i in guess]
  turns += 1
  print "turn " + str(turns)
  print "Guess: " + ''.join(map(str,guess_list))
  for x in guess_list:
      u+=1
      j=0
      for y in answer_list:
        j+=1
        if x==y and u==j:
          circle+=1
        elif x==y and u!=j:
          triangle+=1
#  if type(guess_list]) is str: # [2] is guess
#    guess_list] = [int(i) for i in guess_list]]
  if circle == 3: # number of circles
    turn_ary.append(turns)
    reset()
    print "you solved it!"
  else:  
    triangleremover(guess_list, circle+triangle) 
    circleremover(guess_list, circle) 
    checker2(possible_sets[(len(possible_sets)/2)]) #takes middle value
#  logic([circle, triangle, guess_list]) 

def checker3(): #fill in the blanks version! think i should do lambda here
  global turns
  turns += 1 
  print "turn " + str(turns)
  guess = raw_input("guess?: ")
  circle = int(raw_input("# circles?: "))
  triangle = int(raw_input("# triangles?: "))
  guess_list=[int(i) for i in guess]
#  if type(guess_list]) is str: # [2] is guess
#    guess_list] = [int(i) for i in guess_list]]
  if circle == 3: # number of circles
    print "you solved it!"
  else:  
    triangleremover(guess_list, circle+triangle) 
    circleremover(guess_list, circle) 
    print "possible values: "
    print possible_sets
    print "try "+ str(possible_sets[(len(possible_sets)/2)])
    checker3()

def triangleremover(guess, number):
  new_set = []
  global possible_sets
  for example in possible_sets:
#    i = 0
    count = {}
    for x, y in zip(guess,example):
      if x not in count:
        count[x] = 0
      else:
        count[x] += 1
      if y not in count:
        count[x] = 0
      else:
        count[x] += 1
#    for x in guess:
#      for y in example:
#        if x == y:
#          i+=1
    if number == sum(count.values()) :
      new_set.append(example)
  possible_sets = new_set

def circleremover(guess, number):
  new_set = []
  global possible_sets
  for example in possible_sets:
    i = 0
    for j in range(0,3):
      if guess[j] == example[j]:
        i+=1
    if i == number:
      new_set.append(example)
  possible_sets = new_set

for x in range(0,5):
   checker2("123")
print max(turn_ary)
print sum(turn_ary)/float(len(turn_ary))
#count = {}
#for x, y in zip([1,2,3,1],[3,2,1]):
#  if x not in count:
#    count[x] = 0
#  else: count[x]+=1
#  print count
#  print sum(count.values())
