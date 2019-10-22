import pygame
import math
from numpy import zeros
import random
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



# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (168, 233, 240)
PURPLE = (102, 0, 102)
ORANGE = (252, 192, 27)

# Pygame visuals
size = (808, 808)
sq_size = 8
screen = pygame.display.set_mode(size)
pygame.display.set_caption("A*")


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

    # update the first view of the world
    openheap.extend(checkneighbors(startx, starty, gridworld, endx, endy, g, "start"))
    updateMentalWorld(openheap, mentalworld, startx, starty)
    openheap.clear()

    # create the first nodes and add start to heap
    h = abs(startx - endx) + abs(starty - endy)
    startNode = Node(startrow, startcolumn, 0, h, h + 0, "start")
    openheap.append(startNode)
    endNode = Node(endrow, endcolumn, math.inf, 0, math.inf,"closed")

    # INTIALIZE WORLD
    pygame.init()
    printpath(closedlist, openheap, "WHITE")
    # Prints Start
    printpath(closedlist, openheap, "START")
    # Bryan's code here...
    while openheap:

        # node = the goal state
        node = computepath(openheap, closedlist, mentalworld, endNode)
        if len(closedlist) > 0 and closedlist[0].x != endx and closedlist[0].y != endy:
            print("not found")
            break
        path = followDirections(node)
        path.reverse()
        traveled = []
        mentalworld[startNode.x][startNode.y] = 0
        printpath(closedlist, openheap, "WHITE")
        printpath(closedlist, openheap, "START")
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


            else:
                currentblock = traveled[-1]
                break
                print("stop")
        startposition = []
        startposition.append(currentblock)
        printpath(None, traveled, "ORANGE")
        printpath(closedlist, openheap, "WHITE")
        printpath(None,startposition, "START")

        if gridworld[currentblock.x][currentblock.y] == 3:
            print("target reached goal")
            break

        mentalworld[startrow][startcolumn] = 0
        mentalworld[currentblock.x][currentblock.y] = 2
        path.clear()
        openheap.clear()
        openheap.append(startNode)
        closedlist.clear()

    printpath(closedlist, openheap, "WHITE")
    printpath(closedlist, startposition, "START")
    exit()


def computepath(openheap, closedlist, mentalworld, end):
    #Used for tied F values
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
        # Have to look through openMinFCost to find lowest h cost for optimization
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
            print("found a path")
            #printpath(closedlist, openheap, "OPEN")
            printpath(closedlist, openheap, "BLUE")
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

# Colors in the path
def printpath(closedlist, openheap, color):
    done = False
    """""
    if color == "OPEN":
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for i in range(len(openheap)):
                            pygame.draw.rect(screen, LIGHTBLUE,
                                             [openheap[i].x * sq_size + 2, openheap[i].y * sq_size + 2, sq_size - 2,
                                              sq_size - 2])
                            done = True
    """""
    if color == "BLUE":
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(openheap)):
                        pygame.draw.rect(screen, LIGHTBLUE,
                                         [openheap[i].x * sq_size + 2, openheap[i].y * sq_size + 2, sq_size - 2,
                                          sq_size - 2])
                    for i in range(len(closedlist)):
                        pygame.draw.rect(screen, BLUE,
                                         [closedlist[i].x * sq_size + 2, closedlist[i].y * sq_size + 2, sq_size - 2,
                                          sq_size - 2])
                        done = True
    if color == "ORANGE":
        for i in range(len(openheap)):
            pygame.draw.rect(screen, ORANGE,
                             [openheap[i].x * sq_size + 2, openheap[i].y * sq_size + 2, sq_size - 2,
                              sq_size - 2])


    if color == "BLACK":
        for x0, x1 in enumerate(gridworld):
            for y0, y1 in enumerate(x1):
                if y1 == 1:
                    pygame.draw.rect(screen, BLACK,
                                     [x0 * sq_size + 2, y0 * sq_size + 2, sq_size - 2, sq_size - 2])
    if color == "WHITE":
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(WHITE)

                    # Prints Grid
                    for x in range(0, 101):
                        pygame.draw.line(screen, BLACK, [0, x * sq_size], [808, x * sq_size], 2)
                        pygame.draw.line(screen, BLACK, [x * sq_size, 0], [x * sq_size, 808], 2)
                    # Prints blocked squares
                    printpath(closedlist, openheap, "BLACK")
                    pygame.draw.rect(screen, RED,
                                     [endrow * sq_size + 2, endcolumn * sq_size + 2, sq_size - 2, sq_size - 2])
                    done = True
    if color == "START":
        pygame.draw.rect(screen, GREEN, [openheap[0].x * sq_size + 2, openheap[0].y * sq_size + 2, sq_size - 2, sq_size - 2])

    pygame.display.flip()
