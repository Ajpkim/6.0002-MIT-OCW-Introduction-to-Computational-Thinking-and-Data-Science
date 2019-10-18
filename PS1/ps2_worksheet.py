# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 16:25:33 2019

@author: alexk
"""

#Pytutor Visualize Test Code

counter = 0

def dp_make_weight(egg_weights, target_weight, memo = {}):

    global counter
    counter += 1

    if counter == 100:
        raise ValueError
        
    if target_weight == 0:
        return 0
    
    #If solution for weight has been found return the solution
    elif target_weight in memo:
        return memo[target_weight]
        
    
#    Recursive case
    else:
        
        result = False 
        
#       Try taking each egg 
        for egg in egg_weights:
             
#           capacity, considering = target_weight, egg
                    
            if egg <= target_weight:
                
                take_egg = 1 + dp_make_weight(egg_weights, (target_weight - egg), memo)
                
            if result == False or result > take_egg:
          
                result = take_egg
                
        memo[target_weight] = result
        
        return result


egg_weights = (1, 3, 5)
target_weight = 5
print (dp_make_weight(egg_weights, target_weight, memo={}))