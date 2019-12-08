import pandas as pd
import math

class Table:
  def __init__(self, name, attributes, fds, mvds, boolean_constraints, key, foreign_key_constraints=[], rows=[]):
    self.name = name
    self.attributes = attributes
    self.fds = fds
    self.mvds = mvds
    self.key = key
    self.boolean_constraints = boolean_constraints
    self.rows = pd.DataFrame(rows, columns = attributes)
    # data['Item Code'].astype(str)
    self.foreign_key_constraints = foreign_key_constraints
    self.dependent_tables = []

  def to_dict(self):
    return self.__dict__
  
  def __repr__(self):
    return f"name={self.name}, attributes={self.attributes}, fds={self.fds}, mvds={self.mvds}, boolean_constraints={self.boolean_constraints}, foreign_key_constraints={self.foreign_key_constraints}"

  def insert_tuple(self, row_data):
    key_attributes = list(self.key)
    row = 0 if math.isnan(self.rows.index.max()) else self.rows.index.max() + 1
    if self.is_duplicate_key(key_attributes, row_data):
      key_data = { k:v for k,v in row_data.items() if k in key_attributes }
      print(f"Duplicate Key: {key_data} already exist in the table.")
      return
    self.rows.loc[row] = row_data
    print(f"Inserted row: {row_data}")
  
  def delete_tuples(self, query, parent=True):
    query = ' and '.join([f'{k}=={v}' for k, v in query.items()])
    matched_rows_index = self.rows.query(query).index
    rows_count = len(matched_rows_index)
    if rows_count != 0 and self.dependent_tables:
      self.delete_associated_tables_rows(matched_rows_index)
      print("Deleted dependent tables rows")
    self.rows.drop(matched_rows_index, inplace=True)
    if parent: print(f"Deleted {rows_count} tuples.") 

  def find_tuples(self, query):
    print(f"Rows based on query: {query}")
    print(self.rows.query(query))
    print("-------------------------------")

  def group_tuples(self, attributes):
    print(f"Grouped tuples based on attribute(s) {attributes}")
    grouped_tuples = self.rows.groupby(attributes)
    for key, _ in grouped_tuples:
      print(key, ':')
      print(grouped_tuples.get_group(key), "\n\n")
    print("-------------------------------")

  def drop(self):
    self.rows.iloc[0:0]

  def is_duplicate_key(self, key, data):
    self.find(key, data).all(axis=1).any()

  def find(self, key, data):
    query = ' and '.join([f'{k}=={v}' for k, v in data.items() if k in key])
    return self.rows.query(query)
  
  def add_dependent_tables(self, table):
    self.dependent_tables.append(table)

  def delete_associated_tables_rows(self, matched_rows_index):
    print("Deleting dependent tables rows")
    for _, row in self.rows.iloc[matched_rows_index].iterrows():
      for table in self.dependent_tables:
        key = list(table.key)
        query = { f"{k}" : row[f"{k}"] for k in key }
        table.delete_tuples(query, parent=False)

      




