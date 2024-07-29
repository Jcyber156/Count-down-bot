import time
import itertools
from Brute_force import Skeletons
from multiprocessing import Pool

#https://cdn.discordapp.com/attachments/690290111115821087/1266333275065028679/image.png?ex=66a76744&is=66a615c4&hm=e5291921320476b65c7c82059db9d74664e7c2445c5ea801fa32bac80b31f820&
#Test data
global results
results = []

def populate_valid_skeletons(templates,operator_combinations,number_permutations)-> list:
    #Iterate over different combinations of operators
    expressions = []


    for skeleton in templates:
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



def get_results(results_i):
    results.append(results_i)



if __name__ == "__main__":
    num_list  = []
    num_list+= str(input("Enter numbers (seperated by a space): ")).split(" ")
    num_list = [int(x) for x in num_list] #convert all element into int()

    target = int(input("What is the target? "))


    sk = Skeletons()
    templates = sk.parse_for_valid_skeletons()


    #Multi-threading logic
    p = Pool(processes = 14)
    
    operator_combinations = set(itertools.combinations(["+","-","*","/"]*5,5))
    number_permutations= set(itertools.permutations(num_list,6))

    start = time.time()
    for i in range(14):
        p.apply_async(populate_valid_skeletons,args=(templates[i*3:(i+1)*3],operator_combinations,number_permutations),callback=get_results)
    p.close()
    p.join()

    print(time.time()-start)
    #RESULTS APPENED AND ACCESSED CORRECTLY WHOOOOOOOOOOOHOOOOOOOO
