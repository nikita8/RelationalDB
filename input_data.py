import re
import numpy as np
# import FD
from database import Database
from relational_algebra import RelationalAlgebra

def input_table_name():
  table_name=input("Enter the name of the table/ Type quit to exit: ")
  table_name = table_name.upper().strip()
  if(table_name.casefold() == 'quit'):
    exit(0)
  if not table_name:
    print("Table name cannot be blank")
    input_table_name()
  return table_name

def input_table_attributes():
  num_attr = 0
  attributes = {}
  while num_attr < 4:
    attr_input = input("Enter single character table Attribute name / Type quit to exit (Eg: A): ")
    attr_input = attr_input.strip().upper()
    if attr_input == 'QUIT':
      if attributes:
        break
      else:
        print("Table should have atleast one attribute")
        continue
    elif attr_input:
      attr_input_type = get_attr_input_type(attr_input)
    else: 
      continue
    attributes[attr_input] = attr_input_type
    num_attr += 1 
  return attributes

def get_attr_input_type(attr):
    attr_input_type = input(f"Enter the type of attribute {attr}: 1: 'string' and 2: 'int'):")
    attr_input_type = int(attr_input_type.strip())
    if attr_input_type not in [1, 2]:
      print('Invalid Type')
      get_attr_input_type(attr)
    if attr_input_type == 1: 
      attr_input_type = 'string'
    else:
      attr_input_type = 'int'
    return attr_input_type

def input_boolean_constraints(attributes, boolean_constraints=set(), first_time=True):
    if first_time:
        print("Enter list of constraints / Type 'quit' to exit (Attribute op Val) Eg: A > 5:")
    constraints = input()
    constraints = constraints.strip().upper()
    if(constraints == 'QUIT'):
        boolean_constraints = validate_boolean_constraints(boolean_constraints)
        if not boolean_constraints:
            print("Empty boolean constraints after removing conflicting ones")
            add_more = input("Do you want to add new boolean constraints(yes/no)?")
            if add_more.strip().lower() == 'yes':
              input_boolean_constraints(attributes, boolean_constraints)
            else:
              return boolean_constraints
    else:
      valid_constraints = check_boolean_constraints(constraints, attributes)
      if(valid_constraints):
        boolean_constraints.add(constraints)
      input_boolean_constraints(attributes, boolean_constraints, False)
      return boolean_constraints

def validate_boolean_constraints(boolean_constraints):
    print("Checking for conflicting Boolean conditions...")
    conflicting_constraints = check_conflicting_constraints(boolean_constraints)
    if conflicting_constraints:
        print('Following are the conflicting boolean contraints:')
        print(conflicting_constraints)
        print("Removing those from boolean constraints list...")
        # for constraints in conflicting_constraints:
        #     boolean_constraints.remove(constraints)
        boolean_constraints = boolean_constraints - conflicting_constraints
    else:
        print('There is no conflicting boolean constraints.')   
    return  boolean_constraints
   
def check_conflicting_constraints(boolean_constraints):
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
        constraint_operator = re.findall('\W+',constraint)
        another_constraint_operator = re.findall('\W+',another_constraint)
        if(np.array_equal(constraint_operator,another_constraint_operator)):
          if(bool_split_i[1] == bool_split_x[1]):
            print('Duplicated constraints ',constraint,'and ',another_constraint)
            add_cons_to_conflict = True
          else:
            print("Same attribute cannot have different values ", constraint,'and ',another_constraint)
            add_cons_to_conflict = True
        else:
          is_valid = is_valid_boolean_contraints(constraint_operator, another_constraint_operator, bool_split_i[1], bool_split_x[1])
          if not is_valid:
            print("Conflicting boolean constraints: ", constraint,'and ',another_constraint)
          add_cons_to_conflict = True
      else:
        continue

    if add_cons_to_conflict:
      conflicting_contraints.add(constraint)
      conflicting_contraints.add(another_constraint)
    
  return conflicting_contraints

def is_valid_boolean_contraints(constraint_operator, another_constraint_operator, constraint, another_cons):
  if(constraint_operator in ['>','>='] and another_constraint_operator in ['<','<='] ): 
    if Constraint > another_cons: 
      return False
  elif(constraint_operator == '>' and another_constraint_operator == '>='): 
    if Constraint != another_cons: 
      return False
  elif(constraint_operator == '<' and another_constraint_operator == '<='): 
    if constraint != another_cons: 
      return False
  elif(constraint_operator in ['<','<='] and another_constraint_operator in ['>','>=']): 
    if Constraint < another_cons: 
      return False 
  else: 
    return False
  return True

