import itertools

#Maths round bot

#Rules:
#Must take less that 30 secs
#only use the four basic operations
#There are 6 numbers 
#Get as close as possible to the target number 

class MathsBot:
    def __init__(self,target,num_list) -> None:
        self.target = target 
        self.num_list = num_list #0-5 index
        self.operations = ["+","-","*","/"]

    def generate_all_possible_combos(self) -> list:
        #generates all possible permutations of operationsof length 1-r (power set)
        combined_list = self.operations + self.num_list #concatinate lists (combine)
        self.generated_poweset = self.powerset(combined_list)



    def powerset(self,iterable):
        
        
        '''"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(3,len(s)+1)))'''


    def evaluate_powerset(self):
        #1) get all legitimate combinations
        #2) evaluate them and find the closest to the target 
        closest_answer = 0 
        
        
        for phrase in self.generated_poweset:
            for expression in list(itertools.permutations(phrase)):
                current_ans = self.make_and_eval_rpn(expression)
                if current_ans is not False and abs(self.target-current_ans) < abs(self.target- closest_answer): #if legit and closer
                    closest_answer = current_ans
        return closest_answer


    def make_and_eval_rpn(self,expression):
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

    def run(self):
        self.generate_all_possible_combos()
        answer = self.evaluate_powerset()
        print(f"Closest answer: {answer}")


if __name__ == "__main__":
    target = int(input("What is the target? "))
    num_list = []
    num_string = input("What are the numbers (seperate with a space)? ")
    num_list += num_string.split(" ")
    maths_bot = MathsBot(target,num_list)
    maths_bot.run()