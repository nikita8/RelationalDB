# Milton Palaguachi
# Database I
# CSC
# If given an attribute and some FDs
# 1. get the correct not trivial FDs
# 2. get keys 
# 3. conputeclosure
# 4. compute FDs to which NF belons: Depencence(FD)->1NF,2NF,3NF, and BCNF
# 5. Check a valid Functional 
# functions:
#  ____________________________________________________________________________________________________________________________________
# | powerset: will breack down a set in all its subsets, this will be use if set >1 and we want to check if its sub set is in some set  |
# | Funtions: Check_FDS_format: check if valid FD                                                                                       |
# | get_FD :  will get the RHS and LHS of an FD                                                                                         |
# | FD_Validation will make sure that there is no repeated FDs, weak FDs, will break down (A->SB) in A->B and A->C                      |
# | closure: will compute a closure of any attribute if there is relatate FD to this attribue                                           |
# | Which_NormalForm: will compute the NF based in the FDs                                                                              |
# | get_keys: computed the keys of set of attribute and its FDs                                                                         |
#  --------------------------------------------------------------------------------------------------------------------------------------
def return_index(value, qlist):# return index else -1
    try:
        idx = qlist.index(value)
    except ValueError:
        idx = -1
    return idx
# remove MVDs if there are already in FDs
def mvds_in_fds(fds_lhs, fds_rhs, mvds_lhs, mvds_rhs):
    mvd_len = len(mvds_lhs)
    x=0
    for i in range(mvd_len):
        if(mvds_lhs[i] in fds_lhs and mvds_rhs[i] in fds_rhs):
            fd_index = fds_rhs.index(mvds_rhs[i])
            print('Triviliaze MVD:',mvds_lhs[i]+'->->'+mvds_rhs[i],'by FD:',fds_lhs[fd_index]+'->'+fds_rhs[fd_index])
            mvds_rhs[i]='-'# temp assignemnt '-' to mvds so that there is no out of range issues
            mvds_lhs[i]='-'
    while(x<mvd_len):
        if('-' in mvds_rhs):
            mvds_lhs.remove('-')
            mvds_rhs.remove('-')
            x = x + 2
        else:
            x = x + 1
    return fds_lhs,fds_rhs,mvds_lhs, mvds_rhs

#check if FDs= 1  or MVDs=2 has a valid=0 
def check_fd_mvd_format(s):
    s_l = len(s)
    #[A][-][>][C] FD >= 4
    if(s_l < 4):
        print("an FD must in this format: 'A->B' or MVD: 'A->->B'")
        return 0
    # Check if X is alphabet and Y is alphabet: X->Y
    # here we check if '-' is fallowed by'>'
    if(not(s[0].isalpha() and s[s_l-1].isalpha())):
        return 0
    for i in range(1,s_l-1):
        if(s[i] == '-' ):
            if(s[i+1]=='>' and s[i-1].isalpha() and s[i+2].isalpha()):
                return 1
            if(s[i+1] == '>' and s[i+2] == '-' and s[i+3] == '>' and s[i-1].isalpha() and s[i+4].isalpha()):
                return 2
        else:
            continue
    return 0
# we compute all subset of s
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1,1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]
#check if seed is in LHS of FDs
def seed_In_Set(seed,lhs):
    all_subset_of_seed =list(powerset(list(seed)))
    seed_list=[]
    for i in all_subset_of_seed:
        listTostr = ''.join(map(str,i))
        seed_list.append(listTostr)
    # we have all subset of seed in seed_list
    for i in seed_list:
        if(i in lhs):
            #if any subset seed matches the lhs will return True
            return True
    return False
# get the LHS and RHS of an MVD 
def get_mvd(s):
    s_l = len(s)
    str_LHS =''
    str_RHS =''
    st= ''
    for i in range(s_l):
        if(i >= s_l-1):#RHS input FD, we are at the end of 's' string so just get RHS
            st += s[i]
            str_RHS = st
        if(s[i] == '-' and s[i+1] == '>' and s[i+2] == '-' and s[i+3] == '>' and i < s_l):#[A][-][>][C]
            i = i+4# if we find [i]='-' and s[i+1]='>' then skip these two indes
            str_LHS = st# LHS=st, we at this i index we know is the end of LHS
            st=''# reset st='' for the RHS to be used
        else:
            if(s[i]== '-' or s[i]=='>'): #if i is '-' or i is '>' do not store
                continue
            else:
                st+= s[i]#LHS input
    #return LHS and RHS of the MVD
    return str_LHS,str_RHS
