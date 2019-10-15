import numpy as num
from numpy import zeros
import random
import math
from operator import attrgetter
import operator
import sys
sys.setrecursionlimit(10000)

class Nod:
    def __init__(self, data, visited):
        self.data = data
        self.visited = visited

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
endrow = random.randint(70,99)
endcolumn = random.randint(70,99)
startrow = random.randint(0,30)
startcolumn = random.randint(0,30)


def begin(gridworld, startx, starty, endx, endy):
    # intialize mental world
    mentalworld = zeros([101, 101])
    mentalworld[startrow][startcolumn] = 2
    mentalworld[endrow][endcolumn] = 3
    # intial g cost
    g = 0
    # list of minimum f values in open list, used to find min h cost
    openheap = []
    closedlist = []

    openheap.extend(checkneighbors(startx, starty, gridworld, endx, endy, g, "start"))
    updateMentalWorld(openheap, mentalworld, startx, starty)
    openheap.clear()

    h = abs(startx - endx) + abs(starty - endy)
    startNode = Node(startrow, startcolumn, 0, h, h + 0, "start")
    openheap.append(startNode)
    endNode = Node(endrow, endcolumn, math.inf, 0, math.inf, "closed")

    openheap.append(startNode)

    while openheap:

        # node = the goal state
        node = computepath(openheap, closedlist, mentalworld, endNode)
        if len(closedlist) > 0 and closedlist[0].x != endx and closedlist[0].y != endy:
            print("not found")
            break
        path = followDirections(node)
        path.reverse()
        traveled = []
        mentalworld[endNode.x][endNode.y] = 0
        while path:
            currentblock = path.pop(0)
            if gridworld[currentblock.x][currentblock.y] == 3:
                print("done")
                break

            elif gridworld[currentblock.x][currentblock.y] != 1:
                # update world
                checklist = checkneighbors(currentblock.x,currentblock.y, gridworld, endNode.x, endNode.y,0,None)
                updateMentalWorld(checklist, mentalworld, currentblock.x, currentblock.y)
                h = abs(currentblock.x - endx) + abs(currentblock.y - endy)
                startNode = Node(currentblock.x, currentblock.y, 0, h, h + 0, "start")
                traveled.append(startNode)


                mentalworld[currentblock.x][currentblock.y] = 2
                mentalworld[currentblock.x][currentblock.y] = 0

            else:
                currentblock = traveled[-1]
                break
                print("stop")
        if gridworld[currentblock.x][currentblock.y] == 3:
            print("target reached goal")
            break

        mentalworld[startrow][startcolumn] = 0
        mentalworld[currentblock.x][currentblock.y] = 2
        path.clear()
        openheap.clear()
        openheap.append(startNode)
        closedlist.clear()

def computepath(openheap, closedlist, mentalworld, end):
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
        openMinFCost = sorted(openMinFCost, key=operator.attrgetter('h'))
        # Have to look through openMinFCostn to find lowest h cost for optimization
        if len(openMinFCost) > 1:
            node = openMinFCost.pop(0)
            for it in range(len(openheap)):
                if node.x == openheap[it].x and node.y == openheap[it].y:
                    # Pop it from minFcost and pop same node from openheap
                    openheap.pop(it)
                    break
        else:
            node = openheap.pop(0)
        # Add  node to closelist (4/11)
        closedlist.insert(0,node)
        if node.x == end.x and node.y == end.y:
            print("found")
            return closedlist
            break
        # Check Neighbors(5/9/10)
        # not all nodes in potentialneighbors will make it to openlist
        potentialneighbors = checkneighbors(node.x, node.y, mentalworld, end.x, end.y, node.g, node.direction)
        i = 0
        j = 0
        # Used to remove duplicate nodes from checkneighbors (12)
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
            j = 0
            i += 1
        i = 0
        j = 0
        while i < len(potentialneighbors):
            while j < len(closedlist):
                if potentialneighbors[i].x == closedlist[j].x and potentialneighbors[i].y == closedlist[j].y:
                    potentialneighbors.pop(i)
                    i -= 1
                    break
                j += 1
            j = 0
            i += 1
        # (13)
        openheap.extend(potentialneighbors)
        openMinFCost.clear()
        openheap = sorted(openheap, key=operator.attrgetter('f'))


    #If no path was found
    if closedlist[0] != end:
        print("no path found")
        return closedlist
    return closedlist


# Checking node's neighbors
# node.x = x    node.y = y
# a is world that you are using
# end.i = i     end.y = y
# g is node.g and direction is used to not append the direction you came from

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
    if x != 100 and a[x+1][y] != 1:
        h = abs(x-i+1) + abs(y-j)
        f = g + h + 1
        if direction != "up":
            neighbors.append(Node(x+1,y,g+1,h,f,"down"))
    #check right
    if y != 100 and a[x][y+1] != 1:
        h = abs(x-i) + abs(y-j+1)
        f = g + h + 1
        if direction != "left":
            neighbors.append(Node(x,y+1,g + 1,h,f,"right"))
    c = len(neighbors)
    return neighbors

