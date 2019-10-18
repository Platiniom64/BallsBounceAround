"""
This code was written by Vladimir Hanin on the 05/03/2018
Please use Python 2.7
"""

from Tkinter import *
import random
from random import randint
import math
import tkFont


#----------window creation and canvas----------
size_width_window = 1300
size_height_window = 720

#window
tk = Tk()
tk.title("Balls moving around")
tk.geometry((str(size_width_window) + "x" + str(size_height_window)))

#canvas where the balls are
size_width_canvas = 700
size_height_canvas = 700
canvas = Canvas(tk, width=size_width_canvas, height=size_height_canvas, bg="black")
canvas.pack(side=LEFT)


#------------creation of a normal ball--------------
entered_speed = 1
listofballs = []
class Ball:
    def __init__(self, x, y, directionx, directiony):

        #initial position when a normal ball is called
        if x == 0 and y == 0:
            self.x = random.randint(0, size_width_canvas - 1)
            self.y = random.randint(0, size_width_canvas - 1)
        #initial position when the custom ball is called
        else:
            self.x = x
            self.y = y
            
        try:
            self.size = int(givensizeball.get())
        except:
            self.size = 0

        
        #creating ball at the position chosen
        self.shape = canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size, outline="white", fill="white")

        #inital given speed for calculations
        self.speed = 1
    

        #when the ball has no special direction
        if directionx == 0 and directiony == 0:
            if var2.get() == 0:
                #direction for x as unit vector
                self.speedx = random.uniform(-self.speed, self.speed)

                #firection for y as unit vector
                listdirectiony = [1,-1]
                self.speedy = math.sqrt(self.speed * self.speed - self.speedx * self.speedx) * random.choice(listdirectiony)
            else:
                listsmoothdirection = [1, -1]
                self.speedx = random.choice(listsmoothdirection)
                self.speedy = random.choice(listsmoothdirection)

        #when the ball has a special direction
        else:
            self.speedx = directionx
            self.speedy = directiony


    def ball_update(self):
        
        #check if pressed is true, so set the movement to the entered value
        self.pos = canvas.coords(self.shape)

        #if the x coordinate is too much to the left, correction to avoid the side of the canvas
        if self.pos[0] < 0:
            self.pos[0] = 0

        if self.pos[2] > size_width_canvas:
            self.pos[2] = size_width_canvas

        if self.pos[1] < 0:
            self.pos[1] = 0

        if self.pos[3] > size_height_canvas:
            self.pos[3] = size_height_canvas
            
       
        
        if self.pos[2] == size_width_canvas or self.pos[0] == 0:
            self.speedx *= -1
        if self.pos[3] == size_height_canvas or self.pos[1] == 0:
            self.speedy *= -1

        canvas.move(self.shape, self.speedx*entered_speed, self.speedy*entered_speed)

        #for the creation of the line
        return self.pos
    

#-------------------ball circular path:
listofcircularballs = []
class Ball2:
    def __init__(self):
        self.center_x = size_width_canvas/2
        self.center_y = size_height_canvas/2
        self.distance_center = int(givenradius.get())
        self.radius = 0
        self.angle = 0
        self.anglespeed = 1
        self.currx = 0
        self.curry = 0
        
        self.pos = [0,0,0,0]
        
        # calculate oval coordinates
        self.calculate_position()

        # create oval
        self.shape = canvas.create_oval(self.pos[0], self.pos[1], self.pos[2], self.pos[3])

    
    def calculate_position(self):
        # calculate new position of object
        self.x = self.center_x - math.sqrt(self.distance_center)*40* math.sin(math.radians(-self.angle))
        self.y = self.center_y - math.sqrt(self.distance_center)*40* math.cos(math.radians(-self.angle))

        # save positon so other object can use it as its center of rotation
        self.currx = self.x
        self.curry = self.y

        # calcuate oval coordinates
        self.pos[0] = self.x - self.radius
        self.pos[1] = self.y - self.radius
        self.pos[2] = self.x + self.radius
        self.pos[3] = self.y + self.radius

        return self.pos[0], self.pos[1], self.pos[2], self.pos[3]

    def move_object(self):
        # calculate oval coordinates
        self.pos[0], self.pos[1], self.pos[2], self.pos[3] = self.calculate_position()

        # move oval
        canvas.coords(self.shape, self.pos[0], self.pos[1], self.pos[2], self.pos[3])

    def ball_update(self):
        self.angle += self.anglespeed*entered_anglespeed
        self.move_object()

    
