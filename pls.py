import turtle
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("AI")
wn.setup(1300,1200)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.shapesize(.25)
levels = [""]
level_1 = []
#Assembles Maze
#First Row
string = "X"
for y in range(100):
    string = string + "X"
level_1.append(string)
#Middle Rows
endrow = random.randint(0,30)
endcolumn = random.randint(1,101)
startrow = random.randint(70,100)
startcolumn = random.randint(1,101)
for y in range(100):
    string = "X"
    for x in range(99):
        number = random.randint(0,10) # determines if block is path or not
        if x == endrow and y == endcolumn:
            string = string + "E"
        elif x == startrow and y == startcolumn:
            string = string + "S"
        elif number < 9:
            string = string + " "
        else:
            string = string + "X"
    string = string + "X"
    level_1.append(string)
# Last Row
string = "X"
for y in range(100):
    string = string + "X"
level_1.append(string)

# Create the list
levels.append(level_1)
print("end: " + str(endcolumn) + " " + str(endrow))
print("start: " + str(startcolumn) + " " + str(startrow))

def setupmaze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -500 + (x * 6)
            screen_y = 350 - (y * 6)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
            elif character == 'E':
                pen.color("red")
                pen.goto(screen_x, screen_y)
                pen.stamp()
                pen.color("blue")
            elif character == 'S':
                pen.color("yellow")
                pen.goto(screen_x, screen_y)
                pen.stamp()
                pen.color("blue")
def setuphpath(levels, s0, s1, e0, e1):
    x = startrow-endrow
    #for x1 in range(x):



pen = Pen()
print(levels[1][endcolumn+1])

setupmaze(levels[1])


setuphpath(levels[1], startrow, startcolumn, endrow, endcolumn)
while True:
    pass

