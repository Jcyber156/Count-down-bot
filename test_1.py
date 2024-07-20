import itertools

#kiled due to memory
#Brute force may not work. Try an UB,LB aproach and then BF??


operations = ["+","+","+","+","+","+","-","-","-","-","-","-","*","*","*","*","*","*","/","/","/","/","/","/",]
def powerset(numbers,operations):
    #get combos
    powerset = []
    combined = numbers + operations
    for r in range(3,31):
        powerset.append(list(itertools.combinations(combined,r)))

    with open("powerset.txt","r") as f:
        for i in powerset:
            f.write(i)

print(powerset([1,2,3,4,5],operations))