#-------------lines----------------
class Line:
    def __init__(self, firstball, secondball):
        #randwom line
        self.line = canvas.create_line(20, 20, 400, 400, fill="white")
        self.firstballcoords = firstball.pos
        self.secondballcoords = secondball.pos
        
        self.centerx_firstball = 0
        self.centery_firstball = 0

        self.centerx_secondball = 0
        self.centery_secondball = 0
      
    #updates the postion of the line
    def line_update(self, ball1, ball2, listoflines):
        #delete random line from above
        canvas.delete(self.line)

        self.firstballcoords = ball1.pos
        self.secondballcoords = ball2.pos

        self.centerx_firstball = (self.firstballcoords[2]+self.firstballcoords[0])/2
        self.centery_firstball = (self.firstballcoords[3]+self.firstballcoords[1])/2

        self.centerx_secondball = (self.secondballcoords[2]+self.secondballcoords[0])/2
        self.centery_secondball = (self.secondballcoords[3]+self.secondballcoords[1])/2

        differencex = abs(self.firstballcoords[0]-self.secondballcoords[0])
        differencey = abs(self.firstballcoords[1]-self.secondballcoords[1])

        try:
            tocomparelength = int(givenlengthbreak.get())
        except:
            tocomparelength = 0
            
        if differencex < tocomparelength and differencey < tocomparelength:
            self.line = canvas.create_line(self.centerx_firstball+ball1.speedx*entered_speed, self.centery_firstball+ball1.speedy*entered_speed, self.centerx_secondball+ball2.speedx*entered_speed, self.centery_secondball+ball2.speedy*entered_speed, fill="white")
            listoflines.append(self.line)


#--------------update lines on the canvas-----------
listoflines = []
listofsecretlines = []

def updatelines(list_balls, listoflines):

    #draws a line between each dot
    for ball1 in list_balls:
        for ball2 in list_balls:
            if ball1 == ball2:
                continue
            else:
                newline = Line(ball1, ball2)
                newline.line_update(ball1, ball2, listoflines)
                
    tk.update()        


    #enable trace
    if var1.get() == 0:
        for line in listoflines:
            canvas.delete(line)
        del listoflines[:]

    else:
        for line in listoflines:
            listofsecretlines.append(line)
        del listoflines[:]
        
   
#-------------buttons and methods-------------
entered_speed = 1
def enterspeed():
    global entered_speed
    try:
        entered_speed = int(speedofballs.get())
    except:
        entered_speed = 0
    
    for ball in listofballs:
        ball.speed = entered_speed
            

entered_anglespeed = 1
def enteranglespeed():
    global entered_anglespeed
    try:
        entered_anglespeed = (float(givenspeedofballs.get()))/10
    except:
        entered_anglespeed = 0
    
    for ball in listofcircularballs:
        ball.anglespeed = entered_anglespeed
        
def createball():
    newball = Ball(0, 0, 0, 0)
    listofballs.append(newball)

def createsmoothball():
    setvaluesmoothpath()
    createball()

def removeball():
    ballremove = random.choice(listofballs)
    canvas.delete(ballremove.shape)
    listofballs.remove(ballremove)

def removeallballs():
    for ball in listofballs:
        canvas.delete(ball.shape)
    del listofballs[:]

