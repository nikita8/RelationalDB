class TableConstraints:
  def __init__(self, attributes):
    self.fds = set()
    self.attributes = attributes
    self.valid_fds = {}
    self.mvds = []
    self.boolean_constraints = []
    self.foreign_key_constraints = []
  
  def process_fds(self, fds):
    self.discarded_fds = {'trivial_fds' : set(), 'invalid_fds' : set(), 'superfluous_fds': set()}
    for fd in fds:
      fd = fd.strip()
      lhs, rhs = fd.split('->')
      if self.discard_fd(lhs, rhs):
        continue
      if len(rhs) > 1:
        self.transform_trivial_fd(lhs, rhs)
      else:
        self.add_valid_fds(lhs, rhs)
    self.discard_superfluous_fds()
  
  def discard_fd(self, lhs, rhs):
    if not lhs or not rhs: 
      self.add_invalid_fds('invalid_fds', lhs, rhs)
      return True 
    if len(rhs) == 1:
      return self.trivial_or_invalid_fd(lhs, rhs)
    return False

  def trivial_or_invalid_fd(self, lhs, rhs):
    invalid_attributes = set(lhs + rhs) - set(self.attributes)
    trivial = rhs in lhs
    if trivial:
      self.add_invalid_fds('trivial_fds', lhs, rhs)
      return True
    elif invalid_attributes:
      self.add_invalid_fds('invalid_fds', lhs, rhs)
      return True
    return False

  def transform_trivial_fd(self, lhs, rhs):
    for attribute in rhs:
      if not self.trivial_or_invalid_fd(lhs, rhs):
        self.add_valid_fds(lhs, attribute)

  def add_valid_fds(self, lhs, rhs):
    self.valid_fds[lhs] = self.valid_fds.get(lhs, set())
    self.valid_fds[lhs].add(rhs)
    self.fds.add(f"{lhs}->{rhs}")

  def remove_invalid_fds(self, lhs, rhs):
    self.valid_fds[lhs] = self.valid_fds.get(lhs, set())
    if len(self.valid_fds[lhs]) > 1:
      self.valid_fds[lhs].discard(rhs)
    else:
      del self.valid_fds[lhs]

  def add_invalid_fds(self, key, lhs, rhs):
    self.discarded_fds[key] = self.discarded_fds.get(key, set())
    self.discarded_fds[key].add(f"{lhs}->{rhs}")
  
  def discard_superfluous_fds(self):
    discarded_fds = set()
    fds = set(self.fds)
    for fd in fds:
      lhs, rhs = fd.split('->')
      if fd in discarded_fds: 
        continue
      remaining_fds = fds - {fd} - discarded_fds
      fd_closure = self.closure(lhs, remaining_fds)
      if set(rhs).issubset(fd_closure):
        if len(lhs) > 1:
          discarded_fds.add(fd)
          self.remove_invalid_fds(lhs, rhs)
          self.add_invalid_fds('superfluous_fds', lhs, rhs)
        else:
          weaker_fds = set()
          lhs_attributes = self.valid_fds.keys()
          for attr in lhs_attributes:
            if set(lhs).issubset(set(attr)) and set(lhs) != set(attr):
              weaker_fds.add(attr)
          if not weaker_fds: 
            discarded_fds.add(fd)
            self.add_invalid_fds('superfluous_fds', lhs, rhs)
    self.fds = self.fds - discarded_fds
  
  def closure(self, seed, computing_fds):
    print("seed:", seed)
    seed_closure = set(seed.strip()) - {'-', '>', ' '}
    valid_fds = set(computing_fds or self.fds)
    found_fds = set()
    found_all_closure = False
    while not found_all_closure:
      found_all_closure = True
      for fd in valid_fds:
        lhs, rhs = fd.split('->')
        if set(lhs).issubset(seed_closure):
          seed_closure.add(rhs)
          found_fds.add(fd)
          found_all_closure = False
      valid_fds = valid_fds - found_fds
    return seed_closure

# tc = TableConstraints('ABC')
# tc.process_fds(['A->B', 'AB->C', 'B->C'])
# print(tc.discarded_fds)
# print(tc.fds)