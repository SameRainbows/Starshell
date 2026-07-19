import turtle
import math
import tkinter

__ = turtle.Turtle()
screen = __.screen
__.speed(0)
__.color('white')
__.pu()
__.hideturtle()
screen.tracer(0)
screen.setup(700,700)
screen.bgcolor('black')
objs = []
G = 10

spawn_mass = 100
spawn_size = spawn_mass / 10

camera_x = 0
camera_y = 0

class Particle:
    def __init__(self, mass, vx, vy, x, y, radius):
        # store parameters on the instance

        self.turt = turtle.Turtle()
        self.turt.speed(0)
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.radius = radius

        # optional: register the instance in an external list
        

        # initialize turtle appearance / position

        objs.append(self)
        self.turt.pu()
        self.turt.shape('circle')
        self.turt.color('white')
        self.turt.shapesize(self.radius / 10, self.radius / 10)
        self.turt.goto(x, y)
 
Particle(3000, 0, 0, 0, 0, 30)




def distance(obj1,obj2):
    return math.sqrt(((obj2.x ) - (obj1.x )) ** 2 + ((obj2.y ) - (obj1.y )) **2)

def force(obj1, obj2):
    return G * ((obj1.mass * obj2.mass) / (distance(obj1, obj2) ** 2))

def angle(obj1, obj2):
    return math.atan2(obj2.y - obj1.y, obj2.x - obj1.x)

def velo_update(obj, force, angle, mass):
    vx = obj.vx
    vy = obj.vy
    Fx = force * math.cos(angle)
    Fy = force * math.sin(angle)
    ax = Fx / mass
    ay = Fy / mass
    vx += ax
    vy += ay
    obj.vx = vx
    obj.vy = vy
    return 

def merge(obj1, obj2):
    global objs # (obj1 mass * vx plus obj2 mass * vx) divided by total mass
    new_m = obj1.mass + obj2.mass # mass of the merged object
    new_vx = (obj1.mass * obj1.vx + obj2.mass * obj2.vx) / (obj1.mass + obj2.mass)
    new_vy = (obj1.mass * obj1.vy + obj2.mass * obj2.vy) / (obj1.mass + obj2.mass)
    obj1.turt.hideturtle()
    obj2.turt.hideturtle()
    Particle(new_m, new_vx, new_vy, obj1.x, obj1.y, math.sqrt((obj1.radius ** 2) + obj2.radius ** 2))
    objs.remove(obj1)
    objs.remove(obj2)

def merge_collisions():
    merged = False
    for body in objs:
        if merged == True:
            break
        for other in objs:
            if other == body:
                continue
            else:
                if distance(body, other) < body.radius + other.radius:
                    merge(body, other)
                    merged = True
                    break

def update():
    global objs
    merge_collisions()
    for body in objs:
        for other in objs:
            
            if body == other:
                continue
            else:
                F = force(body, other)
                A = angle(body, other)
                velo_update(body, F, A, body.mass)


        
            
        body.x += body.vx 
        body.y += body.vy 

        body.turt.goto(body.x - camera_x, body.y - camera_y)
    merge_collisions()
    screen.update()
    screen.ontimer(update, t=30)

state = None
press_x = None
press_y = None
def sling(event):

    global state
    global press_x
    global press_y
    
    swhh = screen.window_height() / 2
    swwh = screen.window_width() / 2
    if state == None:
        press_x = (event.x + camera_x) - swwh
        press_y = swhh - (event.y - camera_y)
        state = press_x, press_y
    else:
        release_x = event.x + camera_x - swwh
        release_y = swhh - (event.y - camera_y)
        state = None
        vx = (press_x - release_x) * 0.2
        vy = (press_y - release_y) * 0.2
        __.clear()
        Particle(spawn_mass, vx, vy, press_x, press_y, spawn_size) 


    return
def aim(event):
    swhh = screen.window_height() / 2
    swwh = screen.window_width() / 2
    __.clear()
    __.pu()
    __.goto(press_x  - camera_x , press_y  - camera_y)
    __.pd()
    __.goto(event.x - swwh, swhh - event.y )
    screen.update()
def w():
    global camera_y
    camera_y += 20
def a():
    global camera_x
    camera_x -= 20
def s():
    global camera_y
    camera_y -= 20
def d():
    global camera_x
    camera_x += 20

def mass_up(event):
    global spawn_mass
    global spawn_size
    if spawn_mass + 10 < 1000:
        spawn_mass += 10
        spawn_size = spawn_mass / 10

def mass_down(event):
    global spawn_mass
    global spawn_size
    if spawn_mass - 10 > 0:
        spawn_mass -= 10
        spawn_size = spawn_mass / 10

def reset():
    for i in range(len(objs)):
        objs[i].turt.hideturtle()

    objs.clear()
    global camera_x
    global camera_y
    global G
    camera_x = 0
    camera_y = 0
    G = 10
    Particle(3000,0,0,0,0,30)
def g_up():
    global G
    G += 10
canvas = screen.getcanvas()
canvas.bind('<ButtonPress-1>', sling)
canvas.bind('<ButtonRelease-1>', sling)
canvas.bind('<B1-Motion>', aim)
canvas.bind('<Up>', mass_up)
canvas.bind('<Down>', mass_down)

screen.onkeypress(w, 'w')
screen.onkeypress(a, 'a')
screen.onkeypress(s, 's')
screen.onkeypress(d, 'd')
screen.onkeypress(reset, 'r')
screen.onkeypress(g_up, 'g')

screen.listen()
update()
turtle.done()