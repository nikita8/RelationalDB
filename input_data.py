import re
import numpy as np
from database import Database
from relational_algebra import RelationalAlgebra
from input_fds_mvds import *
from which_normal_form import *
import pdb

db = Database()

def input_table_name():
  try:
    table_name=input("Enter the name of the table/ Type quit to exit: ")
    table_name = table_name.upper().strip()
    if(table_name.casefold() == 'quit'):
      exit(0)
    if not table_name:
      print("**Table name cannot be blank")
      input_table_name()
  except Exception:
    if(KeyboardInterrupt):
        exit(0)
    else:
      print("Invalid Name")
      input_table_name()
  return table_name

def input_table_attributes():
  try:
    num_attr = 0
    attributes = {}
    while num_attr < 4:
      attr_input = input("Enter single character table Attribute name / Type quit to exit (Eg: A): ")
      attr_input = attr_input.strip().upper()
     
      if attr_input == 'QUIT':
        if attributes:
          break
        else:
          print("**Table should have atleast one attribute")
          continue
      elif attr_input:
        if not re.match('[a-zA-Z+]',attr_input): 
          print("**Table Attributes must be only alphabets(A-Z).")
          continue
        attr_input_type = get_attr_input_type(attr_input)
      elif not attr_input:
        print("**Attribute should not be blank")
        continue
      else: 
        continue
      attributes[attr_input] = attr_input_type
      num_attr += 1 
  except Exception:
    if(KeyboardInterrupt):
        exit(0)
    else:
      print("Invalid Type Option")
      get_attr_input_type(attr)
  return attributes

def get_attr_input_type(attr):
    try:
      attr_input_type = input(f"Enter the type of attribute {attr}: 1: 'string' and 2: 'int'):")
      attr_input_type = int(attr_input_type.strip())
      if attr_input_type not in [1, 2]:
        print('**Invalid Type')
        get_attr_input_type(attr)
      if attr_input_type == 1: 
        attr_input_type = 'string'
      else:
        attr_input_type = 'int'
      return attr_input_type
    except Exception:
      if(KeyboardInterrupt):
        exit(0)
      else:
        print("Invalid Type Option")
        get_attr_input_type(attr)

def input_boolean_constraints(attributes, boolean_constraints=set(), first_time=True):
    # try:
      
      if first_time:
          print("Enter list of constraints / Type 'quit' to exit (Attribute op Val) Eg: A > 5:")
      constraints = input()
      constraints = constraints.strip().upper()
      constraints = constraints.replace(" ", "")
      
      if(constraints == 'QUIT'):
          boolean_constraints = validate_boolean_constraints(boolean_constraints)
          if not boolean_constraints:
            print("**Empty boolean constraints")
          print("Boolean Constraints:",list(boolean_constraints))
          boolean_constraints = ask_to_add_more(attributes,boolean_constraints)
          return boolean_constraints
              
      elif not constraints:
        input_boolean_constraints(attributes, boolean_constraints, False)
      else:
        valid_constraints = check_boolean_constraints(constraints, attributes)
        if(valid_constraints):
          boolean_constraints.add(constraints)
        input_boolean_constraints(attributes, boolean_constraints, False)
    # except Exception:
    #   # if(KeyboardInterrupt):
    #   #   exit(0)
    #   # else:
    #     print("**Invalid Boolean Constraint enter it again.")
    #     input_boolean_constraints(attributes, boolean_constraints, False)
    # boolean_constraints = validate_boolean_constraints(boolean_constraints)
    # print("Boolean Constraints:",list(boolean_constraints))
      return boolean_constraints

def ask_to_add_more(attributes,boolean_constraints):
  try:
      add_more_constraint = input("Do you want to add new boolean constraints(yes/no)?")
      if add_more_constraint.strip().lower() == 'yes':
        input_boolean_constraints(attributes, boolean_constraints)
      elif add_more_constraint.strip().lower() == 'no':

        return boolean_constraints
      else:
        print("**Invalid Option")
        ask_to_add_more(attributes,boolean_constraints)
  except Exception:
    if(KeyboardInterrupt):
        exit(0)
    else:
      print("**Type Yes/No to add more boolean constraints.")
      ask_to_add_more(attributes,boolean_constraints)