#Last button to exit
def exit():
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    done = True
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


#------------------------------------------------
#now contains 'intMatrix' to be modified, and size of world: 'x'
def dfs(nodeMatrix, intMatrix, xcoord, ycoord,x):
    nodeMatrix[xcoord][ycoord].visited = True
    direction = random.randint(1, 4)
    counter = 0
    while counter < 4:
        if direction % 4 == 0:  # go up
            if ycoord - 2 >= 0:  # check if in bounds
                if (not nodeMatrix[xcoord][ycoord - 2].visited):  # check if visited
                    intMatrix[xcoord][ycoord - 1] = 0  # breaks the wall
                    dfs(nodeMatrix, intMatrix,xcoord, ycoord - 2,x)
        elif direction % 4 == 1:  # go right
            if xcoord + 2 <= x:  # check if in bounds
                if (not nodeMatrix[xcoord + 2][ycoord].visited):  # check if visited
                    intMatrix[xcoord + 1][ycoord] = 0  # breaks the wall
                    dfs(nodeMatrix, intMatrix, xcoord + 2, ycoord,x)
        elif direction % 4 == 2:  # go down
            if ycoord + 2 <= x:  # check if in bounds
                if (not nodeMatrix[xcoord][ycoord + 2].visited):  # check if visited
                    intMatrix[xcoord][ycoord + 1] = 0  # breaks the wall
                    dfs(nodeMatrix, intMatrix, xcoord, ycoord + 2,x)
        elif direction % 4 == 3:  # go right
            if xcoord - 2 >= 0:  # check if in bounds
                if (not nodeMatrix[xcoord - 2][ycoord].visited):  # check if visited
                    intMatrix[xcoord - 1][ycoord] = 0  # breaks the wall
                    dfs(nodeMatrix, intMatrix, xcoord - 2, ycoord,x)
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
        
def main():
 x = 101
 mazeList = []
    nodeMatrix = [[Node(0, False) for i in range(x)] for j in range(x)]
    y = 0
    # run 50 times to store 50 diff matrices
    while y < 50:

        intMatrix = zeros([x, x])
        # modifies nodeMatrix
        for r in range(x):
            for c in range(x):
                nodeMatrix[r][c] = Node(0, False)
        # creates tic-tac-toe pattern of walls, to be broken down
        for row in range(1, x, 2):
            for col in range(x):
                intMatrix[row][col] = 1
                nodeMatrix[row][col] = Node(1, True)
        for col in range(1, x, 2):
            for row in range(x):
                intMatrix[row][col] = 1
                nodeMatrix[row][col] = Node(1, True)
        
        # makes 'xcoord' and 'ycoord' a random positive int between 0 and 'x', inclusive, unless 'x' is negative
        xcoord = random.randrange(0,x,2)
        ycoord = random.randrange(0,x,2)
        dfs(nodeMatrix,intMatrix,xcoord,ycoord,x)
        mazeList.append(intMatrix)
        y+=1

    #prints the maze, but currently commented out
    counter = 0
    while counter<50:
        #print(mazeList[counter])
        counter+=1
# GridWorld Matrix
main() # stores the 50 matrices in 'mazeList'
#----------------------------------------------




endrow = random.randint(70,99)
endcolumn = random.randint(70,99)
startrow = random.randint(0,30)
startcolumn = random.randint(0,30)
gridworld = zeros([101,101])
for x in range(101):
    for y in range(30):
        wall = random.randint(0, 100)
        gridworld[x][wall] = 1
gridworld[endrow][endcolumn] = 3
gridworld[startrow][startcolumn] = 2
"""
dfs(nodeMatrix, intMatrix, random.randrange(0,x,2), random.randrange(0,x,2),x)
endrow = random.randint(70,99)
endcolumn = random.randint(70,99)
startrow = random.randint(0,30)
startcolumn = random.randint(0,30)
gridworld = intMatrix
gridworld[endrow][endcolumn] = 3
gridworld[startrow][startcolumn] = 2
"""
begin(gridworld,startrow, startcolumn, endrow, endcolumn)
