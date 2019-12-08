import re



def input_data():
    
    return input_table_name(dic_para)
   
def input_table_name(dic_para):
    table_name=input("Enter name of the table:")
    if(len(table_name) > 0):
        input_attrs(table_name,dic_para)
    else:
        print("Table name should not be blank")
        p = input("Enter continue to re-enter table name:")
        if(p.casefold() == 'continue'):
            input_data()
        else:
            return
dic_para = {}

def input_attrs(table_name,dic_para):
    attr_input = ''
    num_attr=0
    attr = {}

    while num_attr < 4:
        attr_input = input("Enter Attribute name or Type quit (Attribute name must be a single character):")
         
        if( len(attr_input) == 1):
            
            add_input_type = True
            while(add_input_type):
                attr_input_type = get_attr_input_type()
                
                if(attr_input_type.casefold() == 'string' or attr_input_type.casefold() == 'int'):
                    add_input_type = False
                    attr.update({attr_input.upper():attr_input_type.casefold()})
                else:
                    print("Attribute type must be string or int")
                    
            num_attr+=1
        else:
            if(attr_input.casefold() == 'quit'):
                break
            else:
                if(len(attr_input) > 1):
                    print("Attribute length is greater than 1")
                else:
                    print("Attribute name must not be blank")
        
    tab_name_para = {}
    tab_name_para.update({'attr':attr})
        
    dic_para.update({table_name:tab_name_para})
    
    bool_str = []
    bool_array = []
    
    print("Type list of constraints / Type 'quit' to exit:")
    input_boolean_cons(table_name,dic_para,bool_str,bool_array)


def get_attr_input_type():
    attr_input_type = input("Enter type of attribute you entered(Attribute type should be string or int):")
    return attr_input_type
    
key_dic = {}
def input_boolean_cons(table_name,dic_para,bool_str,bool_array):
    
   
    bool_str = ""
    cons = input()    
    if(cons.casefold() != 'quit'):
        # bool_str.append(cons.upper())
        bool_str = cons.upper()
        bool_array = list(filter(None, bool_array))
        valid_cons = check_bool_constraint(bool_str,table_name,bool_array)
        if(valid_cons):
            bool_array.append(bool_str)
        input_boolean_cons(table_name,dic_para,bool_str,bool_array)
    else:
        conflict_array=[]
        print("Checking for conflicting Boolean conditions...")
        conflict_array = check_bool_conflict(bool_array)
        if(len(conflict_array) > 0):
            print('Following are the conflict boolean contraints list:')
            print(conflict_array)
            print("removing those from boolean constraints list...")
            for i in conflict_array:
                bool_array.remove(i)
        else:
            print('There is no conflicting boolean constraints.')    
        if(len(bool_array) == 0):
            print("All the given boolean constraints are conflicting.")
            print("No boolean Constraint is added in list...")
        dic_para.get(table_name).update({'boolean_cons':bool_array})
        print("dic_para::",dic_para)
        fds = []
        print("Type list of FD's / Type 'quit' to exit:")
        input_fd(table_name,dic_para,fds)

    
def input_fd(table_name,dic_para,fds):
    fd = input()    
    if(fd.casefold() != 'quit'):
        fds.append(fd.upper())
        input_fd(table_name,dic_para,fds)
    else:
        
        ask_to_remove_fd(fds,table_name,dic_para)
        
        
def ask_to_remove_fd(fds,table_name,dic_para):
    c = input("Do you want to remove any Functional Dependency (Yes/No):")
    if(c.casefold() == 'yes'):
        remove_fd(fds,table_name,dic_para)
    else:
        print("Final FDS:::",fds)
        keys_list = get_fd_keys(table_name,fds)
        normalForm = get_nf(table_name,fds)
        # check_all_fds(fds,table_name,dic_para)
        dic_para.get(table_name).update({'FD':fds})
        dic_para.get(table_name).update({'Keys':keys_list})
        print("NormalForm::",normalForm)
        
        forgn_cons=[]
        print("Enter Foreign Constraint:-")
        print("Enter as 'column name:table name' (eg- A:ABC) / Type quit to exit:")
        
        input_foreign_constraints(table_name,dic_para,forgn_cons)

        # print("Type list of MVD's / Type 'quit' to exit:")
        # mvds = []
        # input_mvd(table_name,dic_para,mvds)
        
def get_nf(table_name,fds):
    lhs=[]
    rhs=[]
    attr=[]
    for fd in fds:
        fd_split = fd.split("->")
        lhs.append(fd_split[0])
        rhs.append(fd_split[1])
    for i in dic_para.get(table_name).get('attr').keys():
        attr.append(i)
    keys_list = get_keys(attr,lhs,rhs)

    return Which_NormalForm(keys_list,lhs,rhs)
def get_fd_keys(table_name,fds):
    lhs=[]
    rhs=[]
    attr=[]
    for fd in fds:
        fd_split = fd.split("->")
        lhs.append(fd_split[0])
        rhs.append(fd_split[1])
    for i in dic_para.get(table_name).get('attr').keys():
        attr.append(i)
    keys_list = get_keys(attr,lhs,rhs)
    return keys_list