def validate_boolean_constraints(boolean_constraints):
  try:
    print("Checking for conflicting Boolean conditions...")
    conflicting_constraints = check_conflicting_constraints(boolean_constraints)
    print("conflicting_constraints",conflicting_constraints)
    if conflicting_constraints:
        print('**Following are the conflicting boolean contraints:')
        print(conflicting_constraints)
        print("Removing those from boolean constraints list...")
        # for constraints in conflicting_constraints:
        #     boolean_constraints.remove(constraints)
        boolean_constraints = boolean_constraints - conflicting_constraints
    else:
        print('There is no conflicting boolean constraints.')
  except Exception:
      if(KeyboardInterrupt):
        exit(0)
      else:
        print("Unable to validate boolean Constraint")
  return  boolean_constraints
   
def check_conflicting_constraints(boolean_constraints):
  # try:
    conflicting_contraints = set()
    loop_constraints = set()
    for constraint in boolean_constraints:
      add_cons_to_conflict = False
      loop_constraints.add(constraint)
      validating_constraints = boolean_constraints - loop_constraints - conflicting_contraints
      for another_constraint in validating_constraints:
        if(constraint[0].strip() == another_constraint[0].strip()):
          bool_split_i = re.split('\W+',constraint)
          bool_split_x = re.split('\W+',another_constraint)
          constraint_operator = re.findall('\W+',constraint)[0]
          another_constraint_operator = re.findall('\W+',another_constraint)[0]
          if(constraint_operator == another_constraint_operator):
            if(bool_split_i[1] == bool_split_x[1]):
              print('**Duplicated constraints ',constraint,'and ',another_constraint)
              add_cons_to_conflict = True
              if add_cons_to_conflict:
                conflicting_contraints.add(constraint)
                conflicting_contraints.add(another_constraint)
            else:
              print("**Same attribute cannot have different values ", constraint,'and ',another_constraint)
              add_cons_to_conflict = True
              if add_cons_to_conflict:
                conflicting_contraints.add(constraint)
                conflicting_contraints.add(another_constraint)
          else:
            is_valid = is_valid_boolean_contraints(constraint_operator, another_constraint_operator, bool_split_i[1], bool_split_x[1])
            
            if not is_valid:
              print("**Conflicting boolean constraints: ", constraint,'and ',another_constraint)
              add_cons_to_conflict = True
            if add_cons_to_conflict:
              conflicting_contraints.add(constraint)
              conflicting_contraints.add(another_constraint)
        else:
          continue
  except Exception:
    if(KeyboardInterrupt):
        exit(0)
    else:
      print("Unable to validate conflict boolean Constraint")
    return conflicting_contraints

def is_valid_boolean_contraints(constraint_operator, another_constraint_operator, constraint, another_cons):
  bool = True
  
  if(constraint_operator in ['>','>='] and another_constraint_operator in ['<','<='] ): 
    if not constraint > another_cons: 
      bool = False
  elif(constraint_operator == '>' and another_constraint_operator == '>='): 
    if constraint == another_cons or constraint == another_cons: 
      bool = False
  elif(constraint_operator == '<' and another_constraint_operator == '<='): 
    if constraint == another_cons or constraint == another_cons:
      bool = False
  elif(constraint_operator in ['<','<='] and another_constraint_operator in ['>','>=']): 
    if not constraint < another_cons: 
      bool = False 
  elif(constraint_operator in ['<>','=='] and another_constraint_operator in ['<>','==']):
    if constraint == another_cons:
      bool = False
  else: 
    bool = False
  return bool
  

