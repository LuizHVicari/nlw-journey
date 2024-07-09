from sqlite3 import Connection
from typing import TypedDict, Tuple

TripInfoDict = TypedDict('TripInfoDict', {'id': str, 'destination': str, 'start_date': str, 'end_date': str, 'owner_name': str, 'owner_email': str})

class TripsRepository:
  def __init__(self, conn: Connection) -> None:
    self.__conn = conn

  def create_trip(self, trips_infos: TripInfoDict) -> None:
    cursor = self.__conn.cursor()
    cursor.execute(
      '''
      INSERT INTO trips (id, destination, start_date, end_date, owner_name, owner_email)
        VALUES
          (?, ?, ?, ?, ?, ?)
      ''',
      (
        trips_infos['id'],
        trips_infos['destination'],
        trips_infos['start_date'],
        trips_infos['end_date'],
        trips_infos['owner_name'],
        trips_infos['owner_email'],
      )
    )
    self.__conn.commit()

  
  def find_trip_by_id(self, trip_id: str) -> Tuple:
    cursor =  self.__conn.cursor()
    cursor.execute(
      '''
      SELECT * FROM trips WHERE id = ?
      ''',
      (trip_id, )
    )
    return cursor.fetchone()
  
  
  def update_trip_status(self, trip_id: str) -> None:
    cursor = self.__conn.cursor()
    cursor.execute(
      '''
      UPDATE trips
        SET status = 1
      WHERE
        id = ?
      ''',
      (trip_id, )
    )
    self.__conn.commit()