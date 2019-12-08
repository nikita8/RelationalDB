# import pandas as pd
from table import *
from relational_algebra import *

class Database:
  def __init__(self, name="new_database"):
    self.name = name
    self.tables = {}
    self.table_dependencies = {}
  
  def create_table(self, table_name, table_data):
    self.add_dependencies(table_data.get('foreign_key_constraints'), table_name)
    table = Table(**table_data)
    self.tables[table_name] = table
    return table

  def drop_table(self, table_name, main_table=True):
    table = self.tables[table_name]
    self.delete_dependencies(table_name)
    table.drop
    if(main_table):
      print(f"Successfully Dropped table {table_name}.")
    del self.tables[table_name]

  def show_table(self, table_name, limit=10):
    table = self.tables.get(table_name)
    if not table:
      print(f"Table '{table_name}' does not exist.")
      return
    print(f"Table: {table_name}")
    print(self.tables[table_name].rows.head(limit))

  def delete_dependencies(self, table_name):
    # TODO: Take care of multiple dependencies 
    dependent_tables = self.table_dependencies.get(table_name)
    if dependent_tables:
      print(f"Dropping dependent tables of '{table_name}':")
      for dependent_table in dependent_tables:
        self.drop_table(table_name=dependent_table, main_table=False)
        print(f"    Dropped table '{dependent_table}'")
      del self.table_dependencies[table_name]

  def add_dependencies(self, table_name, dependent_table):
    if table_name:
      dependencies = self.table_dependencies.get(table_name, [])
      dependencies.append(dependent_table)
      self.table_dependencies[table_name] = dependencies

db = Database()
table_name = 'first_table'
second_table_name = 'second_table'
attributes = ['A','B','C','D']
key = 'AB'
table1 = db.create_table(table_name, {'name': table_name, 'attributes': attributes, 'fds': [], 'mvds': [], 'boolean_constraints': [], 'rows': [], 'key': key})
table1.insert_tuple(row_data={'A': 1, 'B': 2, 'C': 3, 'D': 4})
table1.insert_tuple(row_data={'A': 2, 'B': 3, 'C': 4, 'D': 5})
table1.insert_tuple(row_data={'A': 1, 'B': 3, 'C': 3, 'D': 4})
table1.insert_tuple(row_data={'A': 200, 'B': 3, 'C': 3, 'D': 4})
# table1.group_tuples(['A', 'B'])
# table1.delete_tuples({'A':1, 'B': 2})
# table1.find_tuples("A == 1 | A == 2 & C != 1")
db.show_table(table_name)

# attributes = ['A','B','G','F', 'E']
table2 = db.create_table(second_table_name, {'name': second_table_name, 'attributes': attributes, 'fds': [], 'mvds': [], 'boolean_constraints': [], 'rows': [], 'key': key, 'foreign_key_constraints': table_name})
# table2.insert_tuple(row_data={'A': 1, 'B': 2, 'G': 10, 'F': 11, 'E': 15})
# table2.insert_tuple(row_data={'A': 2, 'B': 3, 'G': 10, 'F': 100, 'E': 15})
# table2.insert_tuple(row_data={'A': 1, 'B': 3, 'G': 100, 'F': 100, 'E': 15})
table2.insert_tuple(row_data={'A': 1, 'B': 2, 'C': 3, 'D': 4})
table2.insert_tuple(row_data={'A': 200, 'B': 3, 'C': 4, 'D': 5})
db.show_table(second_table_name)

table1.add_dependent_tables(table2)

table1.delete_tuples({'A':200, 'B': 3})

# rdb = RelationalAlgebra(table2, table1)
# print(rdb.natural_join())
# print(rdb.union())
# print(rdb.cross_join())
# print(rdb.difference())

# db.drop_table(table_name)
# db.show_table(table_name)


