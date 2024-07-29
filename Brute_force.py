#Might be possible to bf by making some educated guesses and already having some of the computations done
import itertools
import more_itertools
class BruteForce:
    def __init__(self,numbers:list,target:int):
        self.numbers = numbers
        self.target = target 

        self.operators = ["+","-","/","*"]


    def populate_valid_skeletons(self):
        sk = Skeletons()
        skeletons = sk.parse_for_valid_skeletons()
        expressions = []
        #Iterate over different combinations of operators
        operator_combinations = set(itertools.combinations(self.operators*5,5))
        number_permutations = set(itertools.permutations(self.numbers,6))
        print("permuatations and combinations complete")
        print(f"Skeleton = {len(skeletons)}")
        print(f"Operands = {len(operator_combinations)}")
        print(f"Number perms = {len(number_permutations)}")
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
                    expressions.append(populated)
        return expressions



class Skeletons:

    def generate_valid_expression_skeletons(self):
        #Generate the skeletons for valid expressions to improve computation (reduce number of nessicary perms)
        #NOTE This function only needs to be run once to generate the perm file that can then be used
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
        with open("valid_expressions.txt","w") as f:
            for i in valid:
                to_write = str(i).replace(", ","")
                to_write = to_write.strip("()")
                f.write(to_write+"\n")
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
    sk = Skeletons()
    sk.parse_for_valid_skeletons() 
