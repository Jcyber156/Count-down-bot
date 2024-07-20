import itertools
import Create_prime_factor_tree

#Maths round bot

#Rules:
#Must take less that 30 secs
#only use the four basic operations
#There are 6 numbers 
#Get as close as possible to the target number 

class MathsBot:
    #Idea 1 :split into products of primes. If it is a prime number, find the primes surrounding the number
    def __init__(self,target,num_list) -> None:
        self.target = target 
        self.num_list = num_list #0-5 index
        self.operations = ["+","-","*","/"]

        #make prime factor tree
        self.prime_factor_tree = Create_prime_factor_tree.Tree(root_value= self.target)
        self.prime_factor_tree.make_tree()



    def eval_rpn(self,expression):
        stack = []
        ops_performed = False
        for item in expression:
            if item not in self.operations: #is a number 
                stack.append(int(item)) #push to stack
            else: #have an operation to pop appropriate items from stack and push back
                if len(stack) >=2: #avoid stack underflow
                    ops_performed = True
                    first = stack.pop()
                    second = stack.pop()
                    #perform operation
                    match item:
                        case "+":
                            ans = first + second
                        case "-":
                            ans = first - second 
                        case "*":
                            ans = first * second 
                        case "/":
                            try:
                                ans = first / second 
                            except ZeroDivisionError:
                                return False #avoid division by 0
                    #push answer to stack
                    stack.append(ans) 
                else: #stack underflow so expression not valid 
                    return False 
        if ops_performed ==True and stack[0] >0:
            return stack[0] #final answer
        return False



if __name__ == "__main__":
    num_list  = []
    num_list+= str(input("Enter numbers (seperated by a space): ")).split(" ")
    target = int(input("What is the target? "))
    maths_bot = MathsBot(target,num_list)

    print(maths_bot.prime_factor_tree.collect_prime_factors())