def check_boolean_constraints(boolean_constraint, attributes):
  try:
    table_attributes = list(attributes.keys())
    if boolean_constraint[0] in table_attributes:
      splitted_constraints = re.split('\W+', boolean_constraint)
      if( len(splitted_constraints) == 2 ):
          attribute, contraint_value = splitted_constraints
          if(re.findall('\W+', boolean_constraint) and attribute and contraint_value):
              attribute = attribute.strip()
              attr_type = attributes.get(attribute)
              bool_operator = re.findall('\W+', boolean_constraint)[0].strip()
              contraint_value = contraint_value.strip()
              return is_valid_contraints(attribute, bool_operator, contraint_value, attr_type, boolean_constraint)
          else:
              print("**Violating boolean constraint: ", boolean_constraint)
              print("**It must be as 'attr op val' eg:(A>10).")
              print("Add another boolean constraint:")
      else:
        print("**Violating boolean constraint: ", boolean_constraint)
        print("**It must be of format 'attr op val' eg:(A>10).")
        print("Add another boolean constraint:")
    elif(re.match('\W+',boolean_constraint[0])):
      print("**",boolean_constraint, " is not valid boolean Constraint.")
      print("**It must be as ' A>10 '.")
      print("Add another boolean constraint:")
    else:
      print("**Given Boolean constraint attribute is not valid")
      print("**Boolean Constraint attribute must be table attributes:",table_attributes)
      print("Add another boolean constraint:")
  except Exception:
    if(KeyboardInterrupt):
        exit(0)
    else:
      print("Unable to check boolean Constraint.")
  return False
   
def is_valid_contraints(boolean_attribute, boolean_operator, boolean_value, attr_type, input_boolean_str):
  if(attr_type == 'string'):
    if(boolean_operator not in ['==', '<>']):
      print("**Violating boolean constraint:", input_boolean_str)
      print(f"**Attribute '{boolean_attribute}' is type 'string' (operand must be '==' or '<>')")
      print("Add another boolean constraint:")
      return False
  elif(attr_type == 'int'):
    if(boolean_operator not in ['==','<>','>','>=','<','<=']):
      print("**Violating Non standard boolean constraint:", input_boolean_str)
      print(f"**Attribute '{boolean_attribute}' is type 'int' (operand must be '==' or '<>' or '>' or '>=' or '<' or '<=')")
      print("Add another boolean constraint:")
      return False
  return True
    
def input_fd(attributes, fds=set(), first_time=True):
  try:
    attr = ""
    attr = attr.join(attributes)
    if first_time:
      print("Enter FD's / Type 'quit' to exit and Press enter to add another fd: Eg: A->B")
    fd = input()
    fd = fd.strip().upper()
    fd = fd.replace(" ", "")
    if(fd != 'QUIT'):
      fds.add(fd)
      input_fd(attributes,fds,False)
    else:
      lhs_fd, rhs_fd = take_fd_list(fds, attr)
      fds = set()
      for lhs, rhs in zip(lhs_fd, rhs_fd):
        fds.add(f"{lhs}->{rhs}")
      print("Valid Fds: ",fds)
    
      fds = delete_fd(fds,attributes)
  except Exception:
    if(KeyboardInterrupt):
      exit(0)
    else:
      print("Invalid Fd enter in again")
      input_fd(attributes,fds,False)
    return fds
  
def delete_fd(fds,attributes):
  remove_fd = input("Do you want to remove any Functional Dependency (Yes/No):")
  remove_fd = remove_fd.strip()
  remove_fd = remove_fd.replace(" ", "")
  if(remove_fd.casefold() == 'yes'):
    fd = input('Enter functional Dependency to remove:')
    fd = fd.strip().upper()
    if(fd in fds):
      fds.discard(fd)
      print(f"Fd '{fd}' is removed.")
      delete_fd(fds,attributes)
    else:
      print('Entered fd not exists')
      delete_fd(fds,attributes)
  elif(remove_fd.casefold() == 'no'):
    decompose_nf(fds,attributes)
  return fds


def input_mvd(attributes,fds,mvds=set(),first_time=True):
  try:
    # attr = ""
    attr = "".join(attributes)
    print(attr)
    if first_time:
      print("Enter list of MVD's / Type 'quit' to exit or Press Enter to input another MVD: Eg: A->->B: ")
    mvd = input()
    mvd = mvd.strip().upper()
    mvd = mvd.replace(" ", "")
    if(mvd != 'QUIT'):
      mvds.add(mvd)
      input_mvd(attributes,fds,mvds,False)
    else:
      
      mvds_lhs,mvds_rhs = take_mvd_list(mvds,attr)
      fds_lhs = []
      fds_rhs = []
      for fd in fds:
        fd_lhs,fd_rhs = fd.split("->")
        fds_lhs.append(fd_lhs)
        fds_rhs.append(fd_rhs)

      mvds_lhs, mvds_rhs=remove_trival_mvd(mvds_lhs,mvds_rhs,fds_lhs,fds_rhs)
      mvds = set()
      for lhs, rhs in zip(mvds_lhs, mvds_rhs):
        mvds.add(f"{lhs}->->{rhs}")
      print("Valid MVDs: ", mvds)
    return mvds
  except Exception:
      print("Invalid FD to remove. Enter it again")
      input_mvd(attributes,fds,mvds, False)

        
