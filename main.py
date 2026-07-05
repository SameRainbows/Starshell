import turtle
import math
import tkinter

t = turtle.Turtle() 
t.screen.setup(700,700)
screen = t.screen
screen.bgcolor('black')
objs = []
# structure: [turtle, mass, vx, vy, x, y, old_x, old_y, radius]

canvas = screen.getcanvas()

counter = 0
def color_fun():
    global counter
    global new_body_color
   
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'white', 'pink']
    new_body_color = colors[counter]
    color_button['text']=f'{new_body_color}'

    counter += 1
    if counter == len(colors):
        counter = 0

def reset():
    for i in range(len(objs)):
        objs[i][0].hideturtle()
    objs.clear()
    global cam_x
    global cam_y
    cam_x = 0
    cam_y = 0
    p = turtle.Turtle()
    p.shape("circle")
    p.shapesize(2,2)
    p.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
    p.pu()
    p.color('white')
    objs.append([p, 100, 0, 0, 0, 0, 0, 0, 20])
    

color_button = tkinter.Button(screen._root, text="Color cycle", command=color_fun)
reset_button = tkinter.Button(screen._root, text='Reset', command=reset)

G_slider = tkinter.Scale(screen._root,label='Gravity', from_=100, to=1000, orient="horizontal")
Mass_slider = tkinter.Scale(screen._root,label='Mass', from_=1, to=100, orient="horizontal")

canvas.create_window(295,-330, window=reset_button)
canvas.create_window(295,-300, window=color_button)
canvas.create_window(290,-255, window=G_slider)
canvas.create_window(290,-192, window=Mass_slider)



cam_x = 0
cam_y = 0


t.shape("circle")
t.shapesize(2,2)
t.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
t.pu()
t.color('white')

objs.append([t, 100, 0, 0, 0, 0, 0, 0, 20])



G = None # 100-1000 works best!
def distance(obj1, obj2): # r = √((x₂−x₁)² + (y₂−y₁)²)
    return math.sqrt((obj2[4]-obj1[4]) ** 2 + (obj2[5] - obj1[5]) ** 2)

def force(obj1, obj2): # F = G × (m₁ × m₂) / r²
    r = distance(obj1, obj2)
    if r < obj1[8] + obj2[8]:
        return 0
    force = G * (obj1[1] * obj2[1]) / r ** 2
    return force

def direction(obj1,obj2): # θ = atan2(y₂−y₁, x₂−x₁)
    return math.atan2(obj2[5] - obj1[5] , obj2[4]- obj1[4])

def velo_update(obj, force, angle, mass):    # Fx = F × cos(θ),  Fy = F × sin(θ) 
    Fx = force * math.cos(angle)
    Fy = force * math.sin(angle)
    ax = Fx / mass
    ay = Fy / mass
    obj[2] += ax
    obj[3] += ay
    return 

def passed_through(body, other):
    body_old_x = body[6]
    body_old_y = body[7]
    body_x = body[4]
    body_y = body[5]
    body_rd = body[8]
    
    other_x = other[4]
    other_y = other[5]
    other_rd = other[8]

    path_x = body_x - body_old_x
    path_y = body_y - body_old_y

    arrow_x = other_x - body_old_x
    arrow_y = other_y - body_old_y

    if body_old_x == body_x and body_old_y == body_y:
        return False

    t = (arrow_x * path_x + arrow_y * path_y) / (path_x * path_x + path_y * path_y)

    radii = other_rd + body_rd

    if t < 0:
        t = 0
    elif t > 1:
        t = 1

    closest_x = body_old_x + path_x * t
    closest_y = body_old_y + path_y * t

    distance = math.sqrt((other[4]-closest_x) ** 2 + (other[5] - closest_y) ** 2)
    
    if distance <= radii:
        return True
    else:
        return False