# get the LHS and RHS of an FD 
def get_fd(s):
    s_l = len(s)
    str_LHS =''
    str_RHS =''
    st= ''
    for i in range(s_l):
        if(i >= s_l-1):#RHS input FD, we are at the end of 's' string so just get RHS
            st+=s[i]
            str_RHS = st
        if(s[i]== '-' and s[i+1]=='>'and i < s_l):#[A][-][>][C]
            i = i+2# if we find [i]='-' and s[i+1]='>' then skip these two indes
            str_LHS = st# LHS=st, we at this i index we know is the end of LHS
            st=''# reset st='' for the RHS to be used
        else:
            if(s[i]== '-' or s[i]=='>'): #if i is '-' or i is '>' do not store
                continue
            else:
                st+= s[i]#LHS input
    #return LHS and RHS of the FD
    return str_LHS,str_RHS

def fds_mvds_validation(LHS_fd,RHS_fd,attr,fd_mvd,arrow):
    rfd=[]
    lfd=[]
    for i in range(len(RHS_fd)):
        str_lhs = LHS_fd[i]
        str_rhs = RHS_fd[i]
        if(len(str_lhs) == 1 and len(str_rhs) == 1):# rhs and lhs == 1
            #check if rhs and lhs is in atribute 
            if(str_rhs in attr and str_lhs in attr):
                # check if not self reflective A->A and are not repeated
                if(str_lhs == str_rhs):
                    print("trivial "+fd_mvd,str_lhs,arrow,str_rhs)
                elif(str_lhs in lfd and str_rhs in rfd): 
                    index_rhs = rfd.index(str_rhs)
                    if(not lfd[index_rhs] == str_lhs ):#check for weak fds
                        print("weak "+fd_mvd+":",lfd[index_rhs]+arrow+str_rhs,"replace by",str_lhs+arrow+str_rhs)
                        lfd[index_rhs] = str_lhs
                    else:
                        print("Already in "+fd_mvd, str_lhs+arrow+str_rhs)
                elif (str_lhs not in lfd or str_rhs not in rfd): 
                    print(str_lhs,arrow,str_rhs)
                    rfd.append(str_rhs)
                    lfd.append(str_lhs)
                else:
                    continue
            else:
                if(str_lhs not in attr):
                    print(str_lhs,'not in Atrribute:',attr)
                if(str_rhs not in attr):
                    print(str_rhs,'not in Atrribute:',attr)

        #make sure rhs or lhs length is < attr length and > 1
        if((len(str_rhs) < len(attr) and len(str_rhs) > 1 ) or (len(str_lhs) < len(attr) and len(str_lhs) > 1)):
            # print(str_lhs,',',str_rhs)# sort lhs and rhs of FDs
            str_rhs = sorted(str_rhs)
            str_lhs = sorted(str_lhs)
            st_tp=''
            for i in str_lhs:
                st_tp += i
            str_lhs = st_tp # put back sorted LHS as one string since we don need break a part
            bool1 = True
            bool2 = True
            # Here in following for loops we check that both rhs and lhs are in atribute
            # RHS = str_rhs and attribute = attr
            for i in str_rhs:# check if RHS is in attribute
                if not(i in attr):
                    bool1 = False
                    print(i,'not in Atrribute:',attr)
            for i in str_lhs:# chen if LHS is in atrribute
                if not(i in attr):
                    bool2 = False
                    print(i,'not in Atrribute:',attr)
            len_str_rhs = len(str_rhs)# we need only rhs to break down to standar nontrivial form
            x=0
            if(bool1  and bool2): # if both are in attribute
                while(x < len_str_rhs):
                    # if alread exist do not add
                    # if lhs != rhs add FD's
                    if(str_lhs in lfd and str_rhs[x] in rfd and str_rhs[x] not in str_lhs):
                        print("Already in "+fd_mvd,str_lhs+arrow+str_rhs[x])
                    if( not str_lhs == str_rhs[x] and str_rhs[x] not in rfd and str_rhs[x] not in str_lhs):
                        rfd.append(str_rhs[x]) # add RHS
                        lfd.append(str_lhs)    # add LHS
                    x = x + 1
    #return LHS and RHS lists
    return lfd,rfd
