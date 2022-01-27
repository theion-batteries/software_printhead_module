import turtle
turtle.delay(0)

t = [turtle.Turtle() for i in range(8)]

for i, j in enumerate(t):
    j.right(i*45)
    j.speed(0)

for i in range(360):
    for j in t:
        j.forward(1)
        j.right(1)