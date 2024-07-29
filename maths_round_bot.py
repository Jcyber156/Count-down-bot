import itertools
import more_itertools
import sys
import time
import cuda



#import Create_prime_factor_tree
#import prime_factors_strat

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


        '''#make prime factor tree
        self.prime_factor_tree = Create_prime_factor_tree.Tree(root_value= self.target)
        self.prime_factor_tree.make_tree()
        self.prime_factors = self.prime_factor_tree.collect_prime_factors()'''


    @cuda.jit(forceobj = True)
    def eval_rpn(self,expressions,target):
        
        current_answer = {"answer":0,
                        "expression": [0]}
        
        #define function here for GPU use
        def compare_answer_with_target(answer,expression,current_answer):
            if abs(target - answer) < abs(target - current_answer["answer"]): #is closer
                current_answer["answer"] = answer 
                current_answer["expression"] = expression 
            
            if current_answer['answer'] == target:
                return True
            return False

        
        for expression in expressions:
            stack = []
            used_expression = []
            for item in expression:
                used_expression.append(item)
                if item not in self.operations: #is a number 
                    stack.append(int(item)) #push to stack
                else: #have an operation to pop appropriate items from stack and push back
                    if len(stack) >=2: #avoid stack underflow
                        first = stack.pop()
                        second = stack.pop()
                        
                        #perform operation
                        match item:
                            case "+":
                                ans = first + second
                            case "-":
                                ans = first - second 
                                if ans <0:
                                    return False #breaks rules of countdown
                            case "*":
                                ans = first * second 
                            case "/":
                                try:
                                    ans = first / second 
                                except ZeroDivisionError:
                                    return False #avoid division by 0
                                if ans % 1 !=0: #not an integer division (breaks rules of countdown):
                                    return False
                        #push answer to stack
                        stack.append(ans) 
                        if compare_answer_with_target(ans,used_expression,current_answer) is True:
                            return current_answer
        return current_answer


    
    def main(self):
        #start with trying to brute force
        bf = BruteForce(self.target,self.num_list)
        sk = Skeletons()
        op_combinations = set(itertools.combinations(self.operations*5,5))
        num_list_perms = set(itertools.permutations(self.num_list,6))
        templates = sk.parse_for_valid_skeletons()
        answer_dict = bf.populate_valid_skeletons(op_combinations,num_list_perms,templates)
        self.display_answer(answer_dict)




    def display_answer(self,current_answer):
        print(f"Answer: {current_answer['answer']}")
        print(f"Expression = {current_answer['expression']}") 
        print(time.time() - start)
        #Nice display 
        print("------------------------")
        self.rpn_for_nice_display(current_answer['expression'])

    def rpn_for_nice_display(self,expression):
        #much simpler as no need to validate anything (already done)
        stack = []
        for item in expression:
            if item not in self.operations:
                stack.append(item)
            else:
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
                        ans = first / second 
                print(f"{first}{item}{second} = {ans}")
                stack.append(ans)

class BruteForce(MathsBot):
    def __init__(self,target,numbers):
        super().__init__(target,numbers)


    def populate_valid_skeletons(self,operator_combinations,number_permutations,skeletons):
        all_expressions = [] #store all checked expressions
        #Iterate over different combinations of operators
        print("running")
        for skeleton in skeletons:
            for operator_sequence in operator_combinations:
                for number_sequence in number_permutations:
                    populated = []
                    operator_index_counter = 0
                    numbers_index_counter = 0
                    for value in skeleton:
                        if value == 0:
                            #operator
                            populated.append(operator_sequence[operator_index_counter])
                            operator_index_counter +=1
                        else:
                            populated.append(number_sequence[numbers_index_counter])
                            numbers_index_counter +=1
                    #Now populated
                    #self.eval_rpn(populated)
                    all_expressions.append(populated)
        #Find best answer
        print("Evaluating")
        answer_dict = self.eval_rpn(all_expressions)
        return answer_dict #returns current_answer dictionary





    '''def remove_communicative_expressions(self,expression,previous_expressions):
        #To avoid running unnessary checks on an expression that is similar to a previous solution.
        #e.g if done 2,1,+. There is no need to do 1,2+ as the answer to that is the same'''


class Skeletons:
    def generate_valid_expression_skeletons(self):
        #Generate the skeletons for valid expressions to improve computation (reduce number of nessicary perms)

        skel_nums = [1 for x in range(6)]
        skel_operators = [0 for x in range(5)]

        combined_lists = skel_nums+ skel_operators

        #all perms
        all_perms = list(more_itertools.distinct_permutations(combined_lists))
        '''with open("All_Skeletons.txt","w") as f:
            for permutation in all_perms:
                f.write(str(permutation))'''
        return all_perms

    def parse_for_valid_skeletons(self):
        valid = []
        all_perms = self.generate_valid_expression_skeletons()
        for perm in all_perms:
            #Only expressionss that could follow RPN rules
            if self.validate_permutation(perm) is True:
                valid.append(perm)
        return valid

    def validate_permutation(self,perm):
        counter = 0
        for value in perm:
            if value == 1:
                counter += 1
            else: #so operator
                if counter <2: #invalid (for RPN):
                    return False
                else:
                    counter -= 1
        #At this point, passed all tests so append to list
        return True




if __name__ == "__main__":
    num_list  = []
    num_list+= str(input("Enter numbers (seperated by a space): ")).split(" ")
    num_list = [int(x) for x in num_list] #convert all element into int()
    
    target = int(input("What is the target? "))
    maths_bot = MathsBot(target,num_list)

    start = time.time()
    maths_bot.main()

#Can now always find a solution/best solution but can take /is quite likely to take too long so
#move eval into creation of expressions? 
