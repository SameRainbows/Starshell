# orbital — Python Turtle Reference

A curated reference of `turtle` module features relevant to building a physics simulator.

---

## 1. Creating & Managing Multiple Turtles

| Concept | How |
|---|---|
| Create a new turtle | `turtle.Turtle()` — each call creates an independent turtle object |
| Get the screen object | `turtle.Screen()` or `t.screen` (from any turtle) |
| Hide a turtle | `.hideturtle()` / `.ht()` |
| Show a turtle | `.showturtle()` / `.st()` |
| Check visibility | `.isvisible()` — returns True/False |

> **Key idea:** Every turtle is independent. You can have dozens on screen at once, each with its own position, heading, color, and size. This is how you'll represent multiple bodies.

---

## 2. Movement & Positioning

| Command | What it does |
|---|---|
| `.forward(distance)` / `.fd()` | Move in current heading direction |
| `.backward(distance)` / `.bk()` | Move opposite to heading |
| `.goto(x, y)` / `.setpos(x, y)` | Jump directly to coordinates |
| `.setx(x)` | Set only the x coordinate |
| `.sety(y)` | Set only the y coordinate |
| `.position()` / `.pos()` | Returns current (x, y) as a Vec2D |
| `.xcor()` | Returns current x |
| `.ycor()` | Returns current y |
| `.towards(x, y)` | Returns the angle toward a point (degrees) |
| `.distance(other)` | Returns distance to another turtle or (x, y) |
| `.setheading(angle)` / `.seth()` | Set absolute heading (0=east, 90=north) |
| `.heading()` | Returns current heading in degrees |
| `.left(angle)` / `.lt()` | Turn left by degrees |
| `.right(angle)` / `.rt()` | Turn right by degrees |

> **Key idea:** `.goto()` is your workhorse for physics — you calculate the new position, then send the turtle there. `.distance()` is critical for computing gravitational force between two bodies.

---

## 3. Pen Control (Drawing Trails)

| Command | What it does |
|---|---|
| `.penup()` / `.pu()` | Stop drawing when moving |
| `.pendown()` / `.pd()` | Start drawing when moving |
| `.pensize(width)` | Set trail thickness |
| `.pencolor(color)` | Set trail color |
| `.isdown()` | Returns True if pen is down |

> **Tip:** Orbit trails can look great with `.pendown()` and a thin pen. But drawing many trails slows Turtle down — be deliberate about when the pen is down.

---

## 4. Appearance & Shape

| Command | What it does |
|---|---|
| `.shape(name)` | Built-in: "arrow", "turtle", "circle", "square", "triangle", "classic" |
| `.shapesize(stretch_wid, stretch_len, outline)` | Scale the shape (1 = default ~20px) |
| `.color(pencolor, fillcolor)` | Set both colors at once |
| `.fillcolor(color)` | Set only the fill |
| `.pencolor(color)` | Set only the outline/trail color |
| `screen.register_shape(name, shape)` | Register a custom polygon as a shape |

### Custom Shapes
- You can register a polygon defined as a tuple of (x, y) coordinate pairs.
- This lets you create custom body shapes if circles aren't enough.

> **Color formats:** Turtle accepts named colors ("red", "cyan"), hex strings ("#FF5733"), and RGB tuples if you call `screen.colormode(255)` first.

---

## 5. Speed & Animation Control

| Command | What it does |
|---|---|
| `.speed(0)` | Fastest (no animation between moves) |
| `.speed(1)` | Slowest animated |
| `.speed(10)` | Fast animated |
| `screen.tracer(n, delay)` | **Critical.** Controls how often the screen refreshes. `tracer(0)` = manual refresh only. |
| `screen.update()` | Manually refresh the screen (use with `tracer(0)`) |
| `screen.delay(ms)` | Set delay between updates |

> **This is the most important section for a simulator.** By default, Turtle redraws after every single turtle movement, which is painfully slow with many objects. Set `tracer(0)` and call `update()` once per simulation step. This is the difference between 2 FPS and smooth animation.

---

## 6. Screen Setup

| Command | What it does |
|---|---|
| `screen.setup(width, height)` | Set window size in pixels |
| `screen.bgcolor(color)` | Set background color |
| `screen.title(string)` | Set window title |
| `screen.setworldcoordinates(llx, lly, urx, ury)` | Redefine the coordinate system |
| `screen.window_width()` | Get current window width |
| `screen.window_height()` | Get current window height |
| `screen.clear()` | Clear everything on screen |
| `screen.reset()` | Clear and reset all turtles |

> **Coordinate note:** By default, (0,0) is center of screen. A 700×700 window goes from roughly -350 to +350 on each axis.

---

## 7. Event Handling (User Interaction!)

