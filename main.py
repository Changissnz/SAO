from ShameAndObedienceGameBoardTestVariables import * 
from Display import * 

## TO DO
# this is where GameBoard gets run
# make introduction screen
# make input boxes for variables
# add more modes to game. 

"""
description:
- this is where variables get inputted 
"""
def input_vars():
    
    # vars 
    sz = 5 
    ls = 100 
    
    # TODO : add default here
    while True: 
        xElem = input("* number of elements? :\t")
        try: 
            xElem = int(xElem) 
        except: 
            print("value must be integer") 
        
        if xElem > 12 or xElem <= 1: print("cannot do more than 12 or less than 2 elements")
        else: break 
        
    while True:
        scales = input(str("* scale of each language? ##range (0.05,1] for each, separated by space##\t :\t"))  
        b = True 
        
        # parse 
        q = scales.split(" ")
        q = [q_.strip() for q_ in q if q_.strip() != ""] 
        q = [float(q_.strip()) for q_ in q]  
        
        if min(q) <= 0 or max(q) > 1:
            print("invalid values, must be in range (0.05, 1]") 
            b = False 
        if len(q) != xElem: 
            print("incorrect number of scales, want {}, got {}".format(xElem, len(q))) 
            b = False 
        if b:
            scales = q 
            break 
            
    # make the languages 
    languages = [] 
    for i in range(xElem): 
        ms = ceil(ls * scales[i])
        l = Language.random(idn = i, minSizeInfo = ms, startSizeInfo = sz, mode = "const") 
        languages.append(l)
        
    # get type of action function
    while True: 
        af = input("* Action function? exponential (e)  threshold (t)  multiplier (m) :\t").lower() 
        if af in {"e", "t", "m"}: 
            break
    
    # get range
    while True: 
        shameRange = input("* specify shame activation range (minimum, maximum) ##values are in range [0, 1], separated by space##:\t") 
        q = shameRange.split(" ")
        q = [q_.strip() for q_ in q if q_.strip() != ""] 
        if len(q) != 2: 
            print("invalid range, example :\t 0.25 0.75") 
            continue
        try: 
            q[0], q[1] = float(q[0]), float(q[1])
        except: 
            print("invalid range, example :\t 0.25 0.75") 
            continue
        
        if q[0] < 0 or q[1] > 1: 
            print("invalid range, example :\t 0.25 0.75") 
            continue
        
        shameRange = q  
        break 
        
    while True: 
        alignRange = input("* specify align activation range (minimum, maximum) ##values are in range [0, 1], separated by space##:\t")
        q = alignRange.split(" ")
        if len(q) != 2:
            print("invalid range, example :\t 0.25 0.75") 
            continue
        try: 
            q[0], q[1] = float(q[0]), float(q[1]) 
        except: 
            print("invalid range, example :\t 0.25 0.75") 
            continue
        
        if q[0] < 0 or q[1] > 1: 
            print("invalid range, example :\t 0.25 0.75") 
            continue        
        
        alignRange = q 
        break 

    # make the action functions 
    if af == "e": 
        while True: 
            expo = input("* specify exponent [1,5]:\t") 
            try: 
                expo = int(expo) 
            except: 
                print("invalid multiplier, must be a float")
                continue
            if expo > 5 or expo < 1: 
                print("exponent must be in range [1,5]") 
                continue 
            break
        shameFunc = exponential_function_restricted(shameRange[0], shameRange[1], expo)
        alignFunc = exponential_function_restricted(alignRange[0], alignRange[1], expo) 
    elif af == "t": 
        shameFunc = make_func_float_by_threshold_standard(shameRange[0], shameRange[1])
        alignFunc = make_func_float_by_threshold_standard(alignRange[0], alignRange[1])
    else: 
        while True: 
            mult = input("* specify multiplier:\t") 
            try: 
                mult = float(mult) 
            except: 
                print("invalid multiplier, must be a float")
                continue
            break
        shameFunc = multiplier_function(shameRange[0], shameRange[1], mult)
        alignFunc = multiplier_function(alignRange[0], alignRange[1], mult) 
        
    funcInfo = {"shame" : shameFunc, "align" : alignFunc}
    while True: 
        elemAss = input("element assignment? best fit (fit) or test/approximate (t/e)?\t").lower() 
        
        if elemAss not in {"fit", "t/e"}: 
            print("invalid assignment scheme, must be best fit (fit) or test/approximate (t/e)") 
            continue
        break 

    while True: 
        frequency = input("frequency of assignment?\t")        
        try: 
            frequency = int(frequency) 
        except: 
            print("frequency must be integer") 
            continue 
    
        if frequency <= 0:
            print("frequency must be greater than 0") 
            continue 
        break 
            
    gb = ShameAndObedienceGameBoard(languages, (8,8), pixelRes = (1000, 750),\
            assignElementsToRegion = (elemAss, frequency), actionFunctions=funcInfo) 
    return gb

def declare_game(): 
    
    x1 = input("* choice (c) or default (d) ?\t").lower()
    if x1 not in {"c", "d"}: 
        declare_game()
    elif x1 == "d": 
        gb = ShameAndObedienceGameBoardTestVariables.sample_gameboard1(assignElementsToRegion=("fit", 5)) 
    else: 
        gb = input_vars()
        
    dg = DisplayGameboard(gb)
    dg.init_screen()
    dg.run_loop()
    
declare_game() 