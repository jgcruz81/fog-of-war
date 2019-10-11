import numpy as num
from numpy import zeros
import random
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
    t = 1
    x = startx
    y = starty
    i = endx
    j = endy
    # intial g cost
    g = 0
    # list of minimum f values in open list excluding the popped node
    openMinFCost = []
    openheap = []
    closedlist = []
    moves = [] # list of x,y moves that agents moves
    counter = 0

    openheap.extend(checkneighbors(x, y, gridworld, i, j, g))
    updateMentalWorld(openheap, mentalworld, x, y)
    h = abs(x - 1) + abs(y - j)
    closedlist.append(Node(x, y, g, h, g + h, "start"))

    while counter < 15:
        openheap = sorted(openheap, key = operator.attrgetter('f'))
        if len(openheap) > 1:
            nodePopped = openheap.pop(0)
            minf = nodePopped.f
            # find min f cost nodes
            for x in range(len(openheap)):
                #if there are ties for f cost
                if openheap[x].f == minf:
                    openMinFCost.append(openheap[x])
                else:
                    break
            # Looking for tied F values and min H values
            possibleHList = sorted(openMinFCost, key=operator.attrgetter('h'))
            if possibleHList:
                possibleNode = possibleHList.pop(0)
                if possibleNode.h < nodePopped.h:
                    nodePopped = possibleNode
            # print("NodePopped: ", nodePopped.x,nodePopped.y, nodePopped.direction)

            closedlist.append((x,y))
            x = nodePopped.x
            y = nodePopped.y
            g = nodePopped.g
            moves.append((x, y))
            # possibly reverse x and y
            print(moves[counter])
        if x == endx and y == endy:
            print("found")
            t = 0
            break
        openMinFCost.clear()
        openheap.extend(checkneighbors(x, y, mentalworld, i, j, g))
        counter += 1

def computepath(openheap, closedlist, mentalworld, start, end):
    openMinFCost = []
    counter = 0
    while openheap:
        # Looking for min F values then min H values if tied F values (3)
        for it in range(len(openheap)):
            # if there are ties for f cost
            if len(openheap) > 1 and openheap[0].f == openheap[it].f:
                openMinFCost.append(openheap[it])
            else:
                break
        openMinFCostn = sorted(openMinFCost, key=operator.attrgetter('h'))
        if len(openMinFCost) > 1:
            node = openMinFCost.pop(0)
            for it in range(len(openheap)):
                if node == openheap[it]:
                    openheap.pop(it)
                    break
        else:
            node = openheap.pop(0)
        # Add to closelist (4)
        closedlist.insert(0,node)
        if node.x == end.x and node.y == end.y:
            print("found")
            return closedlist
            break
        # Check Neighbors(5)
        potentialneighbors = checkneighbors(node.x, node.y, mentalworld, end.x, end.y, node.g)
        # (12)
        for i in len(potentialneighbors):
            for j in len(openheap):
                if potentialneighbors[i].x == openheap[j].x and potentialneighbors[i].y == openheap[j].y:
                    if potentialneighbors[i].g < openheap[j]:
                        openheap.pop(j)
                    else:
                        potentialneighbors.pop()






# function to check neighbors for lowest f value(done)
# if there's a tie then resort to h value (not done)
# if there's a tie then random (not done)
# if all directions are impassable (not done)   perhaps return no value
def checkneighbors(x,y,a,i,j,g):
    neighbors = []
    # check up
    if x != 0 and a[x-1][y] != 1:
        h = abs(x-i-1) + abs(y-j)
        f = g + h + 1
        neighbors.append(Node(x-1,y,g+1,h,f,"up"))
    # check left
    if y != 0 and a[x][y-1] != 1:
        h = abs(x-i) + abs(y-j-1)
        f = g + h + 1
        neighbors.append(Node(x,y-1,g+1,h, f,"left"))
    # check down
    if x != 9 and a[x+1][y] != 1:
        h = abs(x-i+1) + abs(y-j)
        f = g + h + 1
        neighbors.append(Node(x+1,y,g+1,h,f,"down"))
    #check right
    if y != 9 and a[x][y+1] != 1:
        h = abs(x-i) + abs(y-j+1)
        f = g + h + 1
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



