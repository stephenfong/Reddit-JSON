"""
/*
 * Copyright © 2022 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6250 Computer Networks
 * Instructors: Maria Konte
 * Head TAs: Johann Lau and Ken Westdorp
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However,
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials
 * (including exam keys, project requirements, etc.) and do not distribute them
 * to anyone not enrolled in the class. Use of any previous semester course
 * materials, such as tests, quizzes, homework, projects, videos, and any other
 * coursework, is prohibited in this course.
 */
"""

# Spanning Tree Protocol project for GA Tech OMSCS CS-6250: Computer Networks
#
# Copyright 2023 Vincent Hu
#           Based on prior work by Sean Donovan, Jared Scott, James Lohse, and Michael Brown

from Message import Message
from StpSwitch import StpSwitch


class Switch(StpSwitch):
    """
    This class defines a Switch (node/bridge) that can send and receive messages
    to converge on a final, loop-free spanning tree. This class
    is a child class of the StpSwitch class. To remain within the spirit of
    the project, the only inherited members or functions a student is permitted
    to use are:

    switchID: int
        the ID number of this switch object)
    links: list
        the list of switch IDs connected to this switch object)
    send_message(msg: Message)
        Sends a Message object to another switch)

    Students should use the send_message function to implement the algorithm.
    Do NOT use the self.topology.send_message function. A non-distributed (centralized)
    algorithm will not receive credit. Do NOT use global variables.

    Student code should NOT access the following members, otherwise they may violate
    the spirit of the project:

    topolink: Topology
        a link to the greater Topology structure used for message passing
    self.topology: Topology
        a link to the greater Topology structure used for message passing
    """

    def __init__(self, idNum: int, topolink: object, neighbors: list):
        """
        Invokes the super class constructor (StpSwitch), which makes the following
        members available to this object:

        idNum: int
            the ID number of this switch object
        neighbors: list
            the list of switch IDs connected to this switch object
        """
        super(Switch, self).__init__(idNum, topolink, neighbors)
        # TODO: Define class members to keep track of which links are part of the spanning tree
        
        self.idNum = idNum 
        self.neighbors = neighbors
        
        self.root = idNum
        self.distance = 0 
        # self.dist2root = 0
        self.activeLinks = set() # .remove() 
        self.switchThrough = 0 
        #self.pathThrough = False

        
        #print(f"idNum: {idNum}")
        #print(f"Neighbors: {neighbors}")
        
        # Maybe place data structure here: dictionary 

        # I think each node keeps track of its neighbors thru their config messages
        # Keep track of sender ID, root ID, distance to root



    def process_message(self, message: Message):
        """
        Processes the messages from other switches. Updates its own data (members),
        if necessary, and sends messages to its neighbors, as needed.

        message: Message
            the Message received from other Switches
        """
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        # Process message
        # root = message.root
        # distance = message.distance 
        # origin = message.origin
        # destination = message.destination
        # pathThrough = message.pathThrough

        #print("idNum:", self.idNum)
        #print(message)

        # a. 
        # smaller root found
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1

            if self.switchThrough in self.activeLinks:
                #print(f"{self.idNum}: {self.switchThrough} is in {self.activeLinks}, active links - smaller root found")
                self.activeLinks.remove(self.switchThrough)
                #print(f"{self.idNum}: {self.switchThrough} is in {self.activeLinks}, active links - smaller root found")


            self.activeLinks.add(message.origin)
            self.switchThrough = message.origin
            #print(f"{self.idNum}: {self.switchThrough} is in {self.activeLinks}, active links - result")


        # root is same, message distance is shorter
        elif message.root == self.root:
            #print("same root")

            if message.distance + 1 < self.distance:
                #print("message shorter distance")

                self.distance = message.distance + 1

                if self.switchThrough in self.activeLinks:
                    #print(f"{self.switchThrough} is in active links 2")
                    self.activeLinks.remove(self.switchThrough) 

                self.activeLinks.add(message.origin)
                self.switchThrough = message.origin
               
            # root and distance are the same
            elif message.distance + 1 == self.distance:
                #print("message same distance")

                #print(self.idNum,":", message.origin, self.switchThrough)

                if message.origin < self.switchThrough:
                    #print("smaller switchID")

                    if self.switchThrough in self.activeLinks:
                        #print(f"{self.switchThrough} is in active links 3")
                        self.activeLinks.remove(self.switchThrough)

                    self.activeLinks.add(message.origin)
                    self.switchThrough = message.origin
                    
                # I don't think 170 - 177 is needed, code runs the same without    
                elif message.origin > self.switchThrough:
                    #print("bigger switchID")

                    if message.origin in self.activeLinks:
                        #print("in active links")
                        self.activeLinks.remove(message.origin)
                        #print(message.origin in self.activeLinks)
                        #print(self.activeLinks)


              
            # elif message.distance + 1 > self.distance:      
            #     self.activeLinks.add(message.origin)


        # b.
        if message.pathThrough:
            if message.origin not in self.activeLinks:
                self.activeLinks.add(message.origin)
                
        elif message.pathThrough == False:
            if message.origin in self.activeLinks:
                #print("Removed bc F paththrough")  
                #print(message.origin, self.switchThrough) 
                if message.origin != self.switchThrough:
                    self.activeLinks.remove(message.origin)
            
        # How to send a message
        passThrough = False
        ttl = message.ttl
        
        #print(ttl)
        if ttl > 0:
            for destination in self.neighbors:
                if destination == self.switchThrough:
                    passThrough = True
       
                # this is needed because the passThrough doesn't reset to False since it's instantiated before the started of the loop
                elif destination != self.switchThrough: 
                    passThrough = False
                
                #print(self.idNum,":", message.origin, self.switchThrough)
                #print("destination:", destination)
                #print("passThrough:", passThrough)
                
                self.send_message(Message(self.root, self.distance, self.idNum, destination, passThrough, ttl - 1))

            # msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough, ttl)
            #self.send_message(Message(0, 0, 0, 0, False, 0))
        


        # Accepts and processes messages, updates its info of neighbors ID, potential best root, and distance to root
        # sends messages to its neighbors? 
        # Probably want to send messages as a tuple (sender ID, root ID, distance to root)



    def generate_logstring(self):
        """
        Logs this Switch's list of Active Links in a SORTED order

        returns a String of format:
            SwitchID - ActiveLink1, SwitchID - ActiveLink2, etc.
        """
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked
        #      only after the simulation is complete.  Output the links included in the
        #      spanning tree by INCREASING destination switch ID on a single line.
        #
        #      Print links as '(source switch id) - (destination switch id)', separating links
        #      with a comma - ','.
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #
        #      A full example of a valid output file is included (Logs/) in the project skeleton.


        # Logs the final spanning tree after the algorithm is complete
        # By this point the links that are loops are cut off
        # Active links are the connections that are still active after the algorithm
        # Inactive links are the connections that are cut off to prevent an infinite loop
        # Nodes need to know the path to the root, and they need to know the switchThrough
        # Logs a sorted string of its neighbors by its ID and destination ID

        #print(f"generate log string - {self.idNum}")
        #print(f"{self.idNum} - active link #") 
        #print(self.activeLinks)
        
        sortedlist = sorted(list(self.activeLinks)) # and use a for loop and append to string 
        result = ""
        for link in sortedlist:
            if link != sortedlist[-1]: 
                result += f"{self.idNum} - {link}, " 
            else: 
                result += f"{self.idNum} - {link}"
        print(result)
        return result
    
#print('hello')
