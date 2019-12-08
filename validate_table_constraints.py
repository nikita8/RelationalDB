
class ValidateTableConstraints:
  def __init__(self, table, data=[]):
    self.table = table
    self.data = data

  def call(self):
    if self.violate_fds:
      return False, { 'violating_fds': self.violating_fds }
    elif self.is_duplicate_key():
      key_data = { k:v for k,v in self.data.items() if k in self.key }
      # print(f"Duplicate Key: {key_data} already exist in the table.")
      return False, { "duplicate_key" : key_data }
    elif self.demands_new_tuple_in_other_tables():
      return False, { "foreign_key_constraint" : {'table' : self.foreign_table } }
    else:
      return True, None
  
  def is_duplicate_key(self):
    self.key = list(self.table.key)
    query = ' and '.join([f'{k}=="{v}"' for k, v in self.data.items() if k in key])
    return self.table.rows.query(query).all(axis=1).any()

  def violate_fds(self):
    self.violating_fds = []
    return False
  
  def demands_new_tuple_in_other_tables(self):
    self.foreign_table = ''
    pass