def check_boolean_constraints(boolean_constraint, attributes):
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
            print("Violating boolean constraint: ", boolean_constraint)
            print("It must be as 'attr op val' eg:(A>10).")
            print("Add another boolean constraint:")
    else:
      print("Violating boolean constraint: ", boolean_constraint)
      print("It must be of format 'attr op val' eg:(A>10).")
      print("Add another boolean constraint:")
  elif(re.match('\W+',boolean_constraint[0])):
    print(boolean_constraint, " is not valid boolean Constraint.")
    print("It must be as ' A>10 '.")
    print("Add another boolean constraint:")
  else:
    print("Given Boolean constraint attribute is not valid")
    print("Boolean Constraint attribute must be table attributes:",table_attributes)
    print("Add another boolean constraint:")
  return False
   
def is_valid_contraints(boolean_attribute, boolean_operator, boolean_value, attr_type, input_boolean_str):
  if(attr_type == 'string'):
    if(boolean_operator not in ['==', '<>']):
      print("Violating boolean constraint:", input_boolean_str)
      print(f"Attribute '{boolean_attribute}' is type 'string' (operand must be '==' or '<>')")
      print("Add another boolean constraint:")
      return False
  elif(attr_type == 'int'):
    if(boolean_operator not in ['==','<>','>','>=','<','<=']):
      print("Violating Non standard boolean constraint:", input_boolean_str)
      print(f"Attribute '{boolean_attribute}' is type 'int' (operand must be '==' or '<>' or '>' or '>=' or '<' or '<=')")
      print("Add another boolean constraint:")
      return False
  return True
    
def input_fd(attributes, fds=set(), first_time=True):
  if first_time:
    print("Enter FD's / Type 'quit' to exit and Press enter to add another fd: Eg: A->B")
  fd = input()
  fd = fd.strip().upper() 
  if(fd != 'QUIT'):
    fds.add(fd)
    input_fd(attributes, fds)
  else:
    # lhs_fd, rhs_fd = take_fd_list(fds, attributes)
    # fds = set()
    # for lhs, rhs in zip(lhs_fd, rhs_fd):
    #   fds.add(f"{lhs}->{rhs}")
    print("Valid Fds: ", fds)
    fds = remove_fds(fds)
  return fds
  
def remove_fds(fds):
  remove_fd = input("Do you want to remove any Functional Dependency (Yes/No):")
  remove_fd = remove_fd.strip()
  if(remove_fd.casefold() == 'yes'):
    fd = input('Enter functional Dependency to remove:')
    fd = fd.strip().upper()
    if(fd in fds):
      fds.discard(fd)
      print(f"Fd '{fd}' is removed.")
      remove_fds(fds)
    else:
      print('Entered fd not exists')
      remove_fds(fds)
  return fds

def input_mvd(attributes, mvds=set(), first_time=True):
  if first_time:
    print("Enter list of MVD's / Type 'quit' to exit or Press Enter to input another MVD: Eg: A ->->B")
  mvd = input()
  mvd = mvd.strip().upper()
  if(mvd != 'quit'):
    mvds.add(mvd)
    input_mvd(attributes, mvds, False)
  else:
    # lhs_mvd, rhs_mvd = take_mvd_list(mvds, attributes)
    # mvds = set()
    # for lhs, rhs in zip(lhs_mvd, rhs_mvd):
    #   mvds.add(f"{lhs}->->{rhs}")
    print("Valid MVDs: ", mvds)
  return mvds
        
def input_foreign_constraints(tables, attributes, table_name, foreign_constraints=set(), first_time=True):
  if first_time:
    print("Enter Foreign Constraint:-")
    print("Enter as 'column name:table name' (eg- A:ABC) / Type quit to exit:")
  foreign_constraint = input()
  foreign_constraint = foreign_constraint.strip().upper()
  if(foreign_constraint != 'QUIT'):
      is_valid = check_format(foreign_constraint, attributes, tables, table_name)
      if is_valid:
          foreign_constraints.add(foreign_constraint)
      else:
        print("Enter another Constraint::")
      input_foreign_constraints(tables, attributes, table_name, foreign_constraints, False)
  else:
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
              if((column_name in attr) and table and (column_name in tables.attributes)):
                isvalid = True
              else:
                if((column_name not in attr) and not table):
                  print("Both column and table does not exist")
                elif((column_name in attr) and not table):
                  print("Table does not exist")
                elif(column_name not in attr):
                  print(f"The table '{current_table}' does not have attribute '{column_name}'")
                else:
                  print(f"The foreign key table '{table}' does not have attribute '{column_name}'")
          else:
            print(foreign_constraint,"is not a valid foreign constraint.It should be of format (column name:table name).")
      else:
        print(foreign_constraint,"is not a valid foreign constraint.It should be (column name:table name).")
  else:
    print(foreign_constraint, "is not a valid foreign constraint.It should be (column name:table name).")
  return isvalid

