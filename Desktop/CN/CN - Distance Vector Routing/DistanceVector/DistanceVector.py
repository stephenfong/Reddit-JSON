# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *
#import copy


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
    
        self.name = name
        self.outgoing_links = outgoing_links
        self.incoming_links = incoming_links
        #self.dv = [f"{self.name}0"] # node's distance vector, as a list
        #self.dv = set([f"{self.name}|0"]) # node's distance vector, as a set
        self.dv = {self.name : 0} # node's distance vector, as a dictionary
        #self.delay_msg = []
        
        self.test = 0
        """# order doesn't matter, and helpers.py alphabetizes

        # maybe use a dictionary to keep track of each neighbors path weights

        # or a list of tuples, need to figure out the names of the nodes, (name, weight)

        # each node has its own routing table

        # the calculations run are based on the distance vector routing algorithm:

        # dx(y) = min{c(x,y) + dy(y), c(x,z)+dz(y)} = min{2+0, 7+1} = 2  

        # the distance from X to Y(X -> V - ?? - > Y)

        # X's neighbor is V, so it knows the distance(weight)

        # X is trying to find the lowest cost route between V and Y which can added to the already known distance from itself to V.

        # Must be able to detect negative cycles and mark it as -99 (negative infinite loop)

        # The algorithm stops running when all the routing tables are the same

        # Which is the same as the nodes no longer sending updates to each other"""

        
        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py

        """ # This sends the intial message

        # Each node has a table with all nodes
        # neighbors distance vector is the weight
        # all nodes beyond neighbors are infinitely distant
        
        # =-=-= INITIAL MESSAGES =-=-=:
        # The initial message that is sent the weight of neighbors?
        # neighbors tell their neighbors how far away they are from each other
        # everything else is infinitely far away

        # =-=-= Following messages =-=-=:
        # advertise to neighbors of routes to other nodes
        # 
        # keep sending messages to each other
        # stop when messages are no longer sent 

        # How to send a message?
        # send messages to neighbors: how far away it is away from its neighbor
        
        #print("Send initial messages")
        #print("Current Node: ", self.name) # Current node

        # Outgoing
        # print("Outgoing")
        # for out in self.outgoing_links:
        #    print(f"{out.name}, {out.weight}")
        
        # Incoming
        #rint("Incoming")
        #for out in self.incoming_links:
        #    print(f"{out.name}, {out.weight}")
        """
 
        # Initial message: (origin, nodeWeight)
        initial_msg = self.name, [f"{self.name}|0"]
        for link in self.incoming_links:
            self.send_msg(initial_msg, link.name)


    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # print("process BF")
        #print("Current Node: ", self.name)
        # print("messages: ", self.messages)

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:

        # TODO 1. Process queued messages       

        round_start_dv = {} 
        for key in list(self.dv.keys()):
            round_start_dv[key] = self.dv[key]

        # Loop for messages
        for msg in self.messages:      
            #print(msg)      
            origin = msg[0] # origin == neighbor
            nbweight = self.get_outgoing_neighbor_weight(origin)

            links = msg[1] # ex. ("AD|0", "AE|1", "AB|2")

            # Loop for links
            for link in links: # each link will be "AD|0"
                #print("link: ", link)
                link_name, link_weight = link.split("|")
                #print(link_name, link_weight)
                nbweight = int(nbweight)
                link_weight = int(link_weight)
                total_dist = nbweight + link_weight

                if link_name not in list(self.dv.keys()) and link_name != self.name:
                    self.dv[link_name] = total_dist

                elif link_name in list(self.dv.keys()) and link_name != self.name:
                    if nbweight <= -99 or link_weight <= -99 or total_dist <= -99:
                        self.dv[link_name] = -99
                    elif total_dist < self.dv[link_name] and total_dist > -99: 
                        self.dv[link_name] = total_dist
                
        #print("Distance Vector for", self.name, self.dv)
        
        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances       

        if round_start_dv != self.dv: #and self.dv[self.name] > -98: # only send messages if distance vector changes

            distance_vector = []
            for key in list(self.dv.keys()):
                distance_vector.append(f"{key}|{self.dv[key]}")

            updated_msg = self.name, distance_vector # have to change the message

            for link in self.incoming_links:
                self.send_msg(updated_msg, link.name) 

            # self.delay_msg = updated_msg # save the message, send it beginning of the next round
                

    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """

        # Logging function
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.    
        
        result = ""
        #for neighbor in self.dv.keys():
        for key in list(self.dv.keys()):
            #neighbor = self.dv[key].replace("|", "")
            result += f"{key}{self.dv[key]}"
            result += ","
        result = result[:-1]
        add_entry(f"{self.name}", f"{result}")  

        #add_entry("A", "A0,B1,C2")        
         