def input_foreign_constraints(tables, attributes, table_name, foreign_constraints=set(), first_time=True):
  if first_time:
    print("Enter Foreign Constraint:-")
    print("Enter as 'column name:table name' (eg- A:ABC) / Type quit to exit: ")
  foreign_constraint = input()
  foreign_constraint = foreign_constraint.strip().upper()
  if(foreign_constraint != 'QUIT'):
      is_valid = check_format(foreign_constraint, attributes, tables, table_name)
      if is_valid:
          foreign_constraints.add(foreign_constraint)
      else:
        print("Enter another Constraint::")
      input_foreign_constraints(tables, attributes, table_name, foreign_constraints, False)
  constraints = {}
  for constraint in foreign_constraints:
    column_name, table_name = constraint.strip().split(":")
    constraints[table_name.strip()] = column_name.strip()
  return constraints
        
def check_format(foreign_constraint, attr, tables, current_table):
  isvalid = False
  if(':' in foreign_constraint):
      cons_split = foreign_constraint.split(":")
      if(len(cons_split) == 2):
          column_name = cons_split[0].upper().strip()
          table_name = cons_split[1].upper().strip()
          
          if(column_name and table_name):
              table = tables.get(table_name)
              if((column_name in attr) and table and (column_name in table.attributes)):
                isvalid = True
              else:
                if((column_name not in attr) and not table):
                  print("**Both column and table does not exist")
                elif((column_name in attr) and not table):
                  print("**Table does not exist")
                elif(column_name not in attr):
                  print(f"**The table '{current_table}' does not have attribute '{column_name}'")
                else:
                  print(f"**The foreign key table '{table}' does not have attribute '{column_name}'")
          else:
            print("**",foreign_constraint,"is not a valid foreign constraint.It should be of format (column name:table name).")
      else:
        print("**", foreign_constraint,"is not a valid foreign constraint.It should be (column name:table name).")
  else:
    print("**", foreign_constraint, "is not a valid foreign constraint.It should be (column name:table name).")
  return isvalid

# def validate_decomp(fds, attributes):
#   attr = ('').join(attributes)
#   for fd in fds:
#     fd_lhs,fd_rhs = fd.split("->")
#     fds_lhs.append(fd_lhs)
#     fds_rhs.append(fd_rhs)
#   table_keys = get_keys(fds_lhs,fds_rhs,attr)
#   normal_form = get_normal_form(table_keys,fds_lhs,fds_rhs)
#   print("Table Normal Form:",normal_form)
#   return decompose_nf(fds,attributes)

def decompose_nf(fds,attributes):
  attr = ('').join(attributes)
  fds_lhs = []
  fds_rhs = []

  for fd in fds:
    fd_lhs,fd_rhs = fd.split("->")
    fds_lhs.append(fd_lhs)
    fds_rhs.append(fd_rhs)
  table_keys = get_keys(fds_lhs,fds_rhs,attr)
  normal_form = get_normal_form(table_keys,fds_lhs,fds_rhs)
  print("Table Normal Form:",normal_form)
  if(normal_form not in ['BCNF','3NF']):
    print("Enter one of the following option to get the table to atleast 3NF?")
    print("1. Delete Table   2. Add or Remove FD")
    decompose_type = input("Enter Option:").strip()
    if(decompose_type not in ["1","2"]):
      print("Invalid Operation Type")
      decompose_nf(fds,attributes)
    elif(decompose_type == "1"):
      return fds,False
    else:
      print("Enter one of the type of FD operation?")
      print("1. Add FD   2. Remove FD")
      fd_type = input("Enter Option:").strip()
      if(fd_type not in ["1","2"]):
        print("Invalid Operation Type")
        decompose_nf(fds,attributes)
      elif(fd_type == "1"):
        fds = input_fd(attributes,fds)
        decompose_nf(fds,attributes)
      else:
        fds = delete_fd(fds,attributes)
        decompose_nf(fds,attributes)
  else:
    print("Table normal Form:",normal_form)

  return fds,True    
        
    