def resetlines():
    for line in listofsecretlines:
        canvas.delete(line)
    for line in listoflines:
        canvas.delete(line)
    del listoflines[:]

def updatelabels():
    numdot.config(text="there are " + str(len(listofballs)) + " dots")

def setentryvalue(what_to_change, text):
    what_to_change.delete(0, END)
    what_to_change.insert(0, text)


def togglecustom1():
    #horizontal line middle
    newdot1 = Ball(1, size_height_canvas/2, 1, 0)
    listofballs.append(newdot1)

def togglecustom2():
    #vertical line middle
    newdot1 = Ball(size_width_canvas/2, size_height_canvas/2+1, 0, 1)
    listofballs.append(newdot1)
    
def togglecustom3():
    #vertical star
    togglecustom1()
    togglecustom2()

def togglecustom4():
    #negative diagonal
    newdot1 = Ball(size_width_canvas/4, size_height_canvas/4, 1, 1)
    listofballs.append(newdot1)

def togglecustom5():
    #positive diagonal
    newdot2 = Ball(size_width_canvas/4, (size_height_canvas/2)+(size_height_canvas/4), -1, 1)
    listofballs.append(newdot2)

def togglecustom6():
    #diagonal star
    togglecustom4()
    togglecustom5()

def togglecustom7():
    newdot1 = Ball(size_width_canvas/4, size_height_canvas/4, 1, -1)
    listofballs.append(newdot1)

def togglecustom8():
    newdot1 = Ball(size_width_canvas/4, size_height_canvas/4, -1, 1)
    listofballs.append(newdot1)

def togglecustom9():
    newdot = Ball2()
    listofcircularballs.append(newdot)
    listofballs.append(newdot)

def togglecustom10():
    togglecustom3()
    togglecustom6()

def togglecustom11():
    togglecustom3()
    tk.after(300, togglecustom3)


#------automatic--------
def settraceto1():
    var1.set(1)

listoffdrawings = [togglecustom1, togglecustom11, createball, togglecustom10, togglecustom2, togglecustom3, togglecustom4, togglecustom5, togglecustom6, togglecustom7, togglecustom8, togglecustom9]
def triggerautomatic():
    choice = random.choice(listoffdrawings)
    choice()
    if choice == togglecustom9:
        createball()
    elif choice == togglecustom3 or choice == togglecustom6 or choice == togglecustom11 or choice == togglecustom10:
        pass
    else:
        createball()
        createball()
        

    tk.after(9000, removeallballs)
    tk.after(9000, resetlines)
    tk.after(9000, triggerautomatic)


def triggerautomaticandsettraceto1():
    var1.set(1)
    var2.set(1)
    setentryvalue(givenradius, 35)
    setentryvalue(givenspeedofballs, 20)
    
    triggerautomatic()
    
    
    
    
#--------labels---------------
labelFont = tkFont.Font(underline=1)

#settings ball
dotlabels = Label(tk, text="Settings balls:", font=labelFont)
dotlabels.place(x=size_width_canvas + 20, y = 5)

buttoncreatedot = Button(tk, text="create ball", command=createball)
buttoncreatedot.place(x=size_width_canvas + 20, y = 35)

var2 = IntVar()
uniformpath = Checkbutton(tk, variable=var2, text="uniform parth")
uniformpath.place(x=size_width_canvas + 125, y = 39)

buttonremoveball = Button(tk, text="remove one ball", command=removeball)
buttonremoveball.place(x=size_width_canvas + 20, y = 65)

buttonremoveallballs = Button(tk, text="remove all balls", command=removeallballs)
buttonremoveallballs.place(x=size_width_canvas + 20, y = 95)

numdot = Label(tk, text="there are " + str(len(listofballs)) + " dots")
numdot.place(x=size_width_canvas + 20, y = 125)

#second columns settings ball
textgivenlength = Label(tk, text="max len of lines:")
textgivenlength.place(x=size_width_canvas + 280, y = 39)

