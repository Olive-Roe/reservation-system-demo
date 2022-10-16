import turtle
import time
import random
from math import sqrt
import aim_protocol as ap
from display import *

COLORS = ["red", "blue", "green", "yellow", "cyan", "magenta"]





def main():
    # set up the background
    board()
    # set up reservations list
    ap.create_reservations_list(ap.GRANULARITY)

    def new_car(direction, colour, lane=1):
        if direction == 0:
            return ap.Car(-230, (10 + lane * 10), 10, 0, colour)
        elif direction == 90:
            return ap.Car(-(10 + lane * 10), -230, 10, 90, colour)
        elif direction == 180:
            return ap.Car(230, -(10 + lane * 10), 10, 180, colour)
        elif direction == 270:
            return ap.Car((10 + lane * 10), 230, 10, 270, colour)

    # c = ap.Car(-230, 20, 10, 0, "red")
    # c2 = ap.Car(25, 230, 10, 270, "blue")
    time_steps = 0
    while True:
        if time_steps % 10 == 0:
            c = new_car((time_steps // 10 * 90) % 360, random.choice(COLORS),
                        (time_steps // 5) % 3)
        sc.update()
        for car in ap.Car.carlist:
            car.move(time_steps)
        ap.draw_reservation_grid(sc)
        # time.sleep(1)
        time_steps += 1



if __name__ == "__main__":
    main()
    sc.exitonclick()