def get_normal_form(table_keys,fds_lhs,fds_rhs):
  normal_form = Which_NormalForm(table_keys,fds_lhs,fds_rhs)
  return normal_form

def input_key(attributes,fds,table_name):
  key = input(f"Select Key for {table_name} :").strip().upper()
  fds_lhs = []
  fds_rhs = []
  for fd in fds:
    fd_lhs,fd_rhs = fd.split("->")
    fds_lhs.append(fd_lhs)
    fds_rhs.append(fd_rhs)
  attr = ""
  attr = attr.join(attributes)
  compute_key_table = get_keys(fds_lhs,fds_rhs,attr)
  if(key not in compute_key_table):
    print(f"You must select key from {compute_key_table}")
    input_key(attributes,fds,table_name)

def input_table_info():
  table_name = []
  attributes = []
  boolean_constraints = []
  fds = []
  mvds = []
  foreign_constraints = {}
  keys = ""
  table_name = input_table_name()
  attributes = input_table_attributes()
  boolean_constraints = input_boolean_constraints(attributes) or []
  fds = input_fd(list(attributes.keys()))
  # fds = []
  mvds = input_mvd(list(attributes.keys()),fds)
  
  foreign_constraints = input_foreign_constraints(db.tables, attributes, table_name)
  # foreign_constraints = {}
  # TODO
  fds,is_valid_table = decompose_nf(fds,attributes)
  if not is_valid_table:
    return

  keys = input_key(attributes, fds,table_name)
  # keys = ('').join(keys)

  return {'name': table_name, 'attributes': attributes, 'fds': fds, 'mvds': mvds, 'boolean_constraints': boolean_constraints, 'key': keys, 'foreign_key_constraints': foreign_constraints}

def input_tuple(table, table_mapping):
  print(f"Insert values of {table.attributes} into '{table.name}': ") 
  row = {}
  for attr in table.attributes: 
    attr_value = input(f"value of {attr} : ") 
    row[attr] = attr_value 
  valid = validate_row(row, table)
  if valid:
    tables = table.demanding_new_tuple_tables(row, table_mapping)
    for dependent_table in tables:
      print("**Additional tuples required to maintain foreign key constraint: ")
      input_tuple(db.tables[dependent_table], table_mapping)
    table.insert_tuple(row_data=row)
  else:
    print("\n **Failed to input tuple due to violating boolean constraints.\n")

def validate_row(row, table):
  valid = True
  print(table.attributes_type)
  for attribute, data_type in table.attributes_type.items():
    if attribute in row:
      if data_type == 'int':
        try:
          input_value = int(row[attribute])
          for constraints in table.boolean_constraints:
            for op in ['==','<>','>','>=','<','<=']:
              if op in constraints:
                operand, value = constraints.split(op)
                if operand == attribute:
                  if op == '==':
                    if value != input_value:
                      print(f"**{attribute}: {input_value}, Violates constraint: {constraints}")
                      valid = False
                  elif op in ['>', '>=']:
                    if op == '>=':
                      if value < input_value:
                        print(f"**{attribute}: {input_value}, Violates constraint: {constraints}")
                        valid = False
                    elif value <= input_value:
                      print(f"**{attribute}: {input_value}, Violates constraint: {constraints}")
                      valid = False
                  elif op in ['<', '<=']:
                    if op == '<=':
                      if value > input_value:
                        print(f"**{attribute}: {input_value}, Violates constraint: {constraints}")
                        valid = False
                    elif value >= input_value:
                      print(f"**{attribute}: {input_value}, Violates constraint: {constraints}")
                      valid = False
                  elif op == '<>':
                    if value == input_value:
                      print(f"**{attribute}: {input_value}, Violates constraint: {constraints}")
                      valid = False
        except Exception:
          print(f"Invalid data type for integer type attribute {attribute}")
          return False
      else:
        for constraints in table.boolean_constraints:
          input_value = row[attribute]
          for op in ['==','<>']:
            if op in constraints:
              operand, value = constraints.split(op)
              operand = operand.strip()
              value = value.strip()
              if op == '==':
                if input_value != value:
                  print(f"**{attribute}: {value}, Violates constraint: {constraints}")
                  valid = False
              elif op == '<>':
                if input_value == value:
                  print(f"**{attribute}: {value}, Violates constraint: {constraints}")
                  valid = False
  return valid
  
