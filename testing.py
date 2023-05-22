import turtle

screen = turtle.Screen()
turtle.color("Red")
turtle.title("Test")
turtle.pensize(5)


def tLeft():         #Edit everything later, most likely to be inaccurate.
    turtle.right(180)
    turtle.forward(10)

def tRight():
    turtle.left(180)
    turtle.forward(10)

def tUp():
    turtle.right(90)
    turtle.forward(10)

def tDown():
    turtle.left(270)
    turtle.forward(10)

turtle.onkeypress(tUp, "Up")
turtle.onkeypress(tDown, "Down")
turtle.onkeypress(tRight, "Right")
turtle.onkeypress(tLeft, "Left")    #First test: When started the code did nothing, nothing showed up and no errors was shown. Edit:only needed "listen()"
turtle.listen()

screen.mainloop()