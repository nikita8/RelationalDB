def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1,1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]
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
    
    if(len(keys) == len(rhs)):
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
    else:
        return False
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
    
    normalForm = ""
    if(checkBCNF(keys,lhs,rhs) == True):
        normalForm = "BCNF"
    elif(check3nf(keys,lhs,rhs) == True):
        normalForm = "3NF"
    elif(check1Nf(keys,lhs,rhs) == True):
        normalForm = "1NF"
    else:
        normalForm = "2NF"
    return normalForm
#3NF
# attr1= ['AB', 'BC', 'CD','AD']
# lhs=['AB', 'BC', 'CD','AD']
# rhs=['C', 'D','A','B']
#BCNF
# attr1= ['AB']
# lhs=['AB']
# rhs=['C']
#1NF
# attr1= ['AB']
# lhs=['B','B']
# rhs=['C','D']
# #1NF
# attr1= ['AF']
# lhs=['A','B','C','F']
# rhs=['B','C','D','E']
attr1= ['A','AB']
lhs=['A','B','AB']
rhs=['B','C','C']


for i in range(len(lhs)):
    print(lhs[i],"->",rhs[i])

print(Which_NormalForm(attr1,lhs,rhs))
which_normal_form(attr1,lhs,rhs)