### Mouse Events
| Command | What it does |
|---|---|
| `screen.onclick(function)` | Call `function(x, y)` when screen is clicked |
| `screen.onscreenclick(function, btn)` | Same but you can specify button (1=left, 2=middle, 3=right) |
| `turtle_obj.onclick(function)` | Call `function(x, y)` when *this specific turtle* is clicked |

### Keyboard Events
| Command | What it does |
|---|---|
| `screen.onkey(function, key)` | Call `function()` when key is released |
| `screen.onkeypress(function, key)` | Call `function()` when key is pressed (fires repeatedly if held) |
| `screen.listen()` | **Required** — activates keyboard listening. Call once after setting up key bindings. |

### Key Names
Common key names: `"space"`, `"Up"`, `"Down"`, `"Left"`, `"Right"`, `"Return"`, `"Escape"`, `"a"` through `"z"`, `"1"` through `"0"`, `"plus"`, `"minus"`

> **Key idea:** `screen.onclick()` is how you'll let users place bodies. `screen.onkey()` is how you'll let users start/stop/reset the simulation.

---

## 8. Text & Labels

| Command | What it does |
|---|---|
| `.write(text, align, font)` | Write text at current position |
| Align options | `"left"`, `"center"`, `"right"` |
| Font tuple | `("Arial", 14, "bold")` — (family, size, style) |
| `.clear()` | Clears everything *this turtle* has drawn (including text) |

> **Tip:** To display changing values (mass, velocity), dedicate a turtle to writing text. Call `.clear()` then `.write()` each frame to update it.

---

## 9. The Game Loop — `ontimer()`
sc
| Command | What it does |
|---|---|
| `screen.ontimer(function, t)` | Call `function` after `t` milliseconds |

> **This is your simulation heartbeat.** At the end of your update function, call `screen.ontimer(update, 16)` for roughly 60 FPS (16 ms per frame). This creates a recurring loop without blocking Turtle's event system.

---

## 10. Input Dialogs (Built-in UI)

| Command | What it does |
|---|---|
| `screen.textinput(title, prompt)` | Pop-up dialog for text input, returns string |
| `screen.numinput(title, prompt, default, minval, maxval)` | Pop-up dialog for number input, returns float |

> These are modal pop-ups (they freeze the simulation while open). Good for initial setup, but not for real-time interaction.

---

## 11. Stamping (Efficient Static Drawing)

| Command | What it does |
|---|---|
| `.stamp()` | Leave a permanent imprint of the turtle's current shape; returns a stamp ID |
| `.clearstamp(stamp_id)` | Remove a specific stamp |
| `.clearstamps()` | Remove all stamps from this turtle |

> **Use case:** If you want to show a fading trail behind a body, stamps can be more performant than pen trails for certain effects.

---

## 12. Underlying Tkinter Access

| Command | What it does |
|---|---|
| `screen.getcanvas()` | Returns the raw Tkinter Canvas widget |
| Canvas `.create_rectangle()`, `.create_oval()`, etc. | Draw directly on the canvas |
| Canvas `.create_window()` | Embed Tkinter widgets (buttons, sliders, entry fields) onto the canvas |

> **This is the answer to your UI question.** Turtle runs on top of Tkinter. You can reach "under the hood" to access the full Tkinter toolkit — buttons, sliders (`Scale` widget), entry fields, labels, frames. This is how you build a real UI alongside your Turtle canvas.

---

## 13. Useful Math (Python's `math` module)

Not Turtle-specific, but you'll need these constantly:

| Function | What it does |
|---|---|
| `math.sqrt(x)` | Square root |
| `math.atan2(y, x)` | Angle from origin to point (radians) — note: y comes first! |
| `math.sin(angle)`, `math.cos(angle)` | Trig functions (radians) |
| `math.radians(deg)` | Convert degrees to radians |
| `math.degrees(rad)` | Convert radians to degrees |
| `math.hypot(dx, dy)` | Distance — same as `sqrt(dx² + dy²)` |

---

## Quick Physics Formulas You'll Need

These aren't commands, just the math you'll be implementing:

| Concept | Formula |
|---|---|
| Gravitational force | F = G × (m₁ × m₂) / r² |
| Acceleration from force | a = F / m |
| Velocity update | v_new = v_old + a × dt |
| Position update | pos_new = pos_old + v × dt |
| Distance between two points | r = √((x₂−x₁)² + (y₂−y₁)²) |
| Force direction (angle) | θ = atan2(y₂−y₁, x₂−x₁) |
| Force components | Fx = F × cos(θ),  Fy = F × sin(θ) |
| Collision detection | if distance < radius₁ + radius₂ |

> **G (gravitational constant):** In real physics it's 6.674 × 10⁻¹¹. In your simulation, you'll pick a value that *feels good* at your scale. This is a tuning parameter, not a fixed truth.

---

*Last updated: June 2026*
