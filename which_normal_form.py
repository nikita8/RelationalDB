from input_fds_mvds import *
def sort_Item(cl):
    tp_c= sorted(cl)
    tp_s=''
    for i in tp_c:
         tp_s += i
    return tp_s

# def powerset(s):
#     x = len(s)
#     masks = [1 << i for i in range(x)]
#     for i in range(1,1 << x):
#         yield [ss for mask, ss in zip(masks, s) if i & mask]
def check_equal(lhsAttrs,keyAttrs):
    isNotKey = False
    if(lhsAttrs != keyAttrs):
        isNotKey = True
    return isNotKey

def checkBCNF(keys,lhs,rhs):
    keyAttrs = []
    boolBCNF = []
    for i in range(len(lhs)):
        boolBCNF.append(False)
    # for the 3NF all the lhs must be key and rhs subkey
        #check all the lhs must be key
    for i in lhs:
        if(i not in keys):
            return False # one of the lhs not part of the key
    for k in keys:
        keyAttrs.extend(list([char for char in k]))
    for r in range(len(rhs)):
        if(rhs[r] not in keyAttrs):# rhs must be non key attribute for BCNF 
            boolBCNF[r]= True
    if(False in boolBCNF):# if there is one rhs fd that key is  than no BCNF
        return False 
    else:
        return True
    return False

def check3nf(keys,lhs,rhs):
    keyAttrs = []
    # for the 3NF all the lhs must be key and rhs subkey
    if(len(keys) == len(rhs)):
        #check all the lhs must be key
        for i in lhs:
            if(i not in keys):
                return False # one of the lhs not part of the key
        for k in keys:
            keyAttrs.extend(list([char for char in k]))
        for r in rhs:
            if(r not in keyAttrs):# rhs must be part of keys: subkeys
                return False
        return True# it pass all the test return true: 3NF
    else:
        return False
  
def check1Nf(keys,lhs,rhs):
    keys_subset=[]
    for k in keys:
        sub_k = list(powerset(list(k)))
        for m in sub_k:
            str_m=''.join(map(str,m))
            keys_subset.append(str_m)
    # print(keys_subset)

    for i in range(len(lhs)):
        #it might be sub key of lhs
        #if one lhs attribute is non key attribute we know is in the 1NF. 
        # if its lhs is a sub key or not proper attribute in other words a partial key
        if(lhs[i] not in keys and rhs[i] not in keys and rhs[i] not in keys_subset):# It might be in 1NF
            # print(lhs[i],'->',rhs[i])
            bool2NF= False
            if(lhs[i] in keys):#  X->Y, if X is subkey of any key then it violates 2NF so it must be in 1NF
                # print('1NF')
                return True
            for n in lhs:
                # X->A of relation R
                # 1. X is a set of attributes in R
                # 2. A is a not-primery attribute non in X
                # Then to be in 2NF,X should not be a proper subset of any key
                if(n in keys and lhs[i] not in keys and rhs[i] not in keys_subset):
                    bool2NF = True
            # print('2NF' if bool2NF else '1NF')
            return(False if bool2NF else True)

def Which_NormalForm(keys,lhs,rhs):
    normalForm ="BCNF"
    if(len(lhs) == 0):
        return normalForm
    if(checkBCNF(keys,lhs,rhs) == True):
        normalForm = "BCNF"
    elif(check3nf(keys,lhs,rhs) == True):
        normalForm = "3NF"
    elif(check1Nf(keys,lhs,rhs) == True):
        normalForm = "1NF"
    else:
        normalForm = "2NF"
    return normalForm

def decompose_1NF_2NF(keys,lhs,rhs):
    keys_subset =[]
    decomp_keys =[]
    lhs_tmp =lhs
    rhs_tmp =rhs

    str_tmp=''
    for k in keys:
        sub_k = list(powerset(list(k)))
        for m in sub_k:
            str_m=''.join(map(str,m))
            keys_subset.append(str_m)
    # print(keys_subset)

    for i in range(len(lhs)):
        #it might be sub key of lhs
        #if one lhs attribute is non key attribute we know is in the 1NF. 
        # if its lhs is a sub key or not proper attribute in other words a partial key
        if(lhs[i] not in keys and rhs[i] not in keys and rhs[i] not in keys_subset):# It might be in 1NF
            # print(lhs[i],'->',rhs[i])
            bool2NF= False
            if(lhs[i] in keys):#  X->Y, if X is subkey of any key then it violates 2NF so it must be in 1NF
                
                print('1NF',lhs[i],'->',rhs[i])
                # call decompose

                return True
            for n in lhs:
                # X->A of relation R
                # 1. X is a set of attributes in R
                # 2. A is a not-primery attribute non in X
                # Then to be in 2NF,X should not be a proper subset of any key
                if(n in keys and lhs[i] not in keys and rhs[i] not in keys_subset):

                    bool2NF = True
                    print('Decomposition:')
                    print(lhs[i] ,'->',rhs[i])
                    str_tmp +=lhs
                    str_tmp +=rhs
                    decomp_keys.append(str_tmp)
            # print('2NF' if bool2NF else '1NF')
            return(False if bool2NF else True)

#the following check if 'i' an attribute is in lhs or part of lhs
def isAttributeInFD(i,lhs):
    for item in lhs:
        if(len(item) > 1):# ex. i= A !=AB(item of lhs) so breack down if len(item) > 1 
            for j in item:
                if(i in j):
                    return True
    return False
