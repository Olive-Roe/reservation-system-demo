def set_cars():
    car1.penup()
    car1.setposition(-250, 20)
    car1.pendown()
    car2.penup()
    car2.left(90)
    car2.setposition(-20, -250)
    car2.pendown()
    car3.penup()
    car3.setposition(250, -20)
    car3.left(180)
    car3.pendown()
    car4.penup()
    car4.setposition(20, 250)
    car4.right(90)
    car4.pendown()


def set_cars_manually():
    "Unused function to set 4 cars' positions manually (userinput)"
    car1_x = int(
        input("Please enter an x coordiante for car 1 (range -250 to -40): "))
    car2_y = int(
        input("Please enter a y coordinate for car 2 (range -250 to -40): "))
    car3_x = int(
        input("Please enter an x coordinate for car 3 (range 40 to 250): "))
    car4_y = int(
        input("Please enter a y coordinate for car 4 (range 40 to 250): "))

    car1.penup()
    car1.setposition(car1_x, 20)
    car1.pendown()
    car2.penup()
    car2.setposition(-20, car2_y)
    car2.pendown()
    car3.penup()
    car3.setposition(car3_x, -20)
    car3.pendown()
    car4.penup()
    car4.setposition(20, car4_y)
    car4.pendown()


ID_TABLE = {"1": car1, "2": car2, "3": car3, "4": car4}


def set_car(id, x, y):
    "Set a single car with an id at (x, y)"
    car = ID_TABLE[id]
    car.penup()
    car.setpos(x, y)
    car.pendown()


def stamp_car(id, x, y):
    "Move a car to (x, y) and stamp (leave a copy of itself on the background)"
    car = ID_TABLE[id]
    car.penup()
    car.setpos(x, y)
    car.pendown()
    car.stamp()


def set_custom_cars(x1, y1, x2, y2, x3, y3, x4, y4):
    "Set four cars' positions by code"
    car1.penup()
    car1.setposition(x1, y1)
    car1.pendown()
    car2.penup()
    car2.setposition(x2, y2)
    car2.pendown()
    car3.penup()
    car3.setposition(x3, y3)
    car3.pendown()
    car4.penup()
    car4.setposition(x4, y4)
    car4.pendown()


# SERVER

DATA = {"1": [], "2": [], "3": [], "4": []}

TRAJECTORIES = {"1": [], "2": [], "3": [], "4": []}

# collision detection from starting values, not used in the end (instead trajectory formulas were tested)


def collision(dx, dy, vx, vy, ax, ay, b):
    "Takes position data and a buffer and returns True if there is a collision and False if there isn't"
    if ax == 0 and ay == 0:
        # cubic equation, minimum of dy/dx can be found
        t = (dx * vx + dy * vy) / (vx**2 + vy**2)
        if sqrt(dx**2 + dx**2 + 2 * (dx * vx + dy * vy) * t +
                (2 * (dx * ax + dy * ay) + dx**2 + vy**2) * t**2 + 2 *
                (vx * ax + vy * ay) * t**3 + (ax**2 + ay**2) * t**4) < b:
            # collides
            return True
        # does not collide
        return False
    for t in range(100):
        t = t / 10
        if sqrt(dx**2 + dx**2 + 2 * (dx * vx + dy * vy) * t +
                (2 * (dx * ax + dy * ay) + dx**2 + vy**2) * t**2 + 2 *
                (vx * ax + vy * ay) * t**3 + (ax**2 + ay**2) * t**4) < b:
            # a collision detected
            return True
    # no collisions detected
    return False


def add_data(car_number, displacement, time):
    "Add data to global variable, where car number is '1' to '4', displacement is a tuple of x and y floats, and time is a float"
    DATA[car_number].append((displacement[0], displacement[1], time))


def get_initial_values(data):
    "Takes a list of displacements and times, then returns the initial displacement, velocity, and acceleration"
    dxlist = [point[0] for point in data]
    dylist = [point[1] for point in data]
    timelist = [point[2] for point in data]
    d = (dxlist[0], dylist[0])
    v = ((dxlist[1] - dxlist[0]) / (timelist[1] - timelist[0]),
         (dylist[1] - dylist[0]) / (timelist[1] - timelist[0]))
    v2 = ((dxlist[2] - dxlist[1]) / (timelist[2] - timelist[1]),
          (dylist[2] - dylist[1]) / (timelist[2] - timelist[1]))
    a = ((v2[0] - v[0]) / (timelist[2] - timelist[1]),
         (v2[1] - v[1]) / (timelist[2] - timelist[1]))
    return d, v, a


def get_trajectory(d, v, a):
    "Given tuples of initial displacement, velocity, and acceleration, return a lambda function for the displacement of the car given time (assuming constant acceleration)"
    return lambda t: (d[0] + v[0] * t + a[0] * t**2, d[1] + v[1] * t + a[1] * t
                      **2)


