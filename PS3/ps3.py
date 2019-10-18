# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        
#       Represent tiles in dictionary {(integer pair), dirt_amount}
        self.tiles = {}
        for w in range(width):
            for h in range(height):
                self.tiles[(w, h)] = dirt_amount

        
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
#        Convert position to tile integer pair
        tile = (math.floor(pos.get_x()), math.floor(pos.get_y()))

#        If negative dirt value would results, update dirt value to 0        
        if self.tiles[tile] < capacity:
            self.tiles[tile] = 0

#        Reduce tile dirt amount by capacity (dirt can be added by robot if capacity is neg)            
        else:
            self.tiles[tile] -= capacity
        
        

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
#        check tile dictionary to see if tile is clean
        if self.tiles[(m, n)] == 0:
            return True
        
        else:
            return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        num_clean = 0
        
        for tile in self.tiles:
            if self.tiles[tile] == 0:
                num_clean += 1
                
        return num_clean
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
#       Convert position to tile integer pair
        tile = (math.floor(pos.get_x()), math.floor(pos.get_y()))
        
#       Return whether or not the tile exists in room
        return tile in self.tiles
    
##       Less code, but less readable
#        return (math.floor(pos.get_x()), math.floor(pos.get_y())) in self.tiles
        
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """

        return self.tiles[(m, n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        
        self.room = room
        self.speed = speed
        self.capacity = capacity
        
        self.position = room.get_random_position()
        self.direction = round(random.uniform(0, 360), 2)
        
        

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction
        
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    
    def __init__(self, width, height, dirt_amount):
#        Creates self.tiles dictionary as well
        RectangularRoom.__init__(self, width, height, dirt_amount)
    
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.tiles) #or width * height
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
#        Convert position to integer pair and check if its in tile dict
        return (math.floor(pos.get_x()), math.floor(pos.get_y())) in self.tiles
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
#        Return an pair of random coordinates within the room dimensions
        return Position(random.uniform(0, self.width), random.uniform(0, self.height))
        
         

class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        return (m, n) in self.furniture_tiles
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        return self.is_tile_furnished(math.floor(pos.get_x()), math.floor(pos.get_y()))
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
         
        tile = (math.floor(pos.get_x()), math.floor(pos.get_y()))

        if not tile in self.tiles:
            return False
        
        if tile in self.furniture_tiles:
            return False
        
#        Tile is in the room and not furnished, return True
        return True   
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        return len(self.tiles) - len(self.furniture_tiles)
        
    
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        while 0 != 1:
            
            pos = Position(random.uniform(0, self.width), random.uniform(0, self.height))
            
            if self.is_position_valid(pos):
                break
            
        return pos

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        
        destination = self.get_robot_position().get_new_position(self.direction, self.speed)
#        
##        If the destination is valid position in room:
        if self.room.is_position_valid(destination):
##        Update robot position to new destination
            self.set_robot_position(destination)                
#            
##            If new position isn't valid, update direction to new random angle (stay stationary)
        else:
            self.set_robot_direction(round(random.uniform(0, 360), 2))
#
##        Clean dirt on current tile by robot capacity
        self.room.clean_tile_at_position(self.get_robot_position(), self.capacity)

####################################
        ### OLD IMPLEMENTAION Forgot to stay stationary in this implementation
#        
##        Loop until find new valid position 
#        while 0 != 1:
#            
#            destination = self.get_robot_position().get_new_position(self.direction, self.speed)
#        
#            if self.room.is_position_valid(destination):
#                break
#            
##            If new position isn't valid, update direction to new random angle
#            else:
#                self.set_robot_direction(round(random.uniform(0, 360), 2))
#        
##        Update robot position to valid destination position
#        self.set_robot_position(destination)
#        
##        Clean dirt on new tile by robot capacity
#        self.room.clean_tile_at_position(destination, self.capacity)

# Uncomment this line to see your implementation of StandardRobot in action!
#test_robot_movement(StandardRobot, EmptyRoom)
#test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        
        if self.gets_faulty():
            self.set_robot_direction(round(random.uniform(0, 360), 2))
            
        else:
            StandardRobot.update_position_and_clean(self)
        
    
#test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
#   Initialize list to track means from each trial (which we will then return the mean of)
    trial_means = []

#   Loop through each trial
    for t in range(num_trials):
        
#        Initialize time step tracker
        t_steps = 0
        
#       Create new room for each trial        
        room = EmptyRoom(width, height, dirt_amount)
        
#       Create new fleet of robots for each room
        robots = []       
        for i in range(num_robots):
            robots.append(robot_type(room, speed, capacity))
   
#        While the fraction of clean tiles is less than the provided min coverage:
        while min_coverage > (room.get_num_cleaned_tiles()/room.get_num_tiles()):

#            New time step needed to complete simulation
            t_steps += 1
            
            for robot in robots:
                robot.update_position_and_clean()
        
        trial_means.append(t_steps)
        
    return pylab.mean(trial_means)

#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?

### TESTS
#print ('avg time steps for 1 standard robots cleaning 80% of a 20x20 empty room: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.80, 50, StandardRobot)))
#print ('avg time steps for 1 faulty robots cleaning 80% of a 20x20 empty room: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.80, 50, FaultyRobot)))
#print('')
#print ('avg time steps for 3 standard robots cleaning 80% of a 20x20 empty room: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.80, 50, StandardRobot)))
#print ('avg time steps for 3 faulty robots cleaning 80% of a 20x20 empty room: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.80, 50, FaultyRobot)))

#
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#
    
#print ('avg time steps for 2 standard robots cleaning 80% of a 10x30 empty room: ' + str(run_simulation(2, 1.0, 1, 10, 30, 3, 0.80, 50, StandardRobot)))
#print ('avg time steps for 2 faulty robots cleaning 80% of a 10x30 empty room: ' + str(run_simulation(2, 1.0, 1, 10, 30, 3, 0.80, 50, FaultyRobot)))
#print('')
#print ('avg time steps for 2 standard robots cleaning 80% of a 20x15 empty room: ' + str(run_simulation(2, 1.0, 1, 20, 15, 3, 0.80, 50, StandardRobot)))
#print ('avg time steps for 2 faulty robots cleaning 80% of a 20x15 empty room: ' + str(run_simulation(2, 1.0, 1, 20, 15, 3, 0.80, 50, FaultyRobot)))
#print('')
#print ('avg time steps for 2 standard robots cleaning 80% of a 25x12 empty room: ' + str(run_simulation(2, 1.0, 1, 25, 12, 3, 0.80, 50, StandardRobot)))
#print ('avg time steps for 2 faulty robots cleaning 80% of a 25x12 empty room: ' + str(run_simulation(2, 1.0, 1, 25, 12, 3, 0.80, 50, FaultyRobot)))
#print('')
#print ('avg time steps for 2 standard robots cleaning 80% of a 50x6 empty room: ' + str(run_simulation(2, 1.0, 1, 50, 6, 3, 0.80, 50, StandardRobot)))
#print ('avg time steps for 2 faulty robots cleaning 80% of a 50x6 empty room: ' + str(run_simulation(2, 1.0, 1, 50, 6, 3, 0.80, 50, FaultyRobot)))
#print('')

#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')



######################## AK, troubleshooting the plotting issue... 
### Issue resolved but have no idea why. I tried simple plots and was eventually able to plot
# a simple function for calculating investment growth and then the other plots all worked as well
# The given plotting functions aren't working...
#    --> Maybe I just wasn't waiting long enough
#    
#def plot_simulation(title, x_label, y_label):
#    num_robot_range = range(1, 5)
#    times1 = []
#    times2 = []
#    for num_robots in num_robot_range:
#        print ("Plotting", num_robots, "robots...")
#        times1.append(run_simulation(num_robots, 1.0, 1, 10, 10, 3, 0.8, 20, StandardRobot))
#        times2.append(run_simulation(num_robots, 1.0, 1, 10, 10, 3, 0.8, 20, FaultyRobot))
#    pylab.plot(num_robot_range, times1)
#    pylab.plot(num_robot_range, times2)
#    pylab.title(title)
#    pylab.legend(('StandardRobot', 'FaultyRobot'))
#    pylab.xlabel(x_label)
#    pylab.ylabel(y_label)
#    pylab.show()
#    
#    
#title = 'Robot type cleaning comparison'
#x_label = 'Number of robots'
#y_label = 'time / steps'
#
#
#def get_plot_data():
#    num_robot_range = range(1, 5)
#    times1 = []
#    times2 = []
#    for num_robots in num_robot_range:
#        times1.append(run_simulation(num_robots, 1.0, 1, 10, 10, 3, 0.8, 20, StandardRobot))
#        times2.append(run_simulation(num_robots, 1.0, 1, 10, 10, 3, 0.8, 20, FaultyRobot))
#    return [times1, times2]
#
#times1, times2 = get_plot_data()
#print(times1)
#print(times2)
#
##pylab.plot(range(1, len(times1) + 1), times1)
#
#
## Plot test
##pylab.figure(0)
##pylab.plot([1,2,3,4,5], [3,9,3,9,3])
##Now this works...
#
#
##HMMMM, this function from my worksheets works fine...
#
##def Calc_Growth(principal, growth_rate, compounding_rate, years):
##    '''
##    Returns total amount accrued over given years with given growth and 
##    compounding rates. Plots the growth.
##    
##    Assumes principal an int > 0, growth rate a float, compounding rate a float, 
##    and years an int > 0.
##    '''
##    amount = principal
##
##    amount_list = [principal]
##
##    for year in range(1, years + 1):
##        amount = amount * (1.0 + (growth_rate/compounding_rate))**compounding_rate
##        
##        amount_list.append(amount)
##    
###   Graphing    
##        
##    y_title = 'Total Amount'
##    x_title = 'Years'    
##    
##    pylab.figure(0)
##    pylab.plot(range(len(amount_list)), amount_list, 'ko')
##    pylab.title(str(growth_rate) + '% Growth Rate, Compounded ' + str(compounding_rate) + ' Times Annually')
##    pylab.semilogy()
##    
##    
##    pylab.figure(1)
##    pylab.plot(amount_list, 'o')
##    pylab.title(str(growth_rate) + '% Growth Rate, Compounded ' + str(compounding_rate) + ' Times Annually')
##       
##    
##    
##    
##    print('')
##    print('Principal =', principal)
##    print('Annual Growth Rate =', growth_rate)
##    print('Compounding Rate =', compounding_rate)
##    print('Years =', years)
##    
##    print('---> Final Amount: $' + str(round(amount_list[-1], 2)))
##    print('---> Total Growth % = ' + str(round(100 * amount/principal, 2)) + '%')
##    return amount
##
##
##principal = 10.0
##growth_rate = .15
##compounding_rate = 12.0
##years = 20
##
##Calc_Growth(principal, growth_rate, compounding_rate, years)
