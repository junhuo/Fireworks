## Jun Huo
## March 02, 2014

## This is a simple fireworks generator, written in Python 2.7


from Tkinter import *
import random
import math

##A single firework, made up of array of dots (sparks)
class Firework(object):
    def __init__(self, canvas, cx, cy, life):
        self.cx = cx
        self.cy = cy
        self.canvas = canvas
        self.life = life
        self.allSparks = []
        self.tics = 0
        ##Randomly generate number of sparks, maximum radius, and color
        self.nSparks = random.randint(60,80)
        self.maxRadius = random.randint(canvas.height/6,canvas.height/4)
        self.red = random.randint(50,255)
        self.green = random.randint(50,255)
        self.blue = random.randint(50,255)
        self.color = "#%02x%02x%02x" %(self.red,self.green,self.blue)
        ##Determine end position/path of each spark
        for x in xrange(self.nSparks):
            endr = random.randint(0,self.maxRadius)
            deg = random.randint(0,360)
            degree = math.radians(deg)
            endx = cx + endr*math.cos(degree)
            endy = cy + endr*math.sin(degree)
            vx = (endx-cx)/self.life
            vy = (endy-cy)/self.life
            self.allSparks.append([cx,cy,vx,vy]) ##No acceleration

    def update(self):
        self.tics+=1
        ##Simulate fading-out
        if (self.tics>(self.life/2)):
            self.red-=(2.5*self.red/self.life)
            self.green-=(2.5*self.green/self.life)
            self.blue-=(2.5*self.blue/self.life)
            self.color = "#%02x%02x%02x" %(self.red,self.green,self.blue)
        for s in self.allSparks:
            s[0]+=s[2]
            s[1]+=s[3]

    def draw(self):
        for s in self.allSparks:
            self.canvas.create_oval(s[0],s[1],s[0]+5,s[1]+5,fill=self.color)

##---------------------------------------##

class Main(object):
    def mousePressed(self, event):
        ##Add new firework at each click
        self.allFireworks.append( \
            Firework(self.canvas, event.x, event.y, self.sparklife))
        self.redrawAll()

    def redrawAll(self):
        self.canvas.delete(ALL) ##Delete everything from canvas
        self.canvas.create_rectangle(0,0, self.width, self.height, fill="black")
        for fw in self.allFireworks:
            if (fw.tics>self.sparklife):
                ##Firework died
                self.allFireworks.remove(fw)
        for fw in self.allFireworks:
            fw.draw()

    def timerFired(self):
        for fw in self.allFireworks:
            ##Update positions and tics of all fireworks
            fw.update()
        self.redrawAll()
        ##Re-call timerFired
        self.canvas.after(self.timerFiredDelay, self.timerFired)

    def init(self):
        self.allFireworks = []
        self.sparklife = 20
        self.timerFired()

    def run(self, width, height):
        ##Create root/canvas
        root = Tk()
        root.resizable(width=FALSE, height=FALSE)
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        self.width = self.canvas.width = width
        self.height = self.canvas.height = height
        root.canvas = self.canvas.canvas = self.canvas
        ##Call mousePressed at any left-click
        root.bind("<Button-1>", self.mousePressed)
        ##Set up timerFired events
        self.timerFiredDelay = 60 ##Milliseconds
        self.init()
        ##Run until window is closed
        root.mainloop()


##---------------------------------------##
##Run program
app = Main()
app.run(600,400)