def _distance(x1, y1, x2, y2):
    "Given two coordinates (or vectors) calculate the distance between them and return it"
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def _inbounds(coord):
    "Checks if a coordinate is within the boundaries of the model"
    return (coord >= -240 and coord <= 240)


def _inbounds_from_list(coordlist):
    "Takes a list of coordinates and returns False if any of them are out of bounds"
    for coord in coordlist:
        if not (_inbounds(coord)):
            return False
    return True


def collision_from_trajectory(f, g, b, step=0.05):
    "Given two displacement functions for the cars, return True if they will come within b units"
    time = 0
    while True:
        time += step
        c1 = f(time)
        c2 = g(time)
        if not (_inbounds_from_list([c1[0], c1[1], c2[0], c2[1]])):
            # out of bounds, break loop
            break
        dist = _distance(c1[0], c1[1], c2[0], c2[1])
        if dist < b:
            return True
    return False


def min_dist(f, g, step=0.05):
    "Given two displacement functions for the cars, return the smallest distance"
    time = 0
    small = float("inf")
    while True:
        time += step
        c1 = f(time)
        c2 = g(time)
        if not (_inbounds_from_list([c1[0], c1[1], c2[0], c2[1]])):
            # out of bounds, break loop
            break
        dist = _distance(c1[0], c1[1], c2[0], c2[1])
        small = min(small, dist)
    return small


def draw_trajectory(id, f, step=0.1):
    "Given the id of a car and its displacement function, draws its trajectory by stamping at fixed intervals"
    time = 0
    while True:
        time += step
        d = f(time)
        if not (_inbounds_from_list([d[0], d[1]])):
            # out of bounds
            break
        stamp_car(id, d[0], d[1])


def draw_trajectories(ids, functions, step=0.1):
    "Draws trajectories from a lists of ids and displacement functions"
    time = 0
    running = True
    while running:
        for index, num in enumerate(ids):
            time += step
            d = functions[index](time)
            if not (_inbounds_from_list([d[0], d[1]])):
                # out of bounds
                running = False
            stamp_car(num, d[0], d[1])


def draw(number):
    "Draws the trajectory of a car given its unique car id (number) and measurements, calculating its trajectory"
    d, v, a = get_initial_values(DATA[number])
    f = get_trajectory(d, v, a)
    draw_trajectory(number, f)


def draw_multiple(numbers):
    "Draws the trajectories of multiple cars given measurements (data points)"
    functions = []
    for num in numbers:
        d, v, a = get_initial_values(DATA[num])
        functions.append(get_trajectory(d, v, a))
    print(collision_from_trajectory(functions[0], functions[1], 10))
    print(min_dist(functions[0], functions[1]))
    draw_trajectories(numbers, functions, 0.05)


def _divide_without_zde(a, b):
    "An internal function to divide a/b, but if b=0, it will return 0 (used for the braking deceleration function)"
    try:
        return a / b
    except ZeroDivisionError:
        return 0


def getvals_for_stop(v, d):
    'Given current velocity and distance to braking point, find the deceleration and return initial values'
    # using v^2 = v0^2+2ax where v-final velocity, v0-initial velocity, a-constant acceleration, x-change in distacne
    a = (_divide_without_zde(
        (-v[0]**2), (4 * d[0])), _divide_without_zde((-v[1]**2), (4 * d[1])))
    # safe division which ignores 0 to account for zero division error
    # finds the acceleration and returns it
    return a


def check_all_trajectories(traj):
    "Takes a trajectory, returns True if path works, 'stop' if there is a collision"
    for i in TRAJECTORIES:
        if TRAJECTORIES[i] != traj and TRAJECTORIES[
                i] != [] and collision_from_trajectory(traj, TRAJECTORIES[i],
                                                       10):
            return "stop"
    return True


def check_all_collisions(car_number):
    "Takes an id, returns True if path (from trajectories dict) works, 'stop' if there is a collision"
    f = TRAJECTORIES[car_number]
    for i in CARS:
        if i != car_number and TRAJECTORIES[
                i] != [] and collision_from_trajectory(f, TRAJECTORIES[i], 10):
            DATA[car_number] = []  # reset data as trajectory changes
            # find values and tell car to slow down (stop by intersection)
            return "stop"
    return True


def add_data_and_check(car_number, displacement, time):
    "Add data point, return False if not enough data, True if path works, 'stop' if there is a collision"
    DATA[car_number].append((displacement[0], displacement[1], time))
    if len(DATA[car_number]) != 3:
        return False
    # can determine trajectory
    d, v, a = get_initial_values(DATA[car_number])
    f = get_trajectory(d, v, a)
    TRAJECTORIES[car_number] = f
    return check_all_collisions(car_number)


