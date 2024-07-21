#Generate a prime factor tree for the target number as the first strategy

class Node:
    def __init__(self,value,left,right,parent):
        self.value = value
        self.left = left
        self.right = right 
        self.parent = parent

    def traverse_left(self)-> object:
        return self.left 
    
    def traverse_right(self) -> object:
        return self.right

    def get_value(self):
        return self.value
    
    def update_right(self,new_right):
        self.right = new_right

    def update_left(self,new_left):
        self.left = new_left





class Tree:
#find a prime factor

#values to the left are prime
    def __init__(self,root_value):
        self.root_value = root_value
    
    def find_prime_factor(self,number):
        for factor in range(2,number):
            if number%factor == 0:
                return factor
        return None #no factors (so itself)


    def collect_prime_factors(self):
        factors = {}
        traversing = True 
        current_node = self.root_node
        while traversing:
            try:
                factor = current_node.left
                if factor.value in factors: #just add number to dictionary
                    factors[factor.value] += 1
                else:
                    factors[factor.value] = 1
            except AttributeError: #number is an exact prime
                return {1:1,self.root_value:1}
            
            #update current node
            current_node = current_node.right
            #check if at end of tree
            if current_node.right is None:
                factor = current_node.left
                try:
                    if factor.value in factors: #just add number to dictionary
                        factors[factor.value] += 1
                    else:
                        factors[factor.value] = 1
                except AttributeError: #at end of tree 
                    if current_node.value in factors:
                        factors[current_node.value] +=1
                    else:
                        factors[current_node.value] = 1

                return factors



    def make_tree(self):
        self.root_node = Node(self.root_value,None,None,None) 
        current_node = self.root_node #root node
        number = self.root_value
        run = True
        while run:
            factor = self.find_prime_factor(number)
            print(f"current factor = {factor}")
            if factor is not None: 
                current_node.update_left(Node(factor,None,None,number)) #add factor to the left
                #add next node to the right
                next_node = Node(int(number/factor),None,None,number)
                current_node.update_right(next_node)
                #move to the right to repeat
                current_node = next_node
                number = int(number/factor)
            else: #once complete just need to traverse the graph and collect prime factors
                #found final prime
                current_node.value = number
                #Complete
                break 




if __name__ == "__main__":
    tree = Tree(9999999999999)
    tree.make_tree()
    print(tree.collect_prime_factors())

