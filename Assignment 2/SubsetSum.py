# CMPE 365 Assignment 2: Subset Sum
# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.
import copy
import math
import random

class Set:
    def __init__(self, element_array=[]):
        self.elements = list(element_array)
        self.sum = sum(self.elements)

    def add_elements(self, element_array):
        for element in element_array:
            self.elements.append(element)
        self.sum = sum(self.elements)
    
    def __len__(self):
        return len(self.elements)

# Pair sum algorithm, modified to count and return both number of operations and results.
def Pair_Sum(Subsets_1, Subsets_2, k):
    counter = 0
    p1 = 0
    p2 = len(Subsets_2) - 1
    while((p1 < len(Subsets_1)) and (p2 >= 0)):
        counter += 4
        t = Subsets_1[p1].sum + Subsets_2[p2].sum
        if t == k:
            counter = counter - 1
            return [[p1, p2], counter]
        elif t < k:
            p1 = p1 + 1
        else:
            p2 = p2 - 1
    # Did not find any pair that sums to target value return false.
    return [False, counter]

# BFI algorithm modified to return number of operations and result.
def Modified_BFI_Subset_Sum(S, k):
    counter = 0
    subsets = []
    counter += 1
    subsets.append(Set())
    for i in range(len(S)):
        new_subsets = []
        for old_u in subsets:
            new_u = Set(copy.deepcopy(old_u.elements))
            new_u.add_elements([copy.deepcopy(S.elements[i])])
            counter += 4
            if new_u.sum == k:
                # Found a sum in the brute force method, returns that sum as well as number of operations.
                return [counter, True, new_u.elements]
            else:
                counter += 2
                new_subsets.append(old_u)
                new_subsets.append(new_u)
        counter += 1
        subsets = new_subsets
    # Did not find a sum in the brute force method, returns number of operations and all possible subsets.
    return [counter, subsets, False]

def HS_Subset_Sum(S, k):
    # Calculate closest to middle index of given set.
    counter = 1
    if (len(S) % 2 == 0):
        middle_index = (int) (len(S)/2 - 1)
    else:
        middle_index = (int) ((len(S)+1)/2 - 1)
    # Split the set into two halves.
    counter += 2
    S_left = Set(copy.deepcopy(S.elements[0:middle_index + 1]))
    S_right = Set(copy.deepcopy(S.elements[middle_index + 1:]))
    # BFI method on the two resulting halves.
    left_result = Modified_BFI_Subset_Sum(S_left, k)
    right_result = Modified_BFI_Subset_Sum(S_right, k)
    # Add the number of operations that was returned from BFI method.
    counter += left_result[0] + right_result[0]
    Subsets_left = left_result[1]
    Subsets_right = right_result[1]
    counter += 1
    if(Subsets_left == True):
        return left_result[2], counter
    elif(Subsets_right == True):
        return right_result[2], counter  
    else:
        # Sort left and right half sets and count the number of operations required.
        counter += 3*len(Subsets_right)*math.log10(len(Subsets_right))
        Subsets_right.sort(key = lambda x: x.sum)
        counter += 3*len(Subsets_left)*math.log10(len(Subsets_left))
        Subsets_left.sort(key = lambda x: x.sum)
        # Execute pair sum algorithm on the two halves.
        result = Pair_Sum(Subsets_left, Subsets_right, k)
        counter += result[1]
        counter += 1
        if type(result[0]) is bool:
            return False, counter
        else:
            resulting_set = Subsets_left[result[0][0]].elements + Subsets_right[result[0][1]].elements
            return resulting_set, counter

def main():
    # Show that both BFI and HS Subset Sums methods work on the given test set:
    Test_Set = Set([3,5,3,9,18,4,5,6])
    k = 28
    result1 = Modified_BFI_Subset_Sum(Test_Set, k)
    result2, counter = HS_Subset_Sum(Test_Set, k)
    print("Given the set: " + str(Test_Set.elements) + " and target value " + str(k) + ":")
    print("BFI Result: " + str(result1[2]))
    print("HS Result: " + str(result2))

    # Show that both BFI and HS Subset Sums methods work on the given test set:
    Test_Set = Set([6, 12, 8, 12, 6, 9])
    k = 13
    result1 = Modified_BFI_Subset_Sum(Test_Set, k)
    result2, counter = HS_Subset_Sum(Test_Set, k)
    print("Given the set: " + str(Test_Set.elements) + " and target value " + str(k) + ":")
    print("BFI Result: " + str(result1[2]))
    print("HS Result: " + str(result2))

    # Begin tabulating data on the number of steps required by each algorithm:
    BFI_Average_Overall = [0 for k in range(16)]
    HS_Average_Overall = [0 for k in range(16)]
    for n in range(4,16):
        result_BFI = []
        result_HS = []
        BFI_Average_Set = [0 for k in range(21)]
        HS_Average_Set = [0 for k in range(21)]
        for i in range(1, 21):
            S = Set([random.randint(0, 100) for j in range(n)])
            targets = [random.randint(0,1500) for j in range(10)]
            for target in targets:
                current_count = Modified_BFI_Subset_Sum(S, target)
                result_BFI.append(current_count[0])
                current_result, current_count = HS_Subset_Sum(S, target)
                result_HS.append(current_count)
            # Calculate the average number of operations for each test case:
            BFI_Average_Set[i] = sum(result_BFI)/len(result_BFI)
            HS_Average_Set[i] = sum(result_HS)/len(result_HS)
        # Calculate the average number of operations for each value of n:
        BFI_Average_Overall[n] = sum(BFI_Average_Set)/len(BFI_Average_Set)
        HS_Average_Overall[n] = sum(HS_Average_Set)/len(HS_Average_Set)
    # Display resulting arrays so that the data can be graphed:
    print("BFI Operations: " + str(BFI_Average_Overall))
    print("HS Operations: " + str(HS_Average_Overall))

main()