# this method populates the mental world with 1s
#
def updateMentalWorld(neighbors, mentalworld, x, y):
    seen = ["up", "down", "left", "right"]
    encompass = []
    for i in range(len(neighbors)):
        encompass.append(neighbors[i].direction)

    new_list = list(set(seen) - set(encompass))
    if 'up' in new_list and x != 0:
        mentalworld[x - 1][y] = 1
    if 'left' in new_list and y != 0:
        mentalworld[x][y - 1] = 1
    if 'down' in new_list and x != 100:
        mentalworld[x + 1][y] = 1
    if 'right' in new_list and y != 100:
        mentalworld[x][y + 1] = 1

def followDirections(closedlist):
    #closedlist.reverse()
    currentnode = closedlist.pop(0)
    list = []
    list.append(currentnode)
    for x in range(len(closedlist)):
        if currentnode.direction == "start":
            return list
        else:
            for y in range(len(closedlist)):
                #if closedlist[y].
                if currentnode.direction == "up" and closedlist[y].x == currentnode.x + 1 and closedlist[y].y == currentnode.y:
                    currentnode = closedlist[y]
                    list.append(closedlist.pop(y))
                    break
                if currentnode.direction == "left" and closedlist[y].x == currentnode.x and closedlist[y].y == currentnode.y + 1:
                    currentnode = closedlist[y]
                    list.append(closedlist.pop(y))
                    break
                if currentnode.direction == "down" and closedlist[y].x == currentnode.x - 1 and closedlist[y].y == currentnode.y:
                    currentnode = closedlist[y]
                    list.append(closedlist.pop(y))
                    break
                if currentnode.direction == "right" and closedlist[y].x == currentnode.x and closedlist[y].y == currentnode.y - 1:
                    currentnode = closedlist[y]
                    list.append(closedlist.pop(y))
                    break


    return list

def dfs(nodeMatrix, xcoord, ycoord):
    nodeMatrix[xcoord][ycoord].visited = True
    direction = random.randint(1, 4)
    counter = 0
    while counter < 4:
        if direction % 4 == 0:  # go up
            if ycoord - 2 >= 0:  # check if in bounds
                if (not nodeMatrix[xcoord][ycoord - 2].visited):  # check if visited
                    intMatrix[xcoord][ycoord - 1] = 0  # breaks the wall
                    dfs(nodeMatrix, xcoord, ycoord - 2)
        elif direction % 4 == 1:  # go right
            if xcoord + 2 <= x:  # check if in bounds
                if (not nodeMatrix[xcoord + 2][ycoord].visited):  # check if visited
                    intMatrix[xcoord + 1][ycoord] = 0  # breaks the wall
                    dfs(nodeMatrix, xcoord + 2, ycoord)
        elif direction % 4 == 2:  # go down
            if ycoord + 2 <= x:  # check if in bounds
                if (not nodeMatrix[xcoord][ycoord + 2].visited):  # check if visited
                    intMatrix[xcoord][ycoord + 1] = 0  # breaks the wall
                    dfs(nodeMatrix, xcoord, ycoord + 2)
        elif direction % 4 == 3:  # go right
            if xcoord - 2 >= 0:  # check if in bounds
                if (not nodeMatrix[xcoord - 2][ycoord].visited):  # check if visited
                    intMatrix[xcoord - 1][ycoord] = 0  # breaks the wall
                    dfs(nodeMatrix, xcoord - 2, ycoord)
        direction = direction + 1
        counter = counter + 1

x= 101
intMatrix = zeros([x, x])
nodeMatrix = [[Nod(0, False) for i in range(x)] for j in range(x)]
for r in range(x):
    for c in range(x):
        nodeMatrix[r][c] = Nod(0, False)
# creates tic-tac-toe pattern of walls, to be broken down
for row in range(1, x, 2):
    for col in range(x):
        intMatrix[row][col] = 1
        nodeMatrix[row][col] = Nod(1, True)
for col in range(1, x, 2):
    for row in range(x):
        intMatrix[row][col] = 1
        nodeMatrix[row][col] = Nod(1, True)

dfs(nodeMatrix, 0, 0)
endrow = random.randint(70,99)
endcolumn = random.randint(70,99)
startrow = random.randint(0,30)
startcolumn = random.randint(0,30)
gridworld = intMatrix
gridworld[endrow][endcolumn] = 3
gridworld[startrow][startcolumn] = 2

begin(gridworld,startrow, startcolumn, endrow, endcolumn)



