#    a. define new tables: table name, attribute names and types 
#    b. for each defined table ask users to input possible constraints,
#       including Boolean conditions, FDs and MVDs (in this order):
#       The legitimacy of constrains should be checked:
def is_int(user_input):
    try:
        val = int(user_input)
    except ValueError:
        print("That's not an int!")
        return -1
    return val
    

def age_constrain(age,max,min):
    if(age < min or age > max):
        print('The max age is',max,' and the min',min)
        return False
    else:
        return True
def get_attribute_type(attr):
    attr_type={}
    # 1 for  string type
    # 2 for  int type
    str_mg= 'Enter attribute tpye\n# 1 for string\n# 2 for int\n'
    for i in attr:
        while(True):
            user_input = input(str_mg+'for ('+i+') : ')
            user_input = is_int(user_input)
            if(user_input == -1):
                continue
            elif(user_input < 3 and user_input > 0):
                print("great choice",user_input)
                attr_type[i]=user_input
                break
            else:
                print("wrong choice, try again")
    return attr_type
    
def get_attribute_constrain(attr):
    # 1 for  string type
    # A allow repeaped attr in the same column
    # 2 for  int type
    # define range max and min
    temp=0
    attr_constrain={}
    range_data={}
    range_list = ['max_range','min_range']
    msg11=['Enter maximum range: ','Enter minimum range: ']
    msg22= '\nEnter costrain:\n# 1 to allow repeated atributes\n# 2 to disallow repeated atributes\n'
    for i,j in attr.items():
        if(j == 1):
            print('\nAttribute: <'+i+'> with (string type)')
            while(True):
                user_input = input(msg22)
                user_input = is_int(user_input)
                if(user_input == -1):
                    continue
                elif(user_input == 1 or user_input == 2):
                    print("great choice",user_input)
                    if(1 == user_input):
                        attr_constrain[i]=True
                    else:
                        attr_constrain[i]=False
                    break
                else:
                    print("wrong choice!!, try again")
        else:
            # define max and min
            print('\nAttribute :<'+i+'> with Integer type')
            for x in range(2):
                while(True):
                    user_input = input(msg11[x])
                    user_input = is_int(user_input)
                    if(user_input == -1):
                        continue
                    elif(x == 1 and temp  < user_input ):

                        # if max < min
                        print('not allowed:\nmax = ',temp,' < min =',user_input)
                        continue
                    elif(user_input):
                        # print(msg11[x],user_input)
                        temp= user_input
                        range_data[range_list[x]] = temp
                        break
                    else:
                        print("wrong choice!!, try again")
            attr_constrain[i]= range_data
    return attr_constrain

attr=['A','B','C','D']
# list_age=[]

# age_constrain(i,65,18)):
   
attr_type = get_attribute_type(attr)
attr_constrain = get_attribute_constrain(attr_type)
print(attr_type)
print(attr_constrain)





# attri={'A':{'min':100,'max':200},'B':{'A':False},'C':{'min':100},'D':{'min':100}}
# for i,j in attri.items():
#     print(i,j)
# sub =  attri['A']
# print(sub)