#The sort_Item will be used to sort the clouser and return as one single string
def sort_Item(cl):
    tp_c= sorted(cl)
    tp_s=''
    for i in tp_c:
         tp_s += i
    return tp_s
#The following will be use in the clouser function
def closure(lhs,rhs,seed,attr):
    cl_result = ''
    print('seed: ',seed)
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
#the following check if 'i' an attribute is in lhs or part of lhs
def isAttributeInFD(i,lhs):
    for item in lhs:
        if(len(item) > 1):# ex. i= A !=AB(item of lhs) so breack down if len(item) > 1 
            for j in item:
                if(i in j):
                    return True
    return False
def get_keys(attr,lhs,rhs):
    part_Of_Key=''
    pos_keys=[]
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
def Which_NormalForm(keys,lhs,rhs):
    keys_subset=[]
    for k in keys:
        sub_k = list(powerset(list(k)))
        for m in sub_k:
            str_m=''.join(map(str,m))
            keys_subset.append(str_m)
    # print(keys_subset)
    bool3NF=[]
    boolBCNF=[]
    for i in range(len(lhs)):
        boolBCNF.append(False)
        bool3NF.append(False)
    #will go in the loop if key are on 3NF or BCNF
    if(len(keys) == len(lhs)):
        for i in range(len(lhs)):
            if(lhs[i] in keys_subset and rhs[i] in keys_subset): #3NF
                bool3NF[i] = True
            if(lhs[i] in keys and rhs[i] not in keys_subset):#BCNF
                boolBCNF[i]=True
        if(False not in bool3NF):
            print("3NF")
            return
        if(False not in boolBCNF):
            print('BCNF')
            return
    for i in range(len(lhs)):
        #it might be sub key of lhs
        #if one lhs attribute is non key attribute we know is in the 1NF. 
        # if its lhs is a sub key or not proper attribute in other words a partial key
        if(lhs[i] not in keys and rhs[i] not in keys and rhs[i] not in keys_subset):# It might be in 1NF
            # print(lhs[i],'->',rhs[i])
            bool2NF= False
            if(lhs[i] in keys_subset):#  X->Y, if X is subkey of any key then it violates 2NF so it must be in 1NF
                print('1NF')
                return
            for n in lhs:
                # X->A of relation R
                # 1. X is a set of attributes in R
                # 2. A is a not-primery attribute non in X
                # Then to be in 2NF,X should not be a proper subset of any key
                if(n in keys and lhs[i] not in keys and rhs[i] not in keys_subset):
                    bool2NF = True
            print('2NF' if bool2NF else '1NF')
            return
def print_mvd_fd(lhs,row,rhs):
    for i in  range(0,len(lhs)):
        print(lhs[i]+row+rhs[i],end =', ')
    print('')
def remove_fd_or_mvd(user_input):
    val= check_fd_mvd_format(str1)# return 1 for FD, 2 for MVD,and 0 wrong input with some comment
    if(val== 1):
        print("FD:",str1)
        key1,val1 = get_fd(str1)
        if(return_index(val1, fds_rhs) >= 0):# found the in RHS
            index_fd = fds_rhs.index(val1)
            if(key1 == fds_lhs[index_fd]):# found the in LHS
                fds_rhs.pop(index_fd)
                fds_lhs.pop(index_fd)
            else:# Not found the in LHS
                print('The LHS FD not found in FDs list')
                print_mvd_fd(fds_lhs,'->',fds_rhs)
        else:# Not found the in RHS
            print('FD not in FDs list')
            print_mvd_fd(fds_lhs,'->',fds_rhs)
    elif(val == 2):
        print("MVD:",str1)
        key1,val1 = get_mvd(str1)
        if(return_index(val1, mvds_rhs) >= 0):#found the in RHS
            index_mvd = mvds_rhs.index(val1)
            if(key1 == mvds_lhs[index_fd]):# found the in LHS
                mvds_rhs.pop(index_fd)
                mvds_lhs.pop(index_fd)
            else:# Not found the in LHS
                print('The LHS MVD not in MVDs list')
                print_mvd_fd(mvds_lhs,'->->',mvds_rhs)
        else:# Not found the in RHS
            print('MVD not in MVDs list')
            print_mvd_fd(mvds_lhs,'->->',mvds_rhs)
    else:
        # print("wrong input,try again",str1)
        return 0
    if not(val == 0):
        return 1
