class IdNotFoundError(RuntimeError):
  def __init__(self, id):
    self.id = id

  def __repl__(self):
    return "Id: {}".format(self.id)
