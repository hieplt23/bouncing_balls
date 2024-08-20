<div align="center">
    <h1>Bouncing Ball Simulation 🎱</h1>
</div>

## 📚 Table of Contents
- [Introduction](#-introduction)
- [Acknowledgments](#-acknowledgments)
- [Physics Concepts](#-physics-concepts)
  - [Gravity](#gravity)
  - [Circular Motion](#circular-motion)
  - [Collision Detection](#collision-detection)
  - [Reflection](#reflection)
- [Mathematical Formulas](#-mathematical-formulas)
  - [Ball Position](#ball-position)
  - [Velocity Update](#velocity-update)
  - [Collision with Arc](#collision-with-arc)
- [Implementation Details](#-implementation-details)
- [Visualization](#-visualization)
- [Future Improvements](#-future-improvements)

## 🎮 Introduction

This project simulates the motion of balls bouncing within a circular boundary with a rotating arc. The simulation incorporates various physics concepts and mathematical formulas to create realistic ball movements and collisions.

## 👏 Acknowledgments

This project is inspired by [Dung Lai Lap Trinh](https://www.youtube.com/watch?v=sgQJWAuc_kM) - YouTube channel
## 🧠 Physics Concepts

### Gravity

Gravity is simulated by constantly updating the vertical component of the ball's velocity:

```python
ball.v[1] += GRAVITY
```
### Circular Motion
The arc rotates around the circle's center at a constant angular velocity:
```python
start_angle += SPINNING_SPEED
end_angle += SPINNING_SPEED
```
### Collision Detection
Collisions are detected by comparing the distance between the ball and the circle's center to the circle's radius:
```python
dist = np.linalg.norm(ball.pos - circle_center)
if dist + BALL_RADIUS > CIRCLE_RADIUS:
    # Collision occurred
```
### Reflection
When a collision occurs, the ball's velocity is reflected based on the tangent line at the point of collision.

## 📐 Mathematical Formulas
### Ball Position
The ball's position is updated using the equation of motion:
```
new_position = old_position + velocity * time_step
```

### Velocity Update
After a collision, the new velocity is calculated using the reflection formula:
```
v_new = 2(v • t)t - v
```
Where:
* v is the incoming velocity
* t is the unit tangent vector at the point of collision

### Collision with Arc
To determine if a ball is within the arc, we use the atan2 function and compare angles:
```python
ball_angle = math.atan2(dy, dx)
is_in_arc = start_angle <= ball_angle <= end_angle
```
## 💻 Implementation Details
The simulation is implemented in Python using the Pygame library for visualization. Key components include:

* `Ball class`: Represents a ball with position, velocity, and color.
* `draw_arc`: Function to draw the rotating arc.
* `is_ball_in_arc`: Function to check if a ball is within the arc.
* `handle_collision`: Function to update ball velocity after a collision.
## 👁 Visualization
<p align="center">
  <img src="images/demo.gif" width="900">
  <em>Demo</em>
</p>

## 🚀 Future Improvements

* Add user interaction to control arc rotation speed.
* Implement ball-to-ball collisions.
* Add power-ups or obstacles within the circle.
* Create different levels with varying difficulty.
