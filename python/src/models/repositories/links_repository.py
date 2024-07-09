from sqlite3 import Connection
from typing import TypedDict, List, Tuple

LinkInfoDict = TypedDict('LinkInfoDict', {'id': str, 'trip_id': str, 'link': str, 'title': str})


class LinksRepository:
  def __init__(self, conn: Connection) -> None:
    self.__conn = conn

  def register_link(self, link_infos: LinkInfoDict) -> None:
    cursor = self.__conn.cursor()
    cursor.execute(
      '''
      INSERT INTO links (id, trip_id, link, title)
        VALUES
          (?, ?, ?, ?)
      ''',
      (
       link_infos['id'],
       link_infos['trip_id'],
       link_infos['link'],
       link_infos['title']
      )
    )
    self.__conn.commit()

  
  def find_links_from_trip(self, trip_id: str) -> List[Tuple]:
    cursor =  self.__conn.cursor()
    cursor.execute(
      '''
      SELECT * FROM links WHERE trip_id = ?
      ''',
      (trip_id, )
    )
    return cursor.fetchall()
  