# def check_all_fds(fds,table_name,dic_para):
#     # check_conflict_fd(fds,table_name,dic_para)


        
def remove_fd(fds,table_name,dic_para):
    remove_fd = input('Enter functional Dependency to remove')
    
    if(remove_fd.upper() in fds):
        fds.remove(remove_fd.upper())
        ask_to_remove_fd(fds,table_name,dic_para)
    else:
        print('Entered fd not exists')
        ask_to_remove_fd(fds,table_name,dic_para)
        
def input_mvd(table_name,dic_para,mvds):
    mvd = input()    
    if(mvd.casefold() != 'quit'):
        mvds.append(mvd.upper())
        input_mvd(table_name,dic_para,mvds)
    else:
        dic_para.get(table_name).update({'MVD':mvds})
        print("update-mvd::",dic_para)    
        key_dic = find_keys(table_name,dic_para)
        ask_to_add_table()
    
def ask_to_add_table():
    print('key_dic::',key_dic)
    c = input("Do you want to enter new table (Yes/No):")
    if(c.casefold() == 'yes'):
        input_data()
    else:
        ask_for_keys()
        
def ask_for_keys():
    tname = input("Enter table name to enter keys of particular table / Enter 'quit' to exit:")
    if(len(tname) > 0):
        if(tname.casefold() != 'quit'):
            
            key = input('Enter key for table: ')
            check_table_key(tname,key)
    else:
        print("Table name should not be blank")

def check_table_key(table_name,key):
    if(key.upper() in dic_para.get(table_name).get('Keys')):
        print("Key found")
    else:
        print('Key must be from ',dic_para.get(table_name).get('Keys'))
        ask_for_keys()

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

def checkBcnf(keys,lhs):
    bcnf = True;
    count = 0;
    

    for l in lhs:
        print("l in keys::",(l in keys))
        print("l:::",l)
        print("keys::",keys)
        if(l not in keys):
            count+=1
            break
    print("COUTN:::",count)
    if count > 0:
        bcnf = False
       
  
    return bcnf

def split_key(key): 
    return [char for char in word]

def check3nf(keys,rhs):
    is3Nf = False;
    count = 0;
    keyAttrs = [];
    
    for k in keys:
        keyAttrs.extend(list([char for char in k]))
    
   

    for r in rhs:
        if(r in keyAttrs):
            count+=1
            break

    if(count > 0):
        is3Nf = True        
            
    return is3Nf;


    
def check1Nf(keys,lhs,rhs):
    is1Nf = False
    isNotKey = False
    keyAttrs=[]

    for k in keys:
        for l in range(len(lhs)):
            keyAttrs.append([char for char in k])
            lhsAttrs = []
            keyAttrs = []
            lhsAttrs.append([char for char in lhs[l]])
           
            isNotKey = check_equal(lhsAttrs,keyAttrs)
            list(filter(lambda x: x not in keyAttrs,lhsAttrs))
            
            if((isNotKey == True) and (not lhsAttrs) and (isRhsPartialKey(rhs[l],keys) == False)):
                is1Nf = True
                break
        if(is1Nf):
            break
    return is1Nf

def check_equal(lhsAttrs,keyAttrs):
    isNotKey = False
    if(lhsAttrs != keyAttrs):
        isNotKey = True
    return isNotKey


def isRhsPartialKey(rhs,keys):
    rhsKeyAttr = False;
    rhsAttrs = []
    for k in keys:
        for r in rhs:
            if(r in k):
                rhsKeyAttr = True
                break
        
    return rhsKeyAttr
def Which_NormalForm(keys,lhs,rhs):
    print("Keys::",keys)
    print("LHS::",lhs)
    print("RHS:::",rhs)
    normalForm = ""
    if (checkBcnf(keys,lhs) == True):
        normalForm = "BCNF";
    elif(check3nf(keys,rhs) == True):
        normalForm = "3NF";
    elif(check1Nf(keys,lhs,rhs) == True):
        normalForm = "1NF";
    else:
        normalForm = "2NF";
    

    return normalForm

def find_keys(table_name,dic_para):
    key_dic.update({'abc':{'keys':'A'}})
    return key_dic
    


def str_split(word): 
    return [char for char in word] 
    
def check_bool_constraint(bool_str,table_name,bool_array):
    valid_cons = False
    bool_split = []
    table_attr = []
    for i in dic_para.get(table_name).get('attr').keys():
        table_attr.append(i)
   
    if(bool_str[0] in table_attr):
        bool_split = re.split('\W+',bool_str)
     
        if((len(bool_split)==2)):
            if((len(re.findall('\W+',bool_str)) > 0) and (len(bool_split[0]) > 0) and (len(bool_split[1]) > 0) ):
                bool_attr = bool_split[0]
                bool_op = re.findall('\W+',bool_str)[0]
                bool_val = bool_split[1]
          
                valid_cons = check_non_std_constraint(bool_str,table_name,bool_array,bool_attr,bool_op,bool_val)
            else:
                print("Violating boolean constraint:",bool_str)
                print("It must be as 'attr op val' eg:(A>10).")
                print("Add another boolean constraint:")
        else:
            print("Violating boolean constraint:",bool_str)
            print("It must be as 'attr op val' eg:(A>10).")
            print("Add another boolean constraint:")
    else:
        print("Given Boolean contraint attribute is not valid")
        print("Boolean Constraint attribute must be from ",table_attr)
        print("Add another boolean constraint:")
   

    return valid_cons
   
