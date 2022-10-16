import turtle

# CREATING DISPLAY

sc = turtle.Screen()
sc.tracer(0)
turtle1 = turtle.Turtle()
car1 = turtle.Turtle()
car2 = turtle.Turtle()
car3 = turtle.Turtle()
car4 = turtle.Turtle()
car1.color("red")
car2.color("blue")
car3.color("orange")
car4.color("magenta")
turtle1.hideturtle()
car1.hideturtle()
car2.hideturtle()
car3.hideturtle()
car4.hideturtle()


def board():
    "Set up the graphical display (background)"
    turtle1.speed(0)
    turtle1.penup()
    turtle1.setposition(-40, -250)
    turtle1.pendown()

    def lane():
        turtle1.left(90)
        turtle1.forward(190)
        turtle1.circle(20, 90)
        turtle1.forward(190)
        turtle1.right(90)

    for i in range(4):
        lane()
        turtle1.penup()
        turtle1.forward(80)
        turtle1.right(180)
        turtle1.pendown()

    turtle1.penup()
    turtle1.setposition(0, -250)
    turtle1.pendown()

    def d():
        turtle1.left(90)
        turtle1.forward(210)

    for i in range(4):
        d()
        turtle1.penup()
        turtle1.forward(40)
        turtle1.left(90)
        turtle1.forward(250)
        turtle1.pendown()
        turtle1.right(270)

    turtle1.penup()
    turtle1.setposition(0, -250)
    turtle1.pendown()

    def grass():
        turtle1.penup()
        turtle1.backward(40)
        turtle1.left(90)
        turtle1.pendown()
        turtle1.color("green")
        turtle1.begin_fill()
        turtle1.forward(190)
        turtle1.circle(20, 90)
        turtle1.forward(190)
        turtle1.left(90)
        turtle1.forward(210)
        turtle1.left(90)
        turtle1.forward(210)
        turtle1.end_fill()

    for i in range(4):
        grass()
        turtle1.penup()
        turtle1.left(90)
        turtle1.forward(250)
        turtle1.left(90)
        turtle1.forward(210)
        turtle1.left(90)
        turtle1.pendown()
    turtle1.color("black")
    turtle1.hideturtle()
    turtle1.speed(1)