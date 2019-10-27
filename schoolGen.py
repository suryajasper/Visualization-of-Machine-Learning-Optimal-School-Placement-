from graphics import *
import random
import math
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

################Globals#####################
maxX = 750
maxY = 750
win = GraphWin("SchoolGenerator", maxX,maxY, autoflush = False)
houses = []
#schoolColors = []
schools = []
global lines
lines = []
global texts
texts = []
global scaleFactor
scaleFactor = 20
colors = ["red", "blue", "green", "yellow", "black", "purple", "pink", "brown"]
colorInd = 0
random.shuffle(colors)
################Globals#####################

################Classes###################
class School:
    def __init__(self, cost, graphic, color):
        self.cost = cost
        self.graphic = graphic
        self.color = color
        self.students = 0
class House:
    def __init__(self, income, graphic):
        self.income = income
        self.graphic = graphic
        self.school = None
################Classes###################

################Functions###################
def button(x,y, text, color):
    b = Rectangle(Point(x, y), Point(x+len(text)*10, y+30))
    b.setFill(color)
    text = Text(Point(x+(len(text)*5), y+15), text)
    text.setTextColor("white")
    text.setSize(13)
    b.draw(win)
    text.draw(win)
    return b
def inside(point, rectangle):
    ll = rectangle.getP1() 
    ur = rectangle.getP2()  
    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

def drawCircle(point, color, size):
    r = Circle(point, size)
    r.setFill(color)
    r.setWidth(0)
    r.draw(win)
    return r
def makeHouse(point, color):
    houses.append(House(random.randint(20000, 250000), drawCircle(point, color, 5)))
def makeSchool(point):
    color = color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    schools.append(School(0, drawCircle(point, color, 10), color))
def distance(p1, p2):
    dis = math.sqrt( abs( p1.getX()-p2.getX() )**2 + abs( p1.getY()-p2.getY() )**2 )
    return dis
def selectHouse(point):
    for house in houses:
        if distance(house.graphic.getCenter(), point) < 5:
            houseModel = GraphWin("House Model", 200, 200, autoflush = False)
            houseIncomeText = Text(Point(100,50), ("Annual Income: $" + locale.format_string("%d", house.income, grouping=True)))
            houseIncomeText.setSize(15)
            houseIncomeText.draw(houseModel)
            return
    for school in schools:
        if distance(school.graphic.getCenter(), point) < 5:
            schoolModel = GraphWin("School Model", 200, 200, autoflush = False)
            schoolModel.setBackground(school.color)
            schoolIncomeText = Text(Point(100,50), ("Annual Tuition: $" + locale.format_string("%d", school.cost, grouping=True)))
            schoolIncomeText.setSize(15)
            schoolIncomeText.draw(schoolModel)
            schoolStudentsText = Text(Point(100,100), ("Number of students: " + str(school.students)))
            schoolStudentsText.setSize(15)
            schoolStudentsText.draw(schoolModel)
            return
def modifyHouses():
    global lines, scaleFactor, texts
    if len(schools) > 0:
        for line in lines:
            line.undraw()
        for text in texts:
            text.undraw()
        lines = []
        texts = []
        for school in schools:
            school.students = 0
        for house in houses:
            distances = []
            minInd = 0
            for i in range(len(schools)):
                distance = math.sqrt((abs(schools[i].graphic.getCenter().getX()/scaleFactor-house.graphic.getCenter().getX()/scaleFactor)**2 + abs(schools[i].graphic.getCenter().getY()/scaleFactor-house.graphic.getCenter().getY()/scaleFactor)**2))
                distances.append(distance)
                if distance < distances[minInd]:
                    minInd = i
            house.graphic.setFill(schools[minInd].color)
            schools[minInd].students += 1
            line = Line(house.graphic.getCenter(), schools[minInd].graphic.getCenter())
            line.setFill(schools[minInd].color)
            line.draw(win)
            lines.append(line)
            if len(houses) < 200:
                t = Text(line.getCenter(), str(int(distances[minInd])))
                t.setSize(10)
                t.draw(win)
                texts.append(t)
################Functions###################
modeText = Text(Point(maxX/2, maxY/20), "Placing: House")
mode = 0 #house = 0, school = 1, select = 2
makeModeSchool = button(maxX/2-100, maxY/15, "School", "red")
makeModeHouse = button(maxX/2, maxY/15, "House", "blue")
makeModeSelect = button(maxX/2-200, maxY/15, "Select", "black")
randomizeHouses = button(maxX/2+50, maxY/15, "randomize", "green")
randomGenNum = Entry(Point(maxX/2+200, maxY/15), 5)
randomGenNum.draw(win)
randomGenNumSchool = Entry(Point(maxX/2+300, maxY/15), 5)
randomGenNumSchool.draw(win)
modeText.draw(win)
win.setBackground("light gray")
while True:
    point = win.getMouse()
    if (inside(point, makeModeSchool)):
        mode = 1
        modeText.undraw()
        modeText = Text(Point(maxX/2, maxY/20), "Placing: School")
        modeText.draw(win)
    elif (inside(point, makeModeHouse)):
        mode = 0
        modeText.undraw()
        modeText = Text(Point(maxX/2, maxY/20), "Placing: House")
        modeText.draw(win)
    elif (inside(point, makeModeSelect)):
        mode = 2
        modeText.undraw()
        modeText = Text(Point(maxX/2, maxY/20), "Select")
        modeText.draw(win)
    elif (inside(point, randomizeHouses)):
        if (randomGenNum.getText()) != None:
            for i in range(int(randomGenNum.getText())):
                makeHouse(Point(random.randint(0, maxX-20), random.randint(maxY/10,maxY-20)), "black")
        if (randomGenNumSchool.getText()) != None:
            for i in range(int(randomGenNumSchool.getText())):
                makeSchool(Point(random.randint(20, maxX-20), random.randint(maxY/10, maxY-20)))
        modifyHouses()
    else:
        if mode == 0:
            makeHouse(point, "black")
        elif mode == 1:
            makeSchool(point)
        elif mode == 2:
            selectHouse(point)
            continue
        modifyHouses()
