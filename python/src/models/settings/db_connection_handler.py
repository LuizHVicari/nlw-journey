import sqlite3

class DbConnectionHanlder:
  
  def __init__(self) -> None:
    self.__connection_string = "storage.db"
    self.__conn = None

  def connect(self) -> None:
    conn = sqlite3.connect(self.__connection_string, check_same_thread=False)
    self.__conn = conn

  def get_connection(self) -> sqlite3.Connection:
    return self.__conn
  
db_connection_handler = DbConnectionHanlder()
  