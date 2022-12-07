################################################
# Libraries:

from collections import defaultdict
from abc import ABC, abstractmethod

################################################
# Functions/Classes:


class Genome(ABC):
    """Representation of a circular genome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet
        
    @abstractmethod
    def insert_te(self, pos: int, length: int):
        """
        Insert a new transposable element.
        Insert a new transposable element at position pos and len
        nucleotide forward.
        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.
        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int):
        """
        Copy a transposable element.
        Copy the transposable element te to an offset from its current
        location.
        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.
        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int):
        """
        Disable a TE.
        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self):
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self):
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self):
        """
        Return a string representation of the genome.
        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.
        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


# class ListGenome():

#     def __init__(self, n: int):
#         self.n = n
#         self.genome = ['-']*n
#         self.TE_ID = 0
#         self.TE_dict = defaultdict()
        
#     def insert_te(self, pos: int, length: int):
#         self.TE_ID += 1
#         self.TE_dict[self.TE_ID] = (pos, length)
#         r = []
#         for key in self.TE_dict:
#             start = self.TE_dict[key][0] 
#             end = self.TE_dict[key][0] + self.TE_dict[key][1] 
#             if start < pos <= end:
#                 r.append(key)
#                 for i in range(start, end):
#                     self.genome[i] = 'x'
#             if pos < start:
#                 self.TE_dict[key] = (start + length, self.TE_dict[key][1])
#         self.genome[pos:pos] = ['A'] * length
#         for key in r:
#             self.TE_dict.pop(key)
#         return self.TE_ID
            
    
#     def copy_te(self, te: int, offset: int):
#         if te in self.TE_dict:
#             element = self.TE_dict[te]
#             clone_start = (element[0] + offset) % len(self)  ############
#             clone_length = element[1]
#             self.insert_te(clone_start, clone_length)
#             return self.TE_ID
#         else:
#             return None
        
#     def disable_te(self, te: int):
#         if te in self.TE_dict.keys():
#             dis_te = self.TE_dict[te]
#             for i in range(dis_te[0], dis_te[0]+dis_te[1]):
#                 self.genome[i] = 'x'
#         self.TE_dict.pop(te)
#         return None
    
#     def active_tes(self):
#         return list(self.TE_dict.keys())
    
    
#     def __len__(self):
#         return len(self.genome)
    
    
#     def __str__(self):
#         return ''.join(self.genome)

class ListGenome(Genome):
    """
    Representation of a genome.
    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = ['-']*n # portion of genome that is not inactive or active TE is represented as "-"
                                #accoring to line 124 in example abstract genome class 
        self.te = dict() # self.te is a dictonary so we can store TE id as key, and map position and length to that id 
        self.id = 0 # the first id will be 0 

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.
        Insert a new transposable element at position pos and len
        nucleotide forward.
        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.
        Returns a new ID for the transposable element.
        """
        self.id += 1 #reminder that self.id is the index number of transcriptional element, starts at 0 so first will be 1
        self.te[self.id] = [pos, length] # new item in self.te dictionary at with the index [self.id]
                                         # in index of self.if, [0] = pos, [1]= length (supplied in input of class)
        key_list = list(self.te.keys()) # keys() is a built in python method (idea from Sara) that calls all the keys of a dictionary 
        for key in key_list: # this for loop: 
            #1. establishes where new te should go 
            #2. checks to see if there is already a te there and converts it to inactive if so
            #3. inserts the new te into the genome 
            start = self.te[key][0] #see line 156
            end = start + self.te[key][1] #see line 156

            if start < pos <= end: # check to see if there is already a te in location where new te wants to go 
                                   # this works because we havent reassined pos to the index of the new te yet. 
                for i in range(start, end): # this loop changes preexisting te to inactive 
                    self.genome[i] = 'x' 
                del self.te[key] #we need to delete the key of the inactivated te from dictionary since there is a new te in that index on genome 

            if pos < start: #this statement moves the 'x' features of old te to their new loccation 
                new_start = start + length 
                self.te[key][0] = new_start #because we deleted this value in line 169, need to update where old te is in dictionary  
        transcriptional_element = ['A'] * length # assign new TE per assignment 
        self.genome[pos:pos] = transcriptional_element #put in the new te we created in line above in correct place 
                                                        #(reminder pos is one of the inputs for class)
        return self.id #index number of new transcriptional element in genome 

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.
        Copy the transposable element te to an offset from its current
        location.
        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.
        If te is not active, return None (and do not copy it).
        """
        if te in self.te.keys(): # if input is in the dictionary (need to go through keys list to limit computational time) 
            position = (self.te[te][0] + offset) % len(self) # from Sara and Laura, see line 156 but tbh im not sure how this works
                                                      # position needs to be in terms of % len 
            length = self.te[te][1] # see line 156
            self.insert_te(position, length) #pos = p, length= l 
            return self.id
        else:
            return None

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.
        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        if te in self.te.keys(): #we are given te as an integer, it is the index number of the te,
                                 #which is the key in our dictionary that maps to the position [0] and length [1]
            start = self.te[te][0] 
            end = start + self.te[te][1] 
            for i in range(start, end): 
                self.genome[i] = 'x' #x marks that it is inactivated 
            del self.te[te]
        return None
            
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te.keys())  

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome) 

    def __str__(self) -> str:
        """
        Return a string representation of the genome.
        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.
        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return ''.join(self.genome) # easy to join lists into a string 



class LinkedListGenome():
    
    class Node:
        def __init__(self, val='-', pos=None):
            self.val = val
            self.pos = pos
            self.out = None

    def __init__(self, n: int):
        self.n = n
        self.genome = self.Node('-', 0)
        cur = self.genome
        for i in range(n-1):
            cur.out = self.Node('-', i+1)
            cur = cur.out
            if cur.out == None:
                cur.out = self.genome
        self.TE_dict = defaultdict()
        self.TE_ID = 0
        
    
    def insert_te(self, pos: int, length: int):
        self.TE_ID += 1
        self.TE_dict[self.TE_ID] = (pos, length)
        r = []
        for key in self.TE_dict:
            start = self.TE_dict[key][0] 
            end = self.TE_dict[key][0] + self.TE_dict[key][1] 
            if start < pos <= end:
                r.append(key)
                cur = self.genome
                while cur.pos != start:
                    cur=cur.out
                for i in range(start, end):
                    cur.val = 'x'
                    cur = cur.out
            if pos < start:
                self.TE_dict[key] = (start + length, self.TE_dict[key][1])
        
        cur = self.genome
        while cur.pos != pos:
            genome_first = cur
            cur=cur.out
            genome_last = cur
        
        branch_first = self.Node('A', None)
        cur = branch_first
        for i in range(1,length):
            cur.out = self.Node('A', None)
            cur = cur.out
        branch_last = cur
        genome_first.out = branch_first
        branch_last.out = genome_last
        
        stop = self.genome.pos
        counter = stop + 1
        cur = self.genome.out
        while cur.pos != stop:
            cur.pos = counter
            counter+=1
            cur = cur.out
            
        for key in r:
            self.TE_dict.pop(key)
        return self.TE_ID
    
    def copy_te(self, te: int, offset: int):
        if te in self.TE_dict:
            element = self.TE_dict[te]
            clone_start = (element[0] + offset) % len(self)  ############
            clone_length = element[1]
            self.insert_te(clone_start, clone_length)
            return self.TE_ID
        else:
            return None
        
    
    def disable_te(self, te: int):
        if te in self.self.TE_dict.keys():
            dis_te = self.TE_dict[te]
            cur = self.genome
            while cur.pos != dis_te[0]:
                cur = cur.out
            for i in range(dis_te[0], dis_te[0]+dis_te[1]):
                cur.val = 'x'
                cur = cur.out
        self.TE_dict.pop(te)
        return None

        
    def active_tes(self):
        return list(self.TE_dict.keys())
    
    
    def __len__(self):
        cur = self.genome.out
        count = 1
        while cur.pos != 0:
            count+=1
            cur=cur.out
        return count
    
    
    def __str__(self):
        string = self.genome.val
        cur = self.genome.out
        while cur.pos != 0:
            string+=cur.val
            cur=cur.out
        return string

#####################

