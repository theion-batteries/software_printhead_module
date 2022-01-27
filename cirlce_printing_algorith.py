# Define the params for circle movement
from turtle import *
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import threading
class Variables:
    T = 60  # seconds: the periode complete one rotation
    F = 1/T  # Hz: how much rotation done in one second
    R = 36  # Radius of outer circle
    m = 0.3  # Kg: mass of the object
    omega = "_"  # rad/degree the angle of the object made to its start
    time_ = "_"  # time in s
    d = 2*math.pi*R  # distance of circle
    v_t = d/T  # m/s: tangential velocity , distance the object omves around circle over time
    # rad/s or degree/s Angular Velocity: the change in angle around a cirlce over the time
    w_t = 2*math.pi*F
    v_t = w_t*R
    # m/s^2 : centripetal Acceleration: acceleration of the object, points to the centre of the circle
    a_c = (v_t*v_t)/R
    F_c = m*a_c  # N: centripetal Force: net force on the object: it points to center
    PrintHead_lenght = 72 # mm
    all_radius = []
    n = 360  # number of edge 360
    z = 100
    num_Nozzles = 200 # number of nozzzles in row (1 column for simplicity)
    r = 0 # start radius by zero
    t = np.linspace(0, 2*np.pi, n+1)  # time or angles in degree
    d_x = R/num_Nozzles

    def generate_radien_list(self):
        for i in range(self.num_Nozzles):
            self.r = self.r + self.d_x
            print(self.r)
            self.all_radius.append(self.r)
        return self.all_radius
class Circle:
    def __init__(self, radius, listOfAlpha):
        self.radius = radius
        self.listOfAlpha = listOfAlpha
        self.ListOfVar = Variables()
        self.x = []
        self.y = []
        #self.xy = []

    def generate_circle(self):
        for angle in self.listOfAlpha:
            self.x.append(self.radius*np.cos(angle))
            self.y.append(self.radius*np.sin(angle))
        return self.x,self.y


    def draw_circle_plot(self):
        plt.axis([0, self.ListOfVar.R, 0, self.ListOfVar.R])
        plt.axis("equal")
        c=plt.Circle((self.x, self.y), radius=self.radius)
        plt.gca().add_artist(c)
        plt.show()
    def draw_concentric_cirlces(self):
        self.radien = self.ListOfVar.fill_radius()
        for radius in radien:
            pass
class Turtle_drawing:
    # Create a turtle at position (r,0):
    def __init__(self, start_pos):
        self.a = Turtle()
        self.v = Variables()
        self.a.hideturtle()  # make the turtle invisible
        self.a.penup()  # don't draw when turtle moves
        self.a.goto(start_pos, 0)  # move the turtle to a location
        self.a.showturtle()  # make the turtle visible
        self.a.pendown()  # draw when the turtle moves

    def draw_Circle(self, x, y):
        self.a.goto(x, y)
    def exitOnClick(self):
        self.a.exitonclick()
if __name__ == "__main__":

    Vars = Variables()
    radien = Vars.generate_radien_list()
    factor = 50
    import turtle
    turtle.delay(0) 
    turtles = [turtle.Turtle() for i in range(50)]
    #tir = Turtle()
    #tir.speed(0)
    circles_objects = []
    for i,j in enumerate(turtles):
        cir = Circle(radien[i]*factor, Vars.t)
        cir.generate_circle()
        circles_objects.append(cir)

        #j.hideturtle()  # make the turtle invisible
        #tir.penup()  # don't draw when turtle moves
    list_Cir = circles_objects
    for k in range(360):
        for i,j in enumerate(turtles):
            j.goto(list_Cir[i].x[k], list_Cir[i].y[k])  # move the turtle to a location
            j.showturtle()  # make the turtle visible
            #tir.pendown()  # draw when the turtle moves
 