def check_non_std_constraint(bool_str,table_name,bool_array,bool_attr,bool_op,bool_val):
   
    valid_cons = False
    if(dic_para.get(table_name).get('attr').get(bool_attr) == 'string'):
       
        if(bool_op not in ['==','<>']):
            print("Violating Non standard boolean constraint:",bool_str)
            print("attribute '",bool_attr,"' is type 'string' (operand must be '==' or '<>')")
            print("add another boolean constraint:")
        else:
            valid_cons = True
    elif(dic_para.get(table_name).get('attr').get(bool_attr) == 'int'):
            
        if(bool_op not in ['==','<>','>','>=','<','<=']):
            print("Violating Non standard boolean constraint:",bool_str)
            print("attribute '",bool_attr,"' is type 'string' (operand must be '==' or '<>' or '>' or '>=' or '<' or '<=')")
            print("add another boolean constraint:")
        else:
            valid_cons = True
    
    return valid_cons  
    

def check_bool_conflict(bool_array):
    bool_attr = []
    bool_op = []
    bool_val = []
    conflict_array = []
    done_arr=[]
    attr = list([x[0] for x in bool_array])
    
    for i in range(len(bool_array)):
        add_cons_to_conflict = False
        
        if(bool_array[i] not in conflict_array):
            for x in range(len(bool_array)):
                
                if(x != i):
                    
                    if(bool_array[i][0] == bool_array[x][0]):
                        bool_split_i = re.split('\W+',bool_array[i])
                        bool_split_x = re.split('\W+',bool_array[x])
                        bool_op_i = re.findall('\W+',bool_array[i])
                        bool_op_x = re.findall('\W+',bool_array[x])
                
                        if(np.array_equal(bool_op_i,bool_op_x)):
                            if(bool_split_i[1] == bool_split_x[1]):
                                print('Two same value',bool_array[i],'and',bool_array[x])
                                add_cons_to_conflict = True
                
                            else:
                
                                print("Same attribute dont have different value",bool_array[i],'and',bool_array[x])
                                add_cons_to_conflict = True
                        else:
                
                            print("same attribute should not have two different operand",bool_array[i],'and',bool_array[x])
                            add_cons_to_conflict = True
                    else:
                        continue
                else:
                    
                    continue
                
                if(add_cons_to_conflict):
                    if(bool_array[x] not in conflict_array):
                        conflict_array.append(bool_array[x])
                    if(bool_array[i] not in conflict_array):
                        conflict_array.append(bool_array[i])
        done_arr.append(bool_array[i])
        
    return conflict_array

def input_foreign_constraints(table_name,dic_para,forgn_cons):
    cons = input()    
    if(cons.casefold() != 'quit'):
        isvalid = check_cons_format(cons,table_name,dic_para)

        if(isvalid == True):
            forgn_cons.append(cons.upper())
        else:
            print("Enter another Constraint::")
        input_foreign_constraints(table_name,dic_para,forgn_cons)
    else:
        cons_list=[]
        for c in forgn_cons:
            isvalid = False
            isvalid = check_cons_format(c,table_name,dic_para)
            if(isvalid == True):
                cons_list.append(c)
        print(cons_list)
        dic_para.get(table_name).update({'Foreign_Constraints':cons_list})
        # print("update-mvd::",dic_para)    
        # key_dic = find_keys(table_name,dic_para)
        # ask_to_add_table()

def check_cons_format(c,table_name,dic_para):
    isvalid = False
    attr = []
    table_List = []
    for i in dic_para.get(table_name).get('attr').keys():
        attr.append(i)

    for table_name in dic_para.keys():
        table_List.append(table_name)


    print("table_List:::",table_List)
    if(':' in c):
        cons_split = c.split(":")
        if(len(cons_split) == 2):
            if(len(cons_split[0]) > 0 and len(cons_split[1]) > 0):
                if((cons_split[0] in attr) and (cons_split[1] in table_List)):
                    isvalid = True
                else:
                    if((cons_split[0] not in attr) and (cons_split[1] not in table_List)):
                        print("both column name and table name is not in your list")
                    elif((cons_split[0] in attr) and (cons_split[1] not in table_List)):
                        print("Table name is not in your list")
                    else:
                        print("Column Name is not in your list")
            else:
                print(c,"is not a valid foreign constraint.It should be (column name:table name).")
                
        else:
            print(c,"is not a valid foreign constraint.It should be (column name:table name).")
            
    else:
        print(c,"is not a valid foreign constraint.It should be (column name:table name).")
        
    return isvalid
d = input_data()