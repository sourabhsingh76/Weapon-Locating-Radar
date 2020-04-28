import os
import sys
import math
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x_coordinate(self):
        return self.x

    def get_y_coordinate(self):
        return self.y
    
    def euclidean_distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2) 


class Some_Object(Point):
    def __init__(self, starting_x, starting_y, v_x, v_y):
        Point.__init__(self, starting_x, starting_y)
        self.delta_t = 1
        self.v_x = v_x
        self.v_y = v_y
        
    def increment_x_coor(self):
        self.x += self.delta_t*self.v_x
    
    def increment_y_coor(self):
        self.y += self.delta_t*self.v_y

# THis function defines all the three components of the bistatic radar system
# Namely Transmitter, Receiver, Missile As in the paper
def main(coordinate_plane):
    # Transmitter is located at the point (0, 0)
    Transmitter = Some_Object(0, 0, 0, 0)
    
    # receiver starts at some (x, y)
    receiver_starts_x = random.randint(coordinate_plane[0][0], coordinate_plane[1][0])
    receiver_starts_y = random.randint(coordinate_plane[0][1], coordinate_plane[1][1])
    receiver_v_x = 70
    receiver_v_y = 0
    Receiver = Some_Object(receiver_starts_x, receiver_starts_y, receiver_v_x, receiver_v_y )

    # The target is coming directly towards the transmitter
    target_starting_X = random.randint(coordinate_plane[0][0], coordinate_plane[1][0])
    target_starting_y = 0
    target_v_x = -600
    target_v_y = 0
    Target = Some_Object(target_starting_X, target_starting_y, target_v_x, target_v_y)

    return Transmitter, Receiver, Target

def check(x, y, max_x, max_y, min_x, min_y):
    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    return False

def simulate():
    coordinate_plane = [(0, 0), (60000, 60000)]
    Transmitter, Receiver, Target = main(coordinate_plane)
    # Define the 2D coordinate plane
    # The coordinate plane is a square with (0,0) as the origin and (x, x) as the ending point
    receiver = []
    target = []
    transmitter = []
    for i in range(2000):
        receiver_x = Receiver.get_x_coordinate()
        receiver_y = Receiver.get_y_coordinate()

        transmitter_x = Transmitter.get_x_coordinate()
        transmitter_y = Transmitter.get_y_coordinate()

        target_x = Target.get_x_coordinate()
        target_y = Target.get_y_coordinate()
        
        if not check(receiver_x, receiver_y, coordinate_plane[1][0], coordinate_plane[1][1], coordinate_plane[0][0], coordinate_plane[0][1]):
            print('Receiver outside simulated area')
            break
        elif not check(target_x, target_y, coordinate_plane[1][0], coordinate_plane[1][1], coordinate_plane[0][0], coordinate_plane[0][1]):
            print('Target outside simulated area')
            break

        receiver.append(tuple([receiver_x, receiver_y]))
        target.append(tuple([target_x, target_y]))
        transmitter.append(tuple([transmitter_x, transmitter_y]))

        # Increment the positions of the receiver and target
        Receiver.increment_x_coor()
        Receiver.increment_y_coor()

        Target.increment_x_coor()
        Target.increment_y_coor()


    
    return transmitter, receiver, target
    
if __name__ == "__main__":
#     Transmitter = Some_Object(0, 0, 0, 0)
#     print(Transmitter.get_x_coordinate(), Transmitter.get_y_coordinate())

    transmitter, receiver, target = simulate()  
    print("TRANSMITTER COORDINATES : ", transmitter)
    print("RECEIVER COORDINATES : ", receiver)
    print("TARGET COORDINATES : ", target)