def enter_table(tables):
  table_name = input("Enter the name of the table:/ Type quit to exit: ").strip().upper()
  if table_name.lower() == 'quit':
    return
  table = tables.get(table_name)
  if not table:
    print("**Table does not exist")
    enter_table(tables)
  return table

def delete_tuple(table):
  conditons = input("Enter the condition separated by ','(Eg: A:1, B:ab, C:a): ").strip()
  conditions = conditons.split(',')
  query = {}
  for condition in conditions:
    key, value = condition.strip().split(':')
    if not key or not value:
      print("**Invalid Input condition")
      return
    query[key.strip()] = f"'{value}'"
  table.delete_tuples(query)
  print("--------------------")

def find_tuple(table):
  query = input("Enter the query separated by and(&) or or(|) Eg: A == 1 | A != 5 & B=='test': ").strip()
  table.find_tuples(query)

def group_tuples(table):
  attributes = input("Enter the attributes Eg: AB to group attributes based on A and B: ").strip().split()
  table.group_tuples(attributes)

def create_table():
  table = input_table_info()
  if table:
    db.create_table(table['name'], table)
    #add associated tables
    for tbl in table['foreign_key_constraints'].keys():
      foreign_table = db.tables[tbl]
      foreign_table.add_associated_tables(db.tables[table['name']])

def input_operation():
  if not db.tables:
    print('Database empty. No tables.')
    print("----------------------------")
    more = input('Do you want to create new table?yes/no: ').strip().lower()
    if more == 'yes':
      create_table()
    else:
      exit(0)
  operations = "Table actions: \n 1. Input Tuple. \t2. Delete a tuple \t 3. Find Tuple \t 4. Group Tuples \t 5. Delete a table \n Two table operations: \n 6. Cross Join \t 7. Natural Join \t 8. Union \t 9. Intersection \t 10.Difference \n Other Actions: \n 11. Create new table \t 12. Show all tables"
  print(operations)
  operation = input("Enter the data manipulation option(1-12) from the above list/ Type quit to exit: ").strip()
  if operation.lower() == 'quit':
    exit(0)
  elif operation not in [str(i) for i in range(1, 13)]:
      print("**Invalid selection of option \n")
      input_operation()

  operation = int(operation)
  if operation in range(1, 6):
    table = enter_table(db.tables)
  elif operation in range(6, 11):
    print("Enter name of two tables:")
    print("Table 1:")
    table1 = enter_table(db.tables)
    if table1:
      print("Table 2:")
      table = enter_table(db.tables)
      if table:
        rdb = RelationalAlgebra(table1, table)
  else:
    table = ''
  try:
    if operation not in [11, 12] and not table:
      input_operation()
  
    if operation == 1:
      input_tuple(table, db.tables)
    elif operation == 2:
      delete_tuple(table)
    elif operation == 3:
      find_tuple(table)
    elif operation == 4:
      group_tuples(table)
    elif operation == 5:
      db.drop_table(table.name)
    elif operation == 6:  
      print(rdb.cross_join())
    elif operation == 7:
      print(rdb.natural_join())
    elif operation == 8:
      print(rdb.union())
    elif operation == 9:
      print(rdb.intersection())
    elif operation == 10:
      print(rdb.difference())
    elif operation == 11:
      create_table()
    elif operation == 12:
      show_tables()
  except Exception as e:
    print(e)
  input_operation()

def show_tables():
  print(list(db.tables.keys()))

while True:
  create_table()
  input_table = input("Do you want to enter new table (Yes/No): ")
  input_table = input_table.strip().lower()
  if(input_table != 'yes'):
    break
input_operation()
    