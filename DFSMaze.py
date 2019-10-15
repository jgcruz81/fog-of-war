import random
import numpy as num
from numpy import zeros
import sys
sys.setrecursionlimit(10000)



class Nod:
    def __init__(self, data, visited):
        self.data = data
        self.visited = visited


# x = size of gridworld
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




# for marking as visited


# xcoord and ycoord restricted to even numbers
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


dfs(nodeMatrix, 0, 0)
print(intMatrix)