


# Add code to modify contents of geo.
# Use drop down menu to select examples.
from math import radians , sin  , cos , sqrt
import threading
import random
def pop():
  global table , row , col
  rad = 0.3
  offsetX = 0.0 ; offsetY = 0.0
  threading.Timer(5.0, pop).start()
  r = random.randint(0,row-1)
  c = random.randint(0,len(table[r])-1)
  table[r].pop(c)
  for i in range(row):
    
    for j in range(len(table[i])):
       
    
        
        x=offsetX + rad * j
        y=offsetY + rad * j
        z = 0
        
        pos = (x,y,z)
        #point = geo.createPoint()
        #point.setPosition(pos)
  #print(table)

num = 100
angle = 137.508
cval = 0.2
row = 10
col = 5
table = [[1 for _ in range(col)] for _ in range(row)]
rad = 0.3
print(table)
'''
->   1 1 ... 1 1
     1 1 ... 1
     1 1 . . 1 1


'''
#from down to up




pop()  
   
    
  