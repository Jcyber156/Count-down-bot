import copy
import itertools
#Try to solve the target by using a method around prime factos (only run if bot thinks it is possible)
#(should only really be used if there are about 3 different factors)
#TODO complete


class Strat:
    def __init__(self,prime_factors:dict,target:int,given_numbers:list) -> None:
        self.target = target
        self.prime_factors = prime_factors
        self.given_numbers = given_numbers
        self.given_numbers.sort(reverse = True)

        self.expression_answer= [] #list for storing the RPN expression for algorithms given answer
        self.operations = ["+","-","*","/"]


    def direct_strat(self):
        #make a copy
        given = copy.deepcopy(self.given_numbers)
        wanted = []
        used = []
        #The most direct stategy:
        #TODO remove
        self.try_make_p_factors(given,wanted,used)
        return None
        
        '''
        See if multiples of the prime factors can be made/prime factors themselves 
        e.g: 2^2 = 4. Need to use/make a 4
        '''
        for factor in self.prime_factors:
            to_achieve = factor**self.prime_factors[factor]
            wanted.append(to_achieve)

        for factor in wanted:
            if factor in given:
                given.remove(factor) #if we already have the number, use it
                used.append(factor)
            else:
                #Try to make prime factor's
                '''Iterate over all numbers trying to find combinations of numbers to give prime factors
                For powered prime factors (in example above) still need to consider multiplication
                Since numbers are sorted highest-lowest, if the last 2 multiplied are too big, can move on'''
                for prime in wanted:
                    if given[-1] * given[-2] <= prime:
                        self.try_make_p_factors(given,wanted,used) #TODO store returns

    def try_make_p_factors(self,given,wanted,used):
        combos = []
        if len(used) == 0: #avoid trying to solve all board sets
            end = len(given) -2
        else:
            end = len(given)
        for r in range(2,end):
            combos.append(list(itertools.combinations(given,r)))
        for comboset in combos:
            for combo in comboset: #now down to each individual combination
                possible_answers = [] #stores expressions to be evaluated for prime
                for operation in self.operations:





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
                                print("Attempted division by 0")
                                return False #avoid division by 0
                    #push answer to stack
                    stack.append(ans) 
                else: #stack underflow so expression not valid 
                    return False 
        if ops_performed ==True and stack[0] >0:
            return stack[0] #final answer
        return False