def remove_trajectory(name):
    "If car is out of bounds (successful intersection), remove its trajectory data from global dicts"
    del (TRAJECTORIES[name])
    del (DATA[name])
    del (CARS[name])


def closest_braking(disp):
    "Given a displacement, calculate the nearest distance to the closest braking point"
    x, y = disp
    closest = float("inf")
    # braking points (at the beginning of intersections) are (-40, 20), (40, 20), (20, 40), (-20, -40)
    for tup in [(-40, 20), (40, 20), (20, 40), (-20, -40)]:
        x1, y1 = tup
        d = _distance(x, y, x1, y1)
        if d < closest:
            closest = d
            output = (x1 - x, y1 - y)
    return output


CARS = {}
CHECK_POINTS = [(-230, 20), (-220, 20), (-210, 20), (230, -20), (-230, -20),
                (230, 20), (220, -20), (-220, -20), (220, 20), (210, -20),
                (-210, -20), (210, 20)]
BRAKE_POINTS = [(-100, 20), (100, -20), (-100, -20), (100, 20)]


def _invert(coord):
    "An internal function to return the four rotations of a coordinate around the intersection (for all 4 cars)"
    return [(coord[0] * -1, coord[1] * -1), (coord[0], coord[1] * -1),
            (coord[0] * -1, coord[1])]


def _mult(vector, multiplicant):
    "Multiplies a vector by something and returns it"
    return (vector[0] * multiplicant, vector[1] * multiplicant)


def get_bezier_func(p0, p1, p2, p3):
    # cubic bezier curve from 0 <= t <= 1
    return lambda t: _mult(p0,
                           (1 - t)**3) + _mult(p1, 3 * t * (1 - t)**2) + _mult(
                               p2, 3 * (1 - t) * t**2) + _mult(p3, t**3)


class Car:

    def __init__(self, name, direction, d, v, a, color="red", delay=0):
        # d, v, a refer to initial displacement, velocity, and acceleration
        self.turtle = turtle.Turtle()
        self.turtle.color(color)
        self.turtle.speed(0)
        self.turtle.setheading(direction)
        self.direction = direction
        self.turtle.penup()
        self.turtle.goto(d)
        # 0 right, 90 up, 180 left, 270 down
        self.name = name
        CARS[name] = self
        DATA[name] = []
        TRAJECTORIES[name] = []
        self.x, self.y = d
        self.d = d
        self.v = v
        self.current_v = v
        self.a = a
        self.braking = False
        # True for positive, True for negative
        self.delay = delay
        self.stopping = False
        self.update_trajectory()
        self.check(0)
        self.last_check_time = time.time()

    def display_trajectory(self):
        draw_trajectory(self.name, self.traj)

    def update_trajectory(self):
        traj = get_trajectory(self.d, self.v, self.a)
        self.traj = traj
        DATA[self.name] = []
        TRAJECTORIES[self.name] = self.traj

    def check(self, t):
        TRAJECTORIES[self.name]
        t -= self.delay
        self.current_v = (self.v[0] + self.a[0] * t, self.v[1] + self.a[1] * t)
        traj = get_trajectory((self.x, self.y), self.current_v, self.a)
        if check_all_trajectories(traj) == "stop":
            TRAJECTORIES[self.name] = []
            if not (self.braking):
                self.brake(t)
            self.last_check_time = time.time()
            self.stopping = True
        elif self.stopping:
            self.accelerate(t)
            self.stopping = False

    def measure(self, t):
        result = add_data_and_check(self.name, (self.x, self.y), time.time())
        if result == "stop":
            # there is a collision path, follow braking trajectory
            self.brake(t)

    def coast(self, t):
        self.a = (0, 0)
        self.v = self.current_v  # set initial speed to current speed
        self.d = (self.x, self.y)  # set initial disp to current disp
        self.update_trajectory()
        self.braking = True
        self.delay += t
        # set a new trajectory, time is now 0

    def brake(self, t):
        a = getvals_for_stop(self.current_v, closest_braking((self.x, self.y)))
        self.a = a
        self.v = self.current_v  # set initial speed to current speed
        self.d = (self.x, self.y)  # set initial disp to current disp
        self.update_trajectory()
        self.braking = True
        self.delay += t
        # set a new trajectory, time is now 0

    def accelerate(self, t, amount):
        self.braking = False
        self.d = (self.x, self.y)
        # t -= self.delay
        self.current_v = (self.v[0] + self.a[0] * t, self.v[1] + self.a[1] * t)
        # self.v = (0, 0)
        self.v = self.current_v
        if self.direction == 0:
            self.a = (amount, 0)
        elif self.direction == 90:
            self.a = (0, amount)
        elif self.direction == 180:
            self.a = (-1 * amount, 0)
        elif self.direction == 270:
            self.a = (0, -1 * amount)
        self.update_trajectory()
        self.delay = t

    def goto(self, t):
        t -= self.delay
        # for multiple trajectories, time of new trajectory is the delay
        if self.braking:
            x1, y1 = closest_braking((self.x, self.y))
            if _distance(x1, y1, self.x, self.y) < 50:
                self.d = (self.x, self.y)
                self.v = (0, 0)
                self.a = (0, 0)
                self.delay += t
                self.update_trajectory()
                self.braking = False
        x, y = self.traj(t)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.x = x
        self.y = y
        self.current_v = (self.v[0] + self.a[0] * t, self.v[1] + self.a[1] * t)
        if self.direction == 0:
            if len(DATA[self.name]) < 3:
                # access the x cooordinate of last measurement
                if DATA[self.name] == []:
                    self.measure(t)
                elif self.x > DATA[self.name][-1][0] + 10:
                    self.measure(t)
            if TL_ON:
                if LIGHTS == "ud" and self.x > -150:
                    self.brake(t)
                    self.stopping = True
                if LIGHTS == "lr" and self.stopping:
                    self.accelerate(t)
                    self.stopping = False
            else:  # traffic lights are not being used
                if self.stopping and (time.time() - self.last_check_time) > 1:
                    self.check(t)
                    self.stopping = False


