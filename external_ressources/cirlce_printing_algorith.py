# Define the params for circle movement
from turtle import *
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import threading
T = 60  # seconds: the periode complete one rotation
F = 1/T  # Hz: how much rotation done in one second
r = 0.036  # m : the radius of the circle
m = 0.3  # Kg: mass of the object
omega = "_"  # rad/degree the angle of the object made to its start
time_ = "_"  # time in s
d = 2*math.pi*r  # distance of circle
v_t = d/T  # m/s: tangential velocity , distance the object omves around circle over time
# rad/s or degree/s Angular Velocity: the change in angle around a cirlce over the time
w_t = 2*math.pi*F
v_t = w_t*r
# m/s^2 : centripetal Acceleration: acceleration of the object, points to the centre of the circle
a_c = (v_t*v_t)/r
F_c = m*a_c  # N: centripetal Force: net force on the object: it points to center

R = 300  # radius
n = 200  # number of edge
z = 100

t = np.linspace(0, 2*np.pi, n+1)  # create array of 33 radians
x = R*np.cos(t)
y = R*np.sin(t)

def draw_circle_plot():
    plt.axis("equal")
    plt.grid()
    plt.plot(x,y)
    plt.show()

class Turtle_drawing:
    # Create a turtle at position (r,0):
    def __init__(self):
        self.a = Turtle()
    def draw_circle(self):
        self.a.hideturtle()  # make the turtle invisible
        self.a.penup()  # don't draw when turtle moves
        self.a.goto(R, 0)  # move the turtle to a location
        self.a.showturtle()  # make the turtle visible
        self.a.pendown()  # draw when the turtle moves
        for i in range(n):
            self.a.goto(x[i+1], y[i+1])

if __name__ == "__main__":
    t1 = threading.Thread()
    t1.run(draw_circle_plot())
    tur = Turtle_drawing()
    t2 = threading.Thread()
    t2.run(tur.draw_circle)