givenlengthbreak = Entry(tk, width="10")
givenlengthbreak.place(x=size_width_canvas + 390, y = 35)
setentryvalue(givenlengthbreak, 710)

textgivensize = Label(tk, text="size balls:")
textgivensize.place(x=size_width_canvas + 280, y = 67)

givensizeball = Entry(tk, width="10")
givensizeball.place(x=size_width_canvas + 360, y = 63)
setentryvalue(givensizeball, 0)


#settings speed ball
speedlabel = Label(tk, text="speed:")
speedlabel.place(x=size_width_canvas + 20, y = 150)

speedofballs = Entry(tk, width="10")
speedofballs.place(x=size_width_canvas + 70, y = 147)
setentryvalue(speedofballs, 10)

#circular ball path
customcreatecircle = Button(tk, text="create circular ball", command=togglecustom9)
customcreatecircle.place(x=size_width_canvas + 20, y = 185)

textanglespeed = Label(tk, text="angle speed:")
textanglespeed.place(x=size_width_canvas + 20, y = 215)

givenspeedofballs = Entry(tk, width="10")
givenspeedofballs.place(x=size_width_canvas + 113, y = 212)
setentryvalue(givenspeedofballs, 10)

textradius = Label(tk, text="radius of balls:")
textradius.place(x=size_width_canvas + 20, y = 240)

givenradius = Entry(tk, width="10")
givenradius.place(x=size_width_canvas + 120, y = 240)
setentryvalue(givenradius, 30)


#settings line
linelabels = Label(tk, text="Settings lines:", font=labelFont)
linelabels.place(x=size_width_canvas + 20, y = 270)

var1 = IntVar()
checktrace1 = Checkbutton(tk, variable=var1, text="trace switch")
checktrace1.place(x=size_width_canvas + 20, y = 295)

resettrace = Button(tk, text="remove all lines", command=resetlines)
resettrace.place(x=size_width_canvas + 20, y = 320)


#customs
customdrawings = Label(tk, text="Custom drawings:", font=labelFont)
customdrawings.place(x=size_width_canvas + 20, y = 360)

custom1 = Button(tk, text="horizontal line middle", command=togglecustom1)
custom1.place(x=size_width_canvas + 20, y = 390)

custom2 = Button(tk, text="vertical line middle", command=togglecustom2)
custom2.place(x=size_width_canvas + 20, y = 420)

custom3 = Button(tk, text="vertical star", command=togglecustom3)
custom3.place(x=size_width_canvas + 20, y = 450)


custom4 = Button(tk, text="diagonal line negative", command=togglecustom4)
custom4.place(x=size_width_canvas + 20, y = 490)

custom5 = Button(tk, text="diagonal line positive", command=togglecustom5)
custom5.place(x=size_width_canvas + 20, y = 520)

custom6 = Button(tk, text="diagonal star", command=togglecustom6)
custom6.place(x=size_width_canvas + 20, y = 550)


custom7 = Button(tk, text="inside trajectory clockwise from left", command=togglecustom7)
custom7.place(x=size_width_canvas + 20, y = 590)

custom8 = Button(tk, text="inside trajectory anti-clockwise from left", command=togglecustom8)
custom8.place(x=size_width_canvas + 20, y = 620)


#automatic
automatic = Button(tk, text="automatic", command=triggerautomaticandsettraceto1)
automatic.place(x=size_width_canvas + 20, y = 670)

#-------------loop-------------
#this function is to slow down the balls depending on the computer
def wait():
    tk.after(10)

while True:

    #calling enterspeed to set the speed to the balls
    enterspeed()
    enteranglespeed()
    #updatelabel of the number of balls in the canvas
    updatelabels()

    #update line position
    updatelines(listofballs, listoflines)

    #update positin dot
    for ball in listofballs:
        ball.ball_update()



    wait()

tk.mainloop()
