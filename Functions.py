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
