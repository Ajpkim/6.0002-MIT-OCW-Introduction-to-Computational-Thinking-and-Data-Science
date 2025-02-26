###########################
# 6.0002 Problem Set 1b: Space Change
# Name: 
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    
#    Recursive base case
    if target_weight == 0:
        return 0
    
    #If solution for weight has been found return the solution
    elif target_weight in memo:
        return memo[target_weight]
    
#    Recursive case
    else:
        # Tracking the best result for each egg at every target weight
        result = False 
#       Try taking each egg 
        for egg in egg_weights:
#           If egg fits                    
            if egg <= target_weight:
#                Take the egg and find resulting best solution 
                take_egg = 1 + dp_make_weight(egg_weights, (target_weight - egg), memo)
#           If taking the current egg produces best result so far for the target wieght      
            if result == False or result > take_egg:
#               Set result to solution from taking egg
                result = take_egg
#       After checking each egg and the solutions that follow from taking each
#       Add the best solution to the memo... (best solution being minimum number of eggs needed to reach limit)
        memo[target_weight] = result
        
#        Return the result (best solution at target_weight)
        return result



# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()