#======================================
# My format
#  FDs
# fds_lhs=[]
# fds_rhs=[]
#  MVDs
# mvds_lhs=[]
# mvds_rhs=[]
# attribute = 'ABCDRSD'
#======================================
# attr1 = input("Enter atributes ") 
# if not (attr1.isalpha()):
#     print('Attribute must be an alphabet type')
#     exit()
# print(attr1)
fds_lhs=[]
fds_rhs=[]
mvds_lhs=[]
mvds_rhs=[]
closure_result=''
#################ENTER MVDs and FDs###############################
# while(True):
#     str1 = input('Enter FD or MVD  or "done" to finished \n' )
#     if(str1 == 'done'):
#         break # exit the while loop
val= check_fd_mvd_format(str1)# return 1 for FD, 2 for MVD,and 0 wrong input with some comment
    # if(val== 1):
    #     print("FD:",str1)
key1,val1 = get_fd(str1)
fds_lhs.append(key1)
fds_rhs.append(val1)
    # elif(val == 2):
    #     print("MVD",str1)
key1,val1 = get_mvd(str1)
mvds_lhs.append(key1)
mvds_rhs.append(val1)
    # else:
    #     print("wrong input, try again",str1)
   
##########################Validata MVD and FDs####################
fds_lhs,fds_rhs = fds_mvds_validation(fds_lhs,fds_rhs,attr1,"FD", "->")
mvds_lhs,mvds_rhs = fds_mvds_validation(mvds_lhs,mvds_rhs,attr1,"MVD", '->->')
if (not fds_lhs or not mvds_lhs ):
    print('Since non FDs are valid,the program will terminate, Bye')
    exit()

######################### remove MVDs if there are already in FDs########
fds_lhs,fds_rhs, mvds_lhs, mvds_rhs = mvds_in_fds(fds_lhs, fds_rhs, mvds_lhs, mvds_rhs)
##########################Print FDs and MVDs###################
print_mvd_fd(fds_lhs,'->',fds_rhs)
print_mvd_fd(mvds_lhs,'->->',mvds_rhs)

#####################Remove FDs or MVDs#######################
# while(True):
    # usert_input = input('Would you like to remove an FD or MVD\nThen enter FD or MVD to be removed\n or enter "done" to finished removing\n...')
    # if(str1 == 'done'):
        # break # exit the while loop
    # return 1 if valid input Format(FD or MVD): however if does not match FD or MVD or will print a massage
    # return 0 wrong input
val =  remove_fd_or_mvd(unser_input)
    
##########################Print FDs and MVDs###################
# print_mvd_fd(fds_lhs,'->',fds_rhs)
# print_mvd_fd(mvds_lhs,'->->',mvds_rhs)
#################Copute clousere of Seed#################################
# while(True):
#     seed = input('Enter seed to compute closure or "quit" to exit program: ')
#     if(seed.isalpha()):
#         if(seed== 'quit'):
#             break#finish program
#         else:
            # closure_result = closure(attr1, str1, LHS_fd, RHS_fd)
            # closure_result = closure(LHS_fd, RHS_fd, str1, attr1)
            # print(closure_result)
print(' {',seed,'}^+ :',closure(fds_lhs, fds_rhs, seed, attr1))
    # else:
        # continue# continue going through loop
# print("we will compute the key of FDs")
list_keys=[]   
#The following command will find keys
attr= sort_Item(attr1)# we sort attribute to compare with possible key
# in get_key we compute the attr that are not in FDs and that are on the lhs
possible_keys = get_keys(attr,fds_lhs, fds_rhs)

# print('possible keys: ',possible_keys)
# in the for loop we parse those possible keys and compute the closure
#if the closure== attr then we know is a key
# for i in possible_keys:
    # key_closure = closure(attr,i,LHS_fd,RHS_fd)
key_closure = closure(fds_lhs, fds_rhs, i, attr)
    #check if key_closure is equal to attr
key_closure = sort_Item(key_closure)#  so is ABC... and not CAB..
    # print(' {',i,'}^+ =',key_closure)
    # if a clousere(seed) == to attribue we know that it is a key
if(key_closure == attr):
    list_keys.append(i)
# if(list_keys):
#     print('key(s) ',list_keys)
Which_NormalForm(list_keys,fds_lhs, fds_rhs)