def validate_decomp(fds, attributes):
  normalForm = get_nf(fds, attributes)
  print("Normal Forem:::",normalForm)
  if(normalForm not in ['BCNF','3NF']):
    while(normalForm not in ['BCNF','3NF']):
      mvds = []
      decompose_nf(table_name,dic_para,fds,mvds)
  else:
    ask_for_keys(table_name,dic_para)

def input_key(attributes, fds):
  pass

def input_table_info(db):
  table_name = input_table_name()
  attributes = input_table_attributes()
  # boolean_constraints = input_boolean_constraints(attributes)
  boolean_constraints = []
  # fds = input_fd(list(attributes.keys()))
  fds = []
  # mvds = input_mvd(list(attributes.keys()))
  mvds = []
  # foreign_constraints = input_foreign_constraints(db.tables, attributes, table_name)
  foreign_constraints = {}
  # TODO
  # fds = validate_decomp(fds, attributes)
  # keys = input_key(attributes, fds)
  keys = list(attributes)

  return {'name': table_name, 'attributes': attributes, 'fds': fds, 'mvds': mvds, 'boolean_constraints': boolean_constraints, 'key': keys, 'foreign_key_constraints': foreign_constraints}

def input_tuple(table, table_mapping):
  # row = input("Enter the tuple: Eg: ")
  print(f"Insert values of {table.attributes} into '{table.name}':") 
  row = {} 
  for attr in table.attributes: 
    attr_value = input(f"value of {attr} : ") 
    row[attr] = attr_value 
  valid = validate_row(row)
  tables = table.demanding_new_tuple_tables(row, table_mapping)
  for dependent_table in tables:
    print("Additional tuples required for foreign key constraint tables:")
    input_tuple(dependent_table, table_mapping)
  if valid:
    table.insert_tuple(row_data=row)
  else:
    print("Failed to input tuple")

def validate_row(row):
  return True

def enter_table(tables):
  table_name = input("Enter the name of the table:/ Type quit to exit: ").strip().upper()
  if table_name.lower() == 'quit':
    return
  table = tables.get(table_name)
  if not table:
    print("Table does not exist")
    enter_table(tables)
  return table

def delete_tuple(table):
  conditons = input("Enter the condition: Eg: A:1, B:2").strip()
  conditions = conditons.split(',')
  query = {}
  for condition in conditions:
    key, value = condition.strip().split(':')
    if not key or not value:
      print("Invalid Input condition")
      return
    query[key] = value
  table.delete_tuples(query)

def find_tuple(table):
  query = input("Enter the query separated by and(&) or or(|) Eg: A == 1 | A != 5 & B=='test'").strip()
  table.find_tuples(query)

def group_tuples(table):
  attributes = input("Enter the attributes Eg: AB").strip().split()
  table.group_tuples(attributes)

def create_table(db):
  table = input_table_info(db)
  db.create_table(table['name'], table)
  #add associated tables
  for tbl in table['foreign_key_constraints'].keys():
    table = db.tables[tbl]
    table.add_associated_tables(db.tables[table['name']])

def input_operation(db, print_more_option=False, error_message=''):
  if print_more_option:
    more = input('Do you want to execute more data manipulations?yes/no: ').strip().lower()
    if more != 'yes':
      exit(0)
    else:
      if not db.tables:
        print('Database empty. No tables.')
        more = input('Do you want to create new table?yes/no: ').strip().lower()
        if more == 'yes':
          create_table(db)
        else:
          exit(0)
  operations = "1. Input Tuple. \n 2. Delete a tuple \n 3. Find Tuple \n 4. Group Tuples \n 5. Delete a table \n\n Two table operations: \n 6. Cross Join \n 7. Natural Join \n 8. Union \n 9. Intersection \n 10.Difference \n 11. Create new table"
  print(operations)
  operation = input("Enter the data manipulation option from the above list/ Type quit to exit: ").strip()
  if operation.lower() == 'quit':
    exit(0)
  elif operation not in [str(i) for i in range(1, 12)]:
      print("Invalid selection of option \n")
      input_operation(db)

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
    if operation != 11 and not table:
      input_operation(db.tables)
  
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
      create_table(db)
  except Exception as e:
    print(e)
  db.show_table(table.name)
  input_operation(db, print_more_option=True)

db = Database()
while True:
  create_table(db)
  input_table = input("Do you want to enter new table (Yes/No): ")
  input_table = input_table.strip().lower()
  if(input_table != 'yes'):
    break
input_operation(db)



    