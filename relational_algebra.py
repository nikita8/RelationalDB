import numpy as np
import pandas as pd

class RelationalAlgebra:
  def __init__(self, table1, table2):
    self.table1 = table1
    self.table2 = table2
    self.common_attributes = self.find_common_attributes()

  def find_common_attributes(self):
    return list(np.intersect1d(self.table1.attributes, self.table2.attributes))
  
  def same_attributes_tables(self):
    return set(self.table1.attributes) == set(self.table2.attributes)

  def cross_join(self):
    table1 = self.table1.rows.copy()
    table2 = self.table2.rows.copy()
    #creating a new common column for two tables to join
    table1['_joinkey'] = 1
    table2['_joinkey'] = 1
    suffixes = (f"_{self.table1.name}", f"_{self.table2.name}")
    return pd.merge(table1, table2, on='_joinkey', suffixes=suffixes).drop('_joinkey', axis=1)

  def natural_join(self):
    key = self.find_common_attributes()
    if not key:
      print(f"No common attributes for {self.table1.name} and {self.table2.name}") 
      return
    return pd.merge(self.table1.rows, self.table2.rows, on=key)

  def union(self):
    if not self.same_attributes_tables():
      print(f"Dfferent attributes for {self.table1.name} and {self.table2.name}") 
      return
    print(self.table1.rows)
    print(self.table2.rows)
    return pd.merge(self.table1.rows, self.table2.rows, how='outer')
    
  def intersection(self):
    if not self.same_attributes_tables():
      print(f"Dfferent attributes for {self.table1.name} and {self.table2.name}") 
      return
    return pd.merge(self.table1.rows, self.table2.rows, how='inner')
    
  def difference(self):
    if not self.same_attributes_tables():
      print(f"Dfferent attributes for {self.table1.name} and {self.table2.name}") 
      return
    return pd.concat([self.table1.rows, self.table2.rows, self.table2.rows]).drop_duplicates(keep=False)
  