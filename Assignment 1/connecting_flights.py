# CMPE 365 Week 2 Lab Problem: Connecting Flights
# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

import sys
INFINITY = sys.maxsize

# Prompts user for flight schedule input in the form of a text file.
def readInput():
    filename = input("Enter a file name representing a flight schedule, including the file type: ")
    data = []
    with open(filename, "r") as fileIn:
        # Parse each line as a list of seperated integers and append to a list of all data.
        for line in fileIn:
            data.append(list(map(int, line.split())))
    return data

# Display results given the path that was determined using getPath().
def displayResult(path_array, cost_array, starting_city, destination_city):
    print(f"The optimal route from {starting_city} to {destination_city} is:")
    for i in range(len(path_array)-1):
        print(f"Fly from {path_array[i]} to {path_array[i + 1]}")
    print(f"Arriving at {destination_city} at time {cost_array[destination_city]}")

# Returns the path by tracing through the predecessor_array from the destination city to the starting city.
def getPath(predecessor_array, starting_city, destination_city):
    current_city = destination_city
    path = [current_city]
    while (current_city != starting_city):
        path.insert(0, predecessor_array[current_city])
        current_city = predecessor_array[current_city]
    return path

# Dijkstra's algorithm based on the sudo-code provided in the week 1 lab. This version is modified to allow multiple paths between any two nodes.
def dijkstrasAlgorithm(num_vertices, starting_city, weights):
    # Initialize arrays to their starting positions setting the appropriate starting city for the process.
    cost = [None for i in range(num_vertices)]
    cost[starting_city] = 0
    reached = [False for i in range(num_vertices)]
    reached[starting_city] = True
    estimate = [INFINITY for i in range(num_vertices)]
    estimate[starting_city] = 0
    candidates = [False for i in range(num_vertices)]
    predecessor = [None for i in range(num_vertices)]
    # Update candidates, estimates, and predecessors based on the starting position and its available paths.
    for i in range(num_vertices):
        if (weights[starting_city][i][0] != [0,0]):
            for flight in weights[starting_city][i]:
                if flight[1] < estimate[i]:
                    estimate[i] = flight[1]
                    candidates[i] = True
                    predecessor[i] = starting_city

    # Iterate through all possible nodes to ensure that the optimal cost for each node was calculated.
    for count in range(num_vertices):
        best_candidate_estimate = INFINITY
        # Choose current node and best candidate estimate to proceed with process.
        for i in range(num_vertices):
            if (candidates[i] == True) and (estimate[i] < best_candidate_estimate):
                current_node = i
                best_candidate_estimate = estimate[i]

        cost[current_node] = estimate[current_node]
        reached[current_node] = True
        candidates[current_node] = False

        # Iterate through each node and update variables accordingly.
        for j in range(num_vertices):
            # Check that the flight path exists (greater than 0) and that it has not yet been reached.
            if ((weights[current_node][j][0][1] > 0) and (reached[j] == False)):
                for flight in weights[current_node][j]:
                    # Check that the flight arrives after the previous flight has landed, that the flight path exists, and that the estimate is better than the best_current_estimate.
                    if ((flight[0] > cost[current_node]) and (flight[1] > 0) and (flight[1] < estimate[j])):
                        estimate[j] = flight[1]
                        candidates[j] = True
                        predecessor[j] = current_node

    return cost, predecessor

def Main():
    # Read data for input file and parse the given data into an appropriate data structure.
    data = readInput()
    num_vertices = data[0][0]
    data.pop(0)
    # The data will be stored in a 2-dimensional list of lists of 2-tuples, ie. [[departure_time_1, arrival_time_1], .., [departure_time_n, arrival_time_n]]
    # In this 2-dimensional list, the ith row and jth column represents a list of flights from city i to city j.
    weights = [[[[0,0]] for i in range(num_vertices)] for j in range(num_vertices)]
    for flight in data:
        if(weights[flight[0]][flight[1]][0] == [0,0]):
            weights[flight[0]][flight[1]][0] = [flight[2], flight[3]]
        else:
            weights[flight[0]][flight[1]].append([flight[2],flight[3]])

    # Prompt user for input to determine starting and destination city.
    starting_city = int(input(f"Enter an integer greater than or equal to 0 and less than {num_vertices} representing a starting city: "))
    destination_city = int(input(f"Enter an integer greater than or equal to 0 and less than {num_vertices} representing a destination city: "))
    
    cost_array = [0]*num_vertices
    predecessor_array = [None]*num_vertices
    cost_array, predecessor_array = dijkstrasAlgorithm(num_vertices, starting_city, weights)

    # Display output according to user's input. If there is no available path, display this fact.
    if(starting_city == destination_city):
        print("Please enter a destination city other than the starting city.")
    elif(cost_array[destination_city] == None):
        print(f"There is no valid route from {starting_city} to {destination_city}")
    else:
        path_array = getPath(predecessor_array, starting_city, destination_city)
        displayResult(path_array, cost_array, starting_city, destination_city)

# Call Main funtion to initialize process:
Main()