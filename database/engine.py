import sqlite3 as sql


class Engine:
  def __init__(self):
    self._conn = sql.connect("Railway.db")
    def query(self, file, statement):
    pass
