
# Initial study
# https://www.cs.utexas.edu/~aim/papers/AAMAS04-kurt.pdf


from copy import copy
from math import cos, sin, radians
from turtle import Turtle

# number of pixels of the intersection space
GRID_SIZE = 80
# the 'resolution' of the grid used for the intersection space
GRANULARITY = 8
# an array representing an n by n grid and the reservations associated with each tile
RESERVATIONS = []


def create_reservations_list(granularity: int):
    global RESERVATIONS
    # create a 3D array representing an n by n grid (granularity = n)
    RESERVATIONS = [[[] for i in range(granularity)]
                    for j in range(granularity)]


def check_reservation_collision(x_index, y_index, start, end):
    "Returns True if there is a collision between an existing reservation and the one being requested"
    if RESERVATIONS[x_index][y_index] == []:
        # no reservations yet
        return False
    for reservation in RESERVATIONS[x_index][y_index]:
        # [color, start_time, end_time, car_id]
        # if reservation[0] == "white":
            # this reservation is a placeholder
            # continue
        r_start = reservation[1]
        r_end = reservation[2]
        # only works if the requested reservation is completely outside the existing one
        if end > r_start and start < r_end:
            return True
    # no collisions at all
    return False


def add_reservation(x_index, y_index, start_time, end_time, colour="green", car_index=0):
    "Adds a reservation to the global RESERVATIONS list, and returns True if there is a collision, or the index of the new reservation"
    global RESERVATIONS
    if check_reservation_collision(x_index, y_index, start_time, end_time):
        return True
    RESERVATIONS[x_index][y_index].append(
        [colour, start_time, end_time, car_index])
    return len(RESERVATIONS[x_index][y_index]) - 1


def check_trajectory(trajectory, starting_time, colour="green", car_index=0):
    """Checks if a trajectory can have valid reservations and reserves them if possible.\n
    Returns False if there is already existing reservations, or a list of the visited tiles"""
    # trajectory is a lambda function that takes time as an input and returns (xpos, ypos)
# starting_time is the time the car spawns, this accounts for each car
    time = starting_time
    x, y = trajectory(time)
    x_coord, y_coord = get_indices_from_coord(x, y)
    visited_tiles = []
    # makes a copy to revert to if there is a collision
    reservations_copy = copy(RESERVATIONS)

    def reset_changes():
        global RESERVATIONS
        RESERVATIONS = reservations_copy
        return False

    # initial loop before the car enters the intersection space
    while x_coord not in range(GRANULARITY) or y_coord not in range(GRANULARITY):
        time += 0.5  # this is arbitrary
        # TODO: if amount time is increased by is too high, it might skip a square and not reserve it
        # idea: function to check if tiles are adjacent (in four directions), then check with progressively larger distances unless it skips a tile
        x, y = trajectory(time)
        x_coord, y_coord = get_indices_from_coord(x, y)
        if x < -240 or x > 240 or y < -240 or y > 240:
            raise ValueError(
                f"car {car_index} with color {Car.carlist[car_index].colour} never entered the intersection")
    # add starting reservation to the list
    # x_coord and y_coord are the coordinates of the first square
    last_time = time
    # add to 'memory'
    visited_tiles.append((x_coord, y_coord))

    # while in intersection
    while x_coord in range(GRANULARITY) and y_coord in range(GRANULARITY):
        # every time the car reaches a new tile
        if (x_coord, y_coord) not in visited_tiles:
            # add a reservation to the previous visited tile
            prev_x, prev_y = visited_tiles[-1]
            collision = add_reservation(
                prev_x, prev_y, last_time, time, colour, car_index)
            if type(collision) == int:
                # add the index of the reservation
                visited_tiles[-1] = (prev_x, prev_y)
            else:
                # there is a collision
                reset_changes()
            # find the time that the car enters the next tile
            last_time = time
            # add to the memory
            x, y = trajectory(time)
            x_coord, y_coord = get_indices_from_coord(x, y)
            visited_tiles.append((x_coord, y_coord))
        time += 0.5
        x, y = trajectory(time)
        x_coord, y_coord = get_indices_from_coord(x, y)

    # finish by adding the ending reservation for the final tile
    prev_x, prev_y = visited_tiles[-1]
    collision = add_reservation(
        prev_x, prev_y, last_time, time, colour, car_index)
    if type(collision) == int:
        # add the index of the reservation
        visited_tiles[-1] = (prev_x, prev_y)
    else:
        # there is a collision
        reset_changes()

    # return the visited tiles, to clear after the car has exited
    return visited_tiles


