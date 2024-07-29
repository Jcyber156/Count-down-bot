import time
import itertools
from Brute_force import Skeletons
from multiprocessing import Process,Array,Manager

#https://cdn.discordapp.com/attachments/690290111115821087/1266333275065028679/image.png?ex=66a76744&is=66a615c4&hm=e5291921320476b65c7c82059db9d74664e7c2445c5ea801fa32bac80b31f820&
#Test data



def populate_valid_skeletons(operator_combinations,number_permutations,skeletons,expressions,template_segment:list)-> list:
    #Iterate over different combinations of operators
    skeletons = skeletons[template_segment[0]:template_segment[1]]


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



if __name__ == "__main__":
    num_list  = []
    num_list+= str(input("Enter numbers (seperated by a space): ")).split(" ")
    num_list = [int(x) for x in num_list] #convert all element into int()

    target = int(input("What is the target? "))


    sk = Skeletons()
    op_combinations = set(itertools.combinations(["+","-","*","/"]*5,5))
    num_list_perms = set(itertools.permutations(num_list,6))
    templates = sk.parse_for_valid_skeletons()


    #Mutli-threading logic
    manager = Manager()
    return_dict = manager.dict()
    #so all threads can acces
    array_size = len(templates)*len(op_combinations)*len(num_list_perms)

    
    processes = []
    global expressions
    expressions = []
    for num in range(7):
        a = Process(target=populate_valid_skeletons,args=(op_combinations,num_list_perms,templates,expressions,[num*6,(num+1)*6]))
        processes.append(a)
        a.start()

#Once complete join results
    for job in processes:
        job.join()


    print("Complete")
    print(len(expressions))
