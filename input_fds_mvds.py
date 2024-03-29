
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1,1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]
def check_fd_format(s):
    s_l = len(s)
    if(s_l == 0):
        print("No FD list was passed to check")
        return 0
    #[A][-][>][C] FD >= 4
    if(s_l < 4):
        print("an FD must in this format: 'A->B' ")
        print("yours is in this form",s_l)
        return 0
    # Check if X is alphabet and Y is alphabet: X->Y
    # here we check if '-' is fallowed by'>'
    if(not(s[0].isalpha() and s[s_l-1].isalpha())):
        print("an FD must in this format: 'A->B' ")
        print("yours is in this form",s_l)
        return 0
    for i in range(1,s_l-1):
        if(s[i] == '-' ):
            if(s[i+1]=='>' and s[i-1].isalpha() and s[i+2].isalpha()):
                return 1
        else:
            continue
    print("an FD must in this format: 'A->B' ")
    print("yours is in this form",s_l)
    return 0
def print_fds_mvds(lhs,rhs,arrow):
    for i in range(len(lhs)):
        print(lhs[i],arrow,rhs[i])

def check_mvd_format(s):
    s_l = len(s)
    #[A][-][>][C] FD >= 4
    if(s_l < 6):
        print("an MVD must be in this format: 'A->->B'")
        print("yours is in this form",s_l)
        return 0
    # Check if X is alphabet and Y is alphabet: X->->Y
    # here we check if '-' is fallowed by'>'
    if(not(s[0].isalpha() and s[s_l-1].isalpha())):
        print("an MVD must be in this format: 'A->->B'")
        print("yours is in this form",s_l)
        return 0
    for i in range(1,s_l-1):
        if(s[i] == '-' ):
            if(s[i+1] == '>' and s[i+2] == '-' and s[i+3] == '>' and s[i-1].isalpha() and s[i+4].isalpha()):
                return 1
        else:
            continue
    print("an MVD must be in this format: 'A->->B'")
    print("yours is in this form",s_l)
    return 0
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
                lfd_subset =[]
                str_tmp=''
                for k in lfd:
                    sub_k = list(powerset(list(k)))
                    for m in sub_k:
                        str_m=''.join(map(str,m))
                        lfd_subset.append(str_m)
                if(str_lhs == str_rhs):
                    print("trivial "+fd_mvd,str_lhs,arrow,str_rhs)

                elif(str_lhs in lfd and str_rhs in rfd or str_lhs in  lfd_subset and str_rhs in rfd ): 
                    index_rhs = rfd.index(str_rhs)
                    if(not lfd[index_rhs] == str_lhs ):#check for weak fds
                        print("Superfluous "+fd_mvd+":",lfd[index_rhs]+arrow+str_rhs,"replace by",str_lhs+arrow+str_rhs)
                        lfd[index_rhs] = str_lhs
                    else:
                        print("Already in "+fd_mvd, str_lhs+arrow+str_rhs)
                elif (str_lhs not in lfd or str_rhs not in rfd): 
                    # print(str_lhs,arrow,str_rhs)
                    rfd.append(str_rhs)
                    lfd.append(str_lhs)
                else:
                    pass
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
                    else:
                        print("Superfluous",fd_mvd,":",str_lhs,arrow,str_rhs[x])
                    x = x + 1
    #return LHS and RHS lists
    return lfd,rfd
def remove_trival_mvd(mvd_lhs,mvd_rhs, fd_lhs,fd_rhs):
    for i in range(len(mvd_rhs)):
        if(mvd_rhs[i] in fd_rhs):
            fd_index = fd_rhs.index(mvd_rhs[i])
            if(mvd_lhs[i] == fd_lhs[fd_index]):
                # print("Trivial Already in FD:",mvd_lhs[i],'->->',mvd_rhs[i])
                print('Triviliaze MVD:',mvd_lhs[i]+'->->'+mvd_rhs[i],'by FD:',fd_lhs[fd_index]+'->'+fd_rhs[fd_index])
                mvd_rhs[i]='-'
                mvd_lhs[i]='-'
    while('-' in mvd_rhs):
        mvd_rhs.remove('-')
        mvd_lhs.remove('-')
    return mvd_lhs,mvd_rhs
    
def take_mvd_list(mvd_list,attr1):
    mvds_lhs=[]
    mvds_rhs=[]
    for i in mvd_list:
        val= check_mvd_format(i)# return 1 for FD, 0 wrong input with some comment
        if(val == 1):
            # print("MVD",str1)
            key1,val1 = get_mvd(i)
            mvds_lhs.append(key1)
            mvds_rhs.append(val1)
        else:
            print("MVD must be in this format: 'A->->B'")
            # mvds_lhs=[]
            # mvds_rhs=[]
            # return mvds_lhs, mvds_rhs
    mvds_lhs,mvds_rhs = fds_mvds_validation(mvds_lhs,mvds_rhs,attr1,"MVD", '->->')
    return mvds_lhs,mvds_rhs

def take_fd_list(fd_list,attr1):
    fds_lhs=[]
    fds_rhs=[]
    if(len(fd_list) == 0):
        return fds_lhs, fds_rhs
    for i in fd_list:
        val= check_fd_format(i)# return 1 for FD, 0 wrong input with some comment
        if(val== 1):
            # print("FD:",i)
            key1,val1 = get_fd(i)
            fds_lhs.append(key1)
            fds_rhs.append(val1)
        else:
            print("FD must be in this format: 'A->B'")
            # fds_lhs=[]
            # fds_rhs=[]
            # return fds_lhs, fds_rhs
    fds_lhs,fds_rhs = fds_mvds_validation(fds_lhs,fds_rhs,attr1,"FD", "->")
    return fds_lhs, fds_rhs

