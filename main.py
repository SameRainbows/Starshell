import turtle
import math

t = turtle.Turtle() 
t.screen.setup(700,700)
screen = t.screen
objs = []

t.shape("circle")
t.shapesize(4,4)
t.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
t.pu()

objs.append([t, 100, 0, 0])



G = 1000
def distance(t1, t2): # t1.distance(t2)
    
    return t1.distance(t2)

def force(obj1, obj2): # F = G × (m₁ × m₂) / r²
    force = G * (obj1[1] * obj2[1]) / distance(obj1[0], obj2[0]) ** 2
    return force

def direction(obj1,obj2): # θ = atan2(y₂−y₁, x₂−x₁)
    t1 = obj1[0]
    t2 = obj2[0]
    angle = math.atan2(t2.ycor() - t1.ycor(), t2.xcor() - t1.xcor())
    return angle

def velo_update(obj, force, angle, mass):    # Fx = F × cos(θ),  Fy = F × sin(θ)
    global vx
    global vy
    
    Fx = force * math.cos(angle)
    Fy = force * math.sin(angle)
    ax = Fx / mass
    ay = Fy / mass
    obj[2] += ax
    obj[3] += ay
    return 

def move():
    global objs
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

        x = body[0].xcor()
        y = body[0].ycor()

        body[0].goto(x + vx, y + vy)

    screen.ontimer(move, t=1)
    """obj1 = objs[0]
    obj2 = objs[1]

    vx = obj2[2]
    vy = obj2[3]

    F = force(obj1, obj2)
    D = direction(obj2, obj1)
    velo_update(objs[1], F, D, obj2[1])

    x = obj2[0].xcor()
    y = obj2[0].ycor()
    
    obj2[0].goto(x + vx, y + vy)
    screen.ontimer(move, t=1)"""

canvas = screen.getcanvas()
press_x = None
press_y = None


sling_state = None
def sling(event):
    global sling_state
    global press_x
    global press_y

    if sling_state == None:
        press_x = event.x - 350 
        press_y = 350 - event.y
        sling_state = press_x, press_y
    else:
        release_x = event.x - 350 
        release_y = 350 - event.y
        sling_state = None
        vx = press_x - release_x
        vy = press_y - release_y
        new_body = turtle.Turtle()
        new_body.shapesize(1,1)
        new_body.color("orange")
        new_body.shape('circle')
        new_body.speed(0)
        new_body.penup()
        new_body.goto(press_x, press_y)
        objs.append([new_body, 1, vx, vy])
        

    

canvas.bind("<ButtonPress-1>", sling)
canvas.bind("<ButtonRelease-1>", sling)





move()

turtle.done()