def clear_reservations(visited_tiles, car_index):
    global RESERVATIONS
    # TODO: O(n^2) time complexity, can it be more efficient?
    # (will slow down with many cars)
    for x, y in visited_tiles:
        for i, r in enumerate(RESERVATIONS[x][y]):
            # check each reservation to see if it matches the car
            if r[3] == car_index:
                RESERVATIONS[x][y].pop(i)


def get_indices_from_coord(x, y):
    # find x and y relative to the bottom-left corner of the intersection space, return the index of the reservation list
    # e.g. grid size = 80, x = -30, y = -40 becomes x = 10, y = 0
    x -= GRID_SIZE/2
    y -= GRID_SIZE/2
    # finds the size of one box
    box_size = 80/GRANULARITY
    # finds the x and y index
    return int(x//box_size+8), int(y//box_size+8)


# def clear_reservations(visited_tiles):
#     for x, y in visited_tiles:
#         RESERVATIONS[x][y] = ["white", 0, 0]


def draw_reservation_grid(screen):
    t = Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()

    def draw_square(size, colour):
        t.pendown()
        t.fillcolor(colour)
        t.begin_fill()
        for _ in range(4):
            t.forward(size)
            t.right(90)
        t.end_fill()
        t.penup()

    granularity = GRANULARITY
    t.goto(-40, -30)
    t.setheading(0)
    for y in range(granularity):
        for x in range(granularity):
            if RESERVATIONS[x][y] == []:
                colour = "white"
            else:
                colour = RESERVATIONS[x][y][0][0]
            draw_square(80//granularity, colour)
            t.goto(t.xcor()+80//granularity, t.ycor())
        t.goto(-40, t.ycor()+80//granularity)
    screen.update()


def _in_intersection(x, y):
    "Returns whether the car is in the intersection"
    x_coord, y_coord = get_indices_from_coord(x, y)
    return x_coord in range(GRANULARITY) and y_coord in range(GRANULARITY)


LIGHTCOLORS = ["yellow", "cyan", "magenta"]


class Car:
    carlist = []

    def __init__(self, xpos, ypos, velocity, direction, colour="black", delay=0):
        'Direction is in degrees'
        self.id = len(self.carlist)
        self.carlist.append(self)
        self.xpos = xpos
        self.ypos = ypos
        self.velocity = velocity
        # convert direction (deg) to rad
        self.direction = radians(direction)
        # for 'delay' timesteps, the car will be frozen and invisible
        self.delay = delay
        # set up turtle to mark car's position
        self.t = Turtle()
        # self.t.hideturtle()
        self.colour = colour
        if colour in LIGHTCOLORS:
            # set inside of turtle to black for contrast
            self.t.color(colour, "black")
        else:
            self.t.color(colour, "white")
        self.t.penup()
        self.t.seth(direction)
        self.t.goto(xpos, ypos)
        self.entered_intersection = False
        self.visited_tiles = []
        self.path_available = False

    def display(self, time):
        traj = self.get_trajectory()
        x, y = traj(time)
        self.t.goto(x, y)
        # self.t.goto(self.xpos, self.ypos)

    def stop(self):
        self.velocity = 0

    def get_trajectory(self, start_time=0):
        "Returns a lambda function that returns a tuple (xpos, ypos) for t timesteps in the future"
        vx, vy = self.velocity * \
            cos(self.direction), self.velocity*sin(self.direction)
        return lambda t: (self.xpos + vx*(t-start_time), self.ypos + vy*(t-start_time))

    def move(self, time: float):
        if time < self.delay:
            pass  # TODO
        vx, vy = self.velocity * \
            cos(self.direction), self.velocity*sin(self.direction)
        self.xpos += vx
        self.ypos += vy
        self.t.goto(self.xpos, self.ypos)

        # check if path is available
        if self.path_available == False:
            flag = check_trajectory(
                self.get_trajectory(time), time, self.colour, self.id)
            if flag == False:
                # reservation is booked
                self.velocity -= 1
            else:
                # reservation is available, save the visited tiles
                self.visited_tiles = flag
                self.path_available = True

        # check if we have left the intersection or entered it
        if not self.entered_intersection and _in_intersection(self.xpos, self.ypos):
            # enters intersection for the first time
            self.entered_intersection = True
        elif self.entered_intersection and not _in_intersection(self.xpos, self.ypos):
            # just left the intersection space
            clear_reservations(self.visited_tiles, self.id)
            self.entered_intersection = False


if __name__ == "__init__":
    pass
