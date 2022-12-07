################################################
# Libraries:

from collections import defaultdict

################################################
# Functions/Classes:

class ListGenome():

    def __init__(self, n: int):
        self.n = n
        self.genome = ['-']*n
        self.TE_ID = 0
        self.TE_dict = defaultdict()
        
    def insert_te(self, pos: int, length: int):
        self.TE_ID += 1
        self.TE_dict[self.TE_ID] = (pos, length)
        r = []
        for key in self.TE_dict:
            start = self.TE_dict[key][0] 
            end = self.TE_dict[key][0] + self.TE_dict[key][1] 
            if start < pos <= end:
                r.append(key)
                for i in range(start, end):
                    self.genome[i] = 'I'
            if pos < start:
                self.TE_dict[key] = (start + length, self.TE_dict[key][1])
        self.genome[pos:pos] = ['A'] * length
        for key in r:
            self.TE_dict.pop(key)
        return self.TE_ID
            
    
    def copy_te(self, te: int, offset: int):
        element = self.TE_dict[te]
        clone_start = element[0] + offset
        clone_length = element[1]
        self.insert_te(clone_start, clone_length)
        
        
    def disable_te(self, te: int):
        dis_te = self.TE_dict[te]
        for i in range(dis_te[0], dis_te[0]+dis_te[1]):
            self.genome[i] = 'I'
        self.TE_dict.pop(te)
        
    
    def active_tes(self):
        return list(self.TE_dict.keys())
    
    
    def __len__(self):
        return len(self.genome)
    
    
    def __str__(self):
        return ''.join(self.genome)



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
                    cur.val = 'I'
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
        element = self.TE_dict[te]
        clone_start = element[0] + offset
        clone_length = element[1]
        self.insert_te(clone_start, clone_length)
        
    
    def disable_te(self, te: int):
        dis_te = self.TE_dict[te]
        cur = self.genome
        while cur.pos != dis_te[0]:
            cur = cur.out
        for i in range(dis_te[0], dis_te[0]+dis_te[1]):
            cur.val = 'I'
            cur = cur.out
        self.TE_dict.pop(te)
        
        
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