def get_pos_keys(attr,lhs,rhs):
    part_Of_Key=''
    pos_keys=[]
    if(len(lhs) == 0):
        return attr
    #Case 1. get the attributes that are not in FDs
    for i in attr:
        if(i in lhs or i in rhs):#if a single attr is lhs or rhs then it will not be part of all keys
            continue
        elif(i not in lhs):# only check the lhs since it can have more than 1 attr in lhs
            if(not isAttributeInFD(i,lhs)):# this method will break down a indivudal lhs and compare to single attr
                # if it can not find will add to partofKey
                part_Of_Key += i
        else:
            part_Of_Key += i# must be part to key if no in LHS or RHS 
    # Case 2. There is an An Atribute on one lhs and not in all rhs or the rest of lhs FDs.
    #        so this attribute will be part of key
    lhs_key = ''
    for i in lhs:
        if(len(i) > 1):
            for j in i:#check every single atrr on lhs
                if(j not in lhs and j not in rhs):
                    lhs_key += j
    # add all the lhs + attr that is not in FDS as part of possible key
    for i in lhs:
        get_key = part_Of_Key + i
        if(lhs_key in i):
            #if not in keys list add
            if not (get_key in pos_keys):
                pos_keys.append(get_key)
        else:
            get_key += lhs_key
            #if not in keys list add
            if not (get_key in pos_keys):
                pos_keys.append(get_key)
    
    return pos_keys

#The following will be use in the clouser function
def closure(lhs,rhs,seed,attr):
    cl_result = ''
    # print('seed: ',seed)
    if(seed in lhs):
        cl_result += seed
        x= lhs.index(seed)
        while(x <len(lhs)):
            if(len(cl_result) >= len(attr)):
                return cl_result
            tp = sort_Item(cl_result)#sort result
            cl_result = tp # put back in clouser result
                # check if LHS[i] is in clouser_result and RHS[i] is not already in clouser
            if(lhs[x] in cl_result and rhs[x] not in cl_result):
                cl_result += rhs[x]
            x= x + 1
        if(len(cl_result) < len(attr)):#let's check to see if I miss something
            # print("check one last time1")
            seed= cl_result# seed is result
            all_subset_of_seed =list(powerset(list(seed)))
            seed_list=[]
            for i in all_subset_of_seed:
                listTostr = ''.join(map(str,i))
                seed_list.append(sort_Item(listTostr))
                # we have all subset of seed in seed_list
            for i in seed_list:
                if(i in lhs): 
                    x = lhs.index(i)
                    if(rhs[x] not in cl_result):
                        cl_result +=rhs[x]
                    while(x <len(lhs)):
                        if(len(cl_result) >= len(attr)):
                            return cl_result
                            # check if LHS[i] is in clouser_result and RHS[i] is not already in clouser
                        if(lhs[x] in cl_result and rhs[x] not in cl_result):
                            cl_result += rhs[x]
                        x= x + 1 
    else:
        cl_result+=seed
        all_subset_of_seed =list(powerset(list(seed)))
        seed_list=[]
        for i in all_subset_of_seed:
            listTostr = ''.join(map(str,i))
            seed_list.append(listTostr)
            # we have all subset of seed in seed_list
        for i in seed_list:
            if(i in lhs):
                if(i not in cl_result):
                    cl_result +=i
                x = lhs.index(i)
                while(x <len(lhs)):
                    if(len(cl_result) >= len(attr)):
                        return cl_result
                    tp = sort_Item(cl_result)#sort result
                    cl_result = tp # put back in clouser result
                        # check if LHS[i] is in clouser_result and RHS[i] is not already in clouser
                    if(lhs[x] in cl_result and rhs[x] not in cl_result):
                       cl_result += rhs[x]
                    x= x + 1          
        if(len(cl_result) < len(attr)):#let's check to see if I miss something
            # print("check one last time2")
            seed = cl_result# seed is result
            all_subset_of_seed =list(powerset(list(seed)))
            seed_list=[]
            for i in all_subset_of_seed:
                listTostr = ''.join(map(str,i))
                # seed_list.append(listTostr)
                seed_list.append(sort_Item(listTostr))
                # we have all subset of seed in seed_list
            # print(seed_list)
            for i in seed_list:
                if(i in lhs):
                    x = lhs.index(i)
                    if(rhs[x] not in cl_result):
                        # print(x,rhs[x],i)
                        cl_result +=rhs[x]
                    while(x <len(lhs)):
                        if(len(cl_result) >= len(attr)):
                            return cl_result
                            # check if LHS[i] is in clouser_result and RHS[i] is not already in clouser
                        if(lhs[x] in cl_result and rhs[x] not in cl_result):
                            cl_result += rhs[x]
                        x= x + 1  
    
    return cl_result #before returning
def get_keys(fds_lhs,fds_rhs,attr):
    list_keys=[]
    if(len(fds_lhs) == 0):
        return attr
    # for i in range(len(fds_lhs)):
    #     print(fds_lhs[i],"->",fds_rhs[i])
    possible_keys = get_pos_keys(attr,fds_lhs,fds_rhs)
    # print('possible keys: ',possible_keys)
    # in the for loop we parse those possible keys and compute the closure
    #if the closure== attr then we know is a key
    for i in possible_keys:
        # key_closure = closure(attr,i,LHS_fd,RHS_fd)
        key_closure = closure(fds_lhs, fds_rhs, i, attr)
        #check if key_closure is equal to attr
        key_closure = sort_Item(key_closure)#  so is ABC... and not CAB..
        # print(' {',i,'}^+ =',key_closure)
        # if a clousere(seed) == to attribue we know that it is a key
        if(key_closure == attr):
            list_keys.append(i)
    return list_keys