def merge(obj1, obj2):
    global objs
    new_m = obj1[1] + obj2[1] # mass of the merged object

    # The new velocity depending on the velocities of the merging objects
    new_vx = (obj1[1] * obj1[2] + obj2[1] * obj2[2]) / new_m # (obj1 mass * vx plus obj2 mass * vx) divided by total mass
    new_vy = (obj1[1] * obj1[3] + obj2[1] * obj2[3]) / new_m # (obj1 mass * vy plus obj2 mass * vy) divided by total mass

    # The center of mass where we will spawn the new 'merged' object
    new_x = (obj1[1] * obj1[4] + obj2[1] * obj2[4]) / new_m # (obj1 mass * obj1x plus obj2 mass * obj2x) / total mass
    new_y = (obj1[1] * obj1[5] + obj2[1] * obj2[5]) / new_m # (obj1 mass * obj1y plus obj2 mass * obj2y) / total mass

    new_radius = math.sqrt(obj1[8] ** 2 + obj2[8] ** 2)
    shape_size = new_radius / 10

    new_body = turtle.Turtle()
    new_body.pu()
    new_body.shapesize(shape_size, shape_size)
    new_body.shape('circle')
    new_body.color(new_body_color)
    new_body.speed(0)
    obj1[0].hideturtle() # Hide merging turtles and replace them with new_body
    obj2[0].hideturtle()
    objs.remove(obj1) # Remove them from our list of lists
    objs.remove(obj2)
    objs.append([new_body, new_m, new_vx, new_vy, new_x, new_y, new_x, new_y, new_radius]) # Add new_body to our list of lists
    new_body.goto(new_x - cam_x, new_y - cam_y)
    
def merge_collisions():
    merged = False
    for body in objs:
        if merged == True:
            break
        for other in objs:
            if other == body:
                continue
            else:
                if distance(body, other) < body[8] + other[8] or passed_through(body, other):
                    merge(body, other)
                    merged = True
                    break

def move():
    global objs
    global G
    G = G_slider.get()
    merge_collisions() # Check merges with already touching objects
    for body in objs:
        for other in objs:
            if other == body:
                continue
            else:
                F = force(body, other)
                D = direction(body, other)
                velo_update(body, F, D, body[1])

        vx = body[2]
        vy = body[3]
        body[6] = body[4] # Store the old coords before changing them
        body[7] = body[5]

        body[4] += vx
        body[5] += vy
        body[0].goto(body[4] - cam_x, body[5] - cam_y)

    merge_collisions() # Check again after moving a frame
    screen.ontimer(move, t=1) # Set to 1 for maximum frames set to 2 or higher for more chunky but less compute intensive simulations
    








press_x = None
press_y = None

new_body_color = 'white'
sling_state = None
def sling(event):
    global sling_state
    global press_x
    global press_y
    scww = canvas.winfo_width() / 2
    scwh = canvas.winfo_height() / 2

    if sling_state == None:
        press_x = (event.x - scww) + cam_x
        press_y = (scwh - event.y) + cam_y
        sling_state = press_x, press_y
    else:
        release_x = (event.x - scww) + cam_x
        release_y = (scwh - event.y) + cam_y
        sling_state = None
        vx = press_x - release_x
        vy = press_y - release_y
        new_body = turtle.Turtle()
        new_body.shapesize(1,1)
        new_body.color(new_body_color)
        new_body.shape('circle')
        new_body.speed(0)
        new_body.penup()
        new_body.goto(press_x - cam_x, press_y - cam_y)
        objs.append([new_body, Mass_slider.get(), vx, vy, press_x, press_y, press_x, press_y, 10])
        
def w():
    global cam_y
    cam_y += 10
    cam_y += 10
def a():
    global cam_x
    cam_x -= 10
    cam_x -= 10
def s():
    global cam_y
    cam_y -= 10
    cam_y -= 10
def d():
    global cam_x
    cam_x += 10
    cam_x += 10

canvas.bind("<ButtonPress-1>", sling)
canvas.bind("<ButtonRelease-1>", sling)

screen.onkeypress(w, "w")
screen.onkeypress(a, "a")
screen.onkeypress(s, "s")
screen.onkeypress(d, "d")

screen.onkeypress(w, "Up")
screen.onkeypress(a, "Left")
screen.onkeypress(s, "Down")
screen.onkeypress(d, "Right")

screen.listen()


move()

turtle.done()
