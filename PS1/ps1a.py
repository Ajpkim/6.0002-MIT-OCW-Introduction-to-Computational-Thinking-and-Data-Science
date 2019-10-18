###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: 
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

filename = 'ps1_cow_data.txt'



#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
#   Initialize empty dictionary that will have cow names as key and cow weights as values
    cows = {}    
    # Read file in using "context manager" (with) 
    with open(filename, 'r') as cow_data:
        #Loop through the lines
        for line in cow_data:
            #Remove the spaces and split the line into cow name info and weight info
            cow = line.replace(' ','').split(',')
            #Create new entry in cow dict for each line. Taking the cow name as key and weight as value
            cows[cow[0]] = int(cow[1])
    #Return the dictionary of cow data
    return cows
    
    
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """


#   Create cow list to use as a sorted list for greedy and to track cows that need to be transported        
    cow_List = []
    for cow in cows:
        cow_List.append([cow, cows[cow]])
    
    #Sort the cow list by weight of cows (can remove cows from list as they are transported)
    cow_List.sort(key = lambda x: x[1], reverse = True)

#    print ("sorted list:", cow_List)

    #Create empty list of trips
    trip_List = []
    
    #Begin loop to transport all the cows
    while len(cow_List) > 0:
#        Create a new trip
        trip = []
#       Initialize available weight which is given as function argument 
        avail = limit

        moving_cows = []

#       Loop through cows in sorted list (ensuring that heaviest possible are taken)
        for cow in cow_List:
#           If there is room for the cow on the trip
            if avail - cow[1] >= 0:
#               Add the cow to the current trip    
                trip.append(cow[0])
#               #Add cow to moving cow list which will be used to edit the cow_list OUTSIDE of the loop
                moving_cows.append(cow)
#                Update the available space on trip
                avail -= cow[1]
                
        for mc in moving_cows:
            cow_List.remove(mc)
                
                
#        print('Filled trip:', trip, 'Available space:', avail)
            
#       Add the current trip to the master trip list
        trip_List.append(trip)
        
#   Return a list of all the trip lists
    return trip_List

#Test of load and greedy:
#filename = 'ps1_cow_data.txt'
#cows = (load_cows(filename))
#print(greedy_cow_transport(cows, limit=10))


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
#    Need to get all the partitions and then select the partition with fewest trips that has no trips over the weight limit
    
#    Going to generate all the partitions and loop through them
#    Check each trip in partition to see if any are illegal
#    Store most efficient partition while looping
#    After loop finishes, return best partition
    
#    Create empty list to hold best partition during loop
    best_partition = []
    
#    Loop through all the partitions
    for p in get_partitions(cows):
#        Set a flag to track if all the trips in a partition stay within the weight limit
        legal = True
#        Loop through all the trips in the current partition
        for trip in p:
#            Set available weight to given limit
            avail = limit
#            For each cow in the trip
            for cow in (trip):
#                Reduce the available weight by the cow's weight
                avail -= cows[cow]
#            If the total weight on trip exceeds the limit
            if avail < 0:
                #Set legal flag to false... Trip is overweight!
                legal = False
#        If all the trips are within the weight limit
        if legal == True:
#           If the partition contains less trips than best partition so far, or best is empty
            if best_partition == [] or len(p) < len(best_partition):
#               Update best partition to current partition
                best_partition = p
#   Return a list that contains the fewest number of trips in which all the trips are within the weight limit    
    return best_partition


# Test brute force:
#print('')
#cows = load_cows(filename)
#print (brute_force_cow_transport(cows, limit = 10))



# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
  
    print ('Comparing greedy transport with brute force enumeration...')
    
    print ('Greedy transport:')
    #Load cows
    cows = load_cows(filename)
    
#    Start timer for greedy algo
    start = time.time()
    #Run greedy algo
    print('Number of trips:', len(greedy_cow_transport(cows)))    
#    Stop timer
    end = time.time()
    #Report speed of greedy
    print ('Speed of greedy transport:', end - start)

    print('')
    
    print('Brute force enumeration:')
    start = time.time()
    print('Number of trips:', len(brute_force_cow_transport(cows)))    
#    Stop timer
    end = time.time()
    #Report speed of greedy
    print ('Speed of brute force transport:', end - start)
    
    print('')
    print ('GG, AJPK')

# Running the comparison:
compare_cow_transport_algorithms()
    
