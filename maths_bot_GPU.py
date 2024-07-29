#Uses GPU for computation (complete redesign: #TODO tidy up files)
#Trial to learn
import torch
import itertools
from Brute_force import Skeletons

import time



if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

print(f"Using {device}")




def populate_valid_skeletons(operators:list,numbers:list,skeletons:list,expressions:list)-> list:
    #Iterate over different combinations of operators
    operator_combinations = set(itertools.combinations(operators*5,5))
    number_permutations = set(itertools.permutations(numbers,6))
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




def main(target,num_list):
    #start with trying to brute force
    operations = ["+","-","*","/"]

    sk = Skeletons()
    op_combinations = set(itertools.combinations(operations*5,5))
    num_list_perms = set(itertools.permutations(num_list,6))
    templates = sk.parse_for_valid_skeletons()
    start = time.time()
    answer_dict = populate_valid_skeletons(op_combinations,num_list_perms,templates)
    display_answer(answer_dict,start)

def display_answer(current_answer,start):
    print(f"Answer: {current_answer['answer']}")
    print(f"Expression = {current_answer['expression']}") 
    print(time.time() - start)
    #Nice display #TODO
    