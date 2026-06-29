# orbital 

A 2D astronomical physics simulator built entirely in Python Turtle — no external libraries.

## What it does

orbital simulates gravitational interactions between bodies in 2D space. A planet orbits a central star, with its path determined by real physics: gravitational force, acceleration, and velocity — computed from scratch each frame.

## How the physics works

Every frame, the simulation:
1. Computes the **distance** between each pair of bodies
2. Calculates the **gravitational force** — `F = G × (m₁ × m₂) / r²`
3. Finds the **direction** of that force using `atan2`
4. Splits the force into **x and y components** — `Fx = F × cos(θ)`, `Fy = F × sin(θ)`
5. Computes **acceleration** — `a = F / m`
6. Updates **velocity** — `vx += ax`, `vy += ay`
7. Updates **position** — `goto(x + vx, y + vy)`

Orbits aren't hardcoded. They emerge from the math.

## Running it

Requires Python 3 (no pip installs needed — only the standard library).

```
python main.py
```

## Tuning the simulation

Three variables at the top of `main.py` control the feel of the simulation:

| Variable | Effect |
|---|---|
| `G` | Gravitational constant — higher means stronger pull |
| `vx`, `vy` | Initial velocity of the orbiting body |
| Mass values | Set per body in the `objs` list |

## Project goals

This is a learning project, intentionally built by hand to develop intuition for physics, math, and simulation. Planned features include:

- Multiple interacting bodies
- Click-to-place new bodies
- Collision detection and merging
- UI for setting mass, velocity, and color before placing a body

## Files

- `main.py` — the simulation
- `cmds.md` — a reference guide for Python Turtle features used in this project
