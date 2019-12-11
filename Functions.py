"""
this file contains some examples of Shame/Align functions
"""

'''
standard bool function is by float range
'''
def make_func_bool_standard(minVal, maxVal):
    return lambda x: True if x >= minVal and x <= maxVal else False

'''
standard float function is by direct mapping
'''
def make_func_float_standard():
    return lambda x: x

'''
float function that takes into account threshold,
will output x only if x is found within threshold
'''
def make_func_float_by_threshold_standard(minVal, maxVal):
    return lambda x: x if x >= minVal and x <= maxVal else 0

'''
same as above, except adds a weight to lambda function.
'''
def make_func_float_by_threshold_weighted(minVal, maxVal, weight):
    return lambda x: weight * x if x >= minVal and x <= maxVal else 0

def make_func_float_by_threshold_standard(minVal, maxVal):
    return lambda x: x if x >= minVal and x <= maxVal else 0

def make_func_float_by_threshold_with_apply(minVal, maxVal, applyFunc):
    return lambda x: applyFunc(x) if x >= minVal and x <= maxVal else 0

"""
description:
-

arguments:
- minVal := float, minimum qualifying value for activation
- maxVal := float, maximum qualifying value for activation
- k := float,
- setCap := bool, if output limit is 1.0
"""
def multiplier_function(minVal, maxVal, k, setCap = True):
    assert k >= 0, "k {} invalid".format(k)
    if setCap:
        return lambda x : min(x * k, 1.0) if x >= minVal and x <= maxVal else 0
    return lambda x : x * k if x >= minVal and x <= maxVal else 0

def exponential_function_restricted(minVal, maxVal, k):
    assert type(k) is int and k >= 0 , "k {} invalid".format(k)
    return lambda x : x ** k if x >= minVal and x <= maxVal else 0

# alternative shame function can take into account other ratio values
# ex. : ratio of x(shame)/x(align), in which x is a function.
