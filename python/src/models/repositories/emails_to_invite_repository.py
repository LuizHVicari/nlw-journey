from sqlite3 import Connection
from typing import TypedDict, List, Tuple

EmailInfoDict = TypedDict('EmailInfoDict', {'id': str, 'trip_id': str, 'email': str})

class EmailToInviteRepository:
  def __init__(self, conn: Connection) -> None:
    self.__conn = conn

  def register_email(self, email_infos: EmailInfoDict) -> None:
    cursor = self.__conn.cursor()
    cursor.execute(
      '''
      INSERT INTO email_to_invite (id, trip_id, email)
        VALUES
          (?, ?, ?)
      ''',
      (
        email_infos['id'],
        email_infos['trip_id'],
        email_infos['email'],
      )
    )
    self.__conn.commit()

  
  def find_emails_from_trip(self, trip_id: str) -> List[Tuple]:
    cursor =  self.__conn.cursor()
    cursor.execute(
      '''
      SELECT * FROM email_to_invite WHERE trip_id = ?
      ''',
      (trip_id, )
    )
    return cursor.fetchall()
  
