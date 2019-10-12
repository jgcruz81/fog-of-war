import numpy as num
from numpy import zeros
import random
import math
from operator import attrgetter
import operator
from heapq import heappush, heappop

class Node:
    def __init__(self, x, y, g, h, f, direction):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = f
        self.direction = direction
        return
# initializes the positions of start and end
endrow = random.randint(0,3)
endcolumn = random.randint(0,9)
startrow = random.randint(7,9)
startcolumn = random.randint(0,9)

# we'll start with a small 10 x 10 maze to visualize
gridworld = zeros([10,10])
for x in range(10):
    for y in range(3):
        wall = random.randint(0, 9)
        gridworld[x][wall] = 1
gridworld[endrow][endcolumn] = 3
gridworld[startrow][startcolumn] = 2

print(gridworld)


def begin(gridworld, startx, starty, endx, endy):
    # intialize mental world
    mentalworld = zeros([10, 10])
    mentalworld[startrow][startcolumn] = 2
    mentalworld[endrow][endcolumn] = 3
    # t is for a truth value for while loop
    # x y is for starting positions i j is for end position
    # intial g cost
    g = 0
    # list of minimum f values in open list excluding the popped node
    openMinFCost = []
    openheap = []
    closedlist = []
    moves = [] # list of x,y moves that agents moves
    counter = 0

    openheap.extend(checkneighbors(startx, starty, gridworld, endx, endy, g, "start"))
    updateMentalWorld(openheap, mentalworld, startx, starty)
    h = abs(startx - endx) + abs(starty - endy)
    # closedlist.append(Node(x, y, g, h, g + h, "start"))
    startNode = Node(startrow, startcolumn, 0, h, h + 0, "start")
    endNode = Node(endrow, endcolumn, math.inf, 0, math.inf,"closed")

    while counter < 1:
        computepath(openheap, closedlist, mentalworld,startNode, endNode)

        if len(closedlist) > 0 and closedlist[0].x == endx and closedlist[0].y == endy:
            print("found")
            break
        counter += 1

def computepath(openheap, closedlist, mentalworld, start, end):
    openMinFCost = []
    openheap = sorted(openheap, key=operator.attrgetter('f'))
    while openheap:
        # Looking for min F values then min H values if tied F values (3)
        for it in range(len(openheap)):
            # if there are ties for f cost
            if len(openheap) > 2 and openheap[0].f == openheap[it].f:
                openMinFCost.append(openheap[it])
            else:
                break
        openMinFCostn = sorted(openMinFCost, key=operator.attrgetter('g'))
        openMinFCost = sorted(openMinFCost, key=operator.attrgetter('h'))
        # Pop it from minFcost and pop same node from openheap
        if len(openMinFCost) > 1:
            node = openMinFCost.pop(0)
            for it in range(len(openheap)):
                if node.x == openheap[it].x and node.y == openheap[it].y:
                    openheap.pop(it)
                    break
        else:
            node = openheap.pop(0)
        # Add to closelist (4/11)
        closedlist.insert(0,node)
        if node.x == end.x and node.y == end.y:
            print("found")
            return closedlist
            break
        # Check Neighbors(5/9/10)
        potentialneighbors = checkneighbors(node.x, node.y, mentalworld, end.x, end.y, node.g, node.direction)
        # (12)
        i = 0
        j = 0
        while i < len(potentialneighbors):
            while j < len(openheap):
                if potentialneighbors[i].x == openheap[j].x and potentialneighbors[i].y == openheap[j].y:
                    if potentialneighbors[i].g < openheap[j].g:
                        openheap.pop(j)
                        j -=1
                    else:
                        potentialneighbors.pop(i)
                        i -=1
                        break
                j +=1
            i += 1
        # (13)
        openheap.extend(potentialneighbors)
        openMinFCost.clear()
        openheap = sorted(openheap, key=operator.attrgetter('f'))
        mentalworld[closedlist[0].x][closedlist[0].y] = 1
        print(mentalworld)
        print(closedlist[0].x, closedlist[0].y, closedlist[0].direction)


# function to check neighbors for lowest f value(done)
# if there's a tie then resort to h value (not done)
# if there's a tie then random (not done)
# if all directions are impassable (not done)   perhaps return no value
def checkneighbors(x,y,a,i,j,g, direction):
    neighbors = []
    # check up
    if x != 0 and a[x-1][y] != 1:
        h = abs(x-i-1) + abs(y-j)
        f = g + h + 1
        if direction != "down":
            neighbors.append(Node(x-1,y,g+1,h,f,"up"))
    # check left
    if y != 0 and a[x][y-1] != 1:
        h = abs(x-i) + abs(y-j-1)
        f = g + h + 1
        if direction != "right":
            neighbors.append(Node(x,y-1,g+1,h, f,"left"))
    # check down
    if x != 9 and a[x+1][y] != 1:
        h = abs(x-i+1) + abs(y-j)
        f = g + h + 1
        if direction != "up":
            neighbors.append(Node(x+1,y,g+1,h,f,"down"))
    #check right
    if y != 9 and a[x][y+1] != 1:
        h = abs(x-i) + abs(y-j+1)
        f = g + h + 1
        if direction != "left":
            neighbors.append(Node(x,y+1,g + 1,h,f,"right"))
    c = len(neighbors)
    return neighbors

# this method populates the mental world with 1s
def updateMentalWorld(neighbors, mentalworld, x, y):
    seen = ["up", "down", "left", "right"]
    encompass = []
    for i in range(len(neighbors)):
        encompass.append(neighbors[i].direction)

    new_list = list(set(seen) - set(encompass))
    print(new_list)
    if 'up' in new_list and x != 0:
        mentalworld[x - 1][y] = 1
    if 'left' in new_list and y != 0:
        mentalworld[x][y - 1] = 1
    if 'down' in new_list and x != 9:
        mentalworld[x + 1][y] = 1
    if 'right' in new_list and y != 9:
        mentalworld[x][y + 1] = 1
    print(mentalworld)

begin(gridworld,startrow, startcolumn, endrow, endcolumn)