def run_cars(start=0, stop=10, step=0.05):
    "Simulate several cars simultaneously for a set period of simulation time"
    t = start
    while t < stop:
        for car_id in CARS:
            car = CARS[car_id]
            car.goto(t)
            if TL_ON:
                update_lights()
        t += step


def generate_random_car(name):
    # def __init__(self, name, direction, d, v, a, color="red"):
    # 0 right, 90 up, 180 left, 270 down
    l = [(0, (-230, 20), (10, 0), (10, 0)),
         (90, (-20, -230), (0, 10), (0, 10)),
         (180, (230, -20), (-10, 0), (-10, 0)),
         (270, (20, 230), (0, -10), (0, -10))]
    direction, d, v, a = random.choice(l)
    b = Car(name, direction, d, v, a, random.choice(COLORS))


def generate_random_cars_left():
    for n in range(5):
        Car(str(n + 5), 0, (-230 - n * 20, 20), (10, 0), (10, 0),
            random.choice(COLORS))
    run_cars()


# TRAFFIC LIGHT CODE

TL_ON = True
LIGHTS = "lr"


def setup_tl():
    global START_TIME, light1, light2, light3, light4
    START_TIME = time.time()
    light1 = turtle.Turtle()
    light2 = turtle.Turtle()
    light3 = turtle.Turtle()
    light4 = turtle.Turtle()
    light1.hideturtle()
    light2.hideturtle()
    light3.hideturtle()
    light4.hideturtle()
    light1.penup()
    light2.penup()
    light3.penup()
    light4.penup()
    light1.goto(-40, 0)
    light2.goto(0, 40)
    light3.goto(40, 0)
    light4.goto(0, -40)
    light1.shape("circle")
    light2.shape("circle")
    light3.shape("circle")
    light4.shape("circle")
    light1.turtlesize(0.5)
    light2.turtlesize(0.5)
    light3.turtlesize(0.5)
    light4.turtlesize(0.5)


def leftright():
    global LIGHTS
    light1.color("green")
    light2.color("red")
    light3.color("green")
    light4.color("red")
    LIGHTS = "lr"


def updown():
    global LIGHTS
    light1.color("red")
    light2.color("green")
    light3.color("red")
    light4.color("green")
    LIGHTS = "ud"


def update_lights(delay=5):
    "Graphically updates the traffic lights depending on the delay (s)"
    now = time.time()
    if (now - START_TIME) % (delay * 2) >= delay and LIGHTS == "lr":
        updown()
    elif (now - START_TIME) % (delay * 2) < delay and LIGHTS == "ud":
        leftright()

def main():

    # traj = get_trajectory((-40, 20), (10, 0), (-1, -3))
    # draw_trajectory("1", traj)

    # draw_trajectory("1", get_bezier_func(
    #     (-230, 20), (-220, 20), (-200, 0), (-200, -10)))
    # turtle.exitonclick()
    'testing responsiveness to future collisions'
    # if TL_ON:
    #     setup_tl()
    # c1 = Car("5", 0, (-230, 20), (19, 0), (10, 0), "magenta")
    # c2 = Car("6", 270, (20, 230), (0, -10), (0, -10), "red")
    # run_cars(stop=20)
    # turtle.exitonclick()
    'testing multiple cars in different lanes (distance between cars is incomplete)'
    # for n in range(5):
    #     generate_random_car(str(n+5))
    # run_cars()
    'testing multiple cars on one lane (collisions between cars on the same lane happen)'
    # if TL_ON:
    #     setup_tl()
    # generate_random_cars_left()