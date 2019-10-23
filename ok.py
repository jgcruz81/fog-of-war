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
class Hnode:
    def __init__(self, x, y, g, h, hnew, f, direction):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.hnew = hnew
        self.f = f
        self.direction = direction
        return
# initializes the positions of start and end


def beginAdaptive(hnewworld,gridworld, startx, starty, endx, endy):
    # intialize mental world
    mentalworld = zeros([5, 5])
    mentalworld[startrow][startcolumn] = 2
    mentalworld[endrow][endcolumn] = 3
    # intial g cost
    g = 0
    # list of minimum f values in open list, used to find min h cost
    openheap = []
    closedlist = []

    openheap.extend(checkneighborsAdaptive(hnewworld,startx, starty, gridworld, endx, endy, g, "start"))
    updateMentalWorld(openheap, mentalworld, startx, starty)
    openheap.clear()

    h = abs(startx - endx) + abs(starty - endy)
    startNode = Node(startrow, startcolumn, 0, h, h + 0, "start")
    openheap.append(startNode)
    endNode = Node(endrow, endcolumn, math.inf, 0, math.inf, "closed")

    while openheap:

        # node = the goal state
        node = computepathAdaptive(hnewworld,openheap, closedlist, mentalworld, endNode)
        becausespagcode = closedlist.copy()
        if len(closedlist) > 0 and (closedlist[0].x != endx or closedlist[0].y != endy):
            print("not found")
            break
        path = followDirections(node)
        path.reverse()
        traveled = []
        hnewworld = zeros([5, 5]) #reset the hworld
        mentalworld[endNode.x][endNode.y] = 0
        counter = len(path) - 1
        update(hnewworld,path[0], becausespagcode, counter)
        hnewworld[path[0].x][path[0].y] = counter
        while path:
            currentblock = path.pop(0)
            if gridworld[currentblock.x][currentblock.y] == 3:
                print("done")
                break

            elif gridworld[currentblock.x][currentblock.y] != 1:
                # update world
                checklist = checkneighborsAdaptive(hnewworld,currentblock.x,currentblock.y, gridworld, endNode.x, endNode.y,0,None)
                updateMentalWorld(checklist, mentalworld, currentblock.x, currentblock.y)
                h = abs(currentblock.x - endx) + abs(currentblock.y - endy)
                startNode = Node(currentblock.x, currentblock.y, 0, counter, h, "start")
                update(hnewworld, currentblock, becausespagcode, counter)
                counter = counter - 1
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

def computepathAdaptive(hnewworld,openheap, closedlist, mentalworld, end):
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
        potentialneighbors = checkneighborsAdaptive(hnewworld,node.x, node.y, mentalworld, end.x, end.y, node.g, node.direction)
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

def checkneighborsAdaptive(hnewworld,x,y,a,i,j,g, direction):
    neighbors = []
    # check up
    if x != 0 and a[x-1][y] != 1:
        if hnewworld[x-1][y] != 0:
            h = hnewworld[x-1][y]
        else:
            h = abs(x-i-1) + abs(y-j)
        f = g + h + 1
        if direction != "down":
            neighbors.append(Node(x-1,y,g+1,h,f,"up"))
    # check left
    if y != 0 and a[x][y-1] != 1:
        if hnewworld[x][y-1] != 0:
            h = hnewworld[x-1][y]
        else:
            h = abs(x-i) + abs(y-j-1)
        f = g + h + 1
        if direction != "right":
            neighbors.append(Node(x,y-1,g+1,h, f,"left"))
    # check down
    if x != 4 and a[x+1][y] != 1:
        if hnewworld[x+1][y] != 0:
            h = hnewworld[x+1][y]
        else:
            h = abs(x-i+1) + abs(y-j)
        f = g + h + 1
        if direction != "up":
            neighbors.append(Node(x+1,y,g+1,h,f,"down"))
    #check right
    if y != 4 and a[x][y+1] != 1:
        if hnewworld[x][y+1] != 0:
            h = hnewworld[x][y+1]
        else:
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
    if 'down' in new_list and x != 4:
        mentalworld[x + 1][y] = 1
    if 'right' in new_list and y != 4:
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
#updates the h value for cells that are in the closedlist and traversed
def update(hnewworld,node, list,h):
    currentnode = node
    # update up
    # if not on boundary
    if currentnode.direction != "down":
        if currentnode.x != 0 and gridworld[currentnode.x - 1][currentnode.y] != 1:
            # traverse the closedlist to see if it matches that spot in the gridworld
            for x in range(len(list)):
                if list[x].x == currentnode.x - 1 and list[x].y == currentnode.y:
                    list.pop(x)
                    if hnewworld[currentnode.x - 1][currentnode.y] == 0:
                        hnewworld[currentnode.x - 1][currentnode.y] = h - 1
                    break
    # update left
    if currentnode.direction != "right":
        if currentnode.y != 0 and gridworld[currentnode.x][currentnode.y - 1] != 1:
            for x in range(len(list)):
                if list[x].x == currentnode.x and list[x].y == currentnode.y - 1:
                    list.pop(x)
                    if hnewworld[currentnode.x][currentnode.y - 1] == 0:
                        hnewworld[currentnode.x][currentnode.y - 1] = h - 1
                    break
    # update down
    if currentnode.direction != "down":
        if currentnode.x != 4 and gridworld[currentnode.x + 1][currentnode.y] != 1:
            for x in range(len(list)):
                if list[x].x == currentnode.x + 1 and list[x].y == currentnode.y:
                    list.pop(x)
                    if hnewworld[currentnode.x + 1][currentnode.y] == 0:
                        hnewworld[currentnode.x + 1][currentnode.y] = h - 1
                    break
    # update right
    if currentnode.direction != "left":
        if currentnode.y != 4 and gridworld[currentnode.x][currentnode.y + 1] != 1:
            for x in range(len(list)):
                if list[x].x == currentnode.x and list[x].y == currentnode.y + 1:
                    list.pop(x)
                    if hnewworld[currentnode.x][currentnode.y + 1] == 0:
                        hnewworld[currentnode.x][currentnode.y + 1] = h - 1
                    break



x = 10
intMatrix = zeros([x, x])
gridworld = [[0,0,0,0,0],[0,0,1,0,0],[0,0,1,1,0],[0,0,1,1,0],[0,0,0,1,0]]
gridworld[4][4] = 3
gridworld[4][2] = 2
startrow = 4
startcolumn = 2
endcolumn = 4
endrow = 4

hnewworld = zeros([5, 5])
beginAdaptive(hnewworld,gridworld,startrow, startcolumn, endrow, endcolumn)