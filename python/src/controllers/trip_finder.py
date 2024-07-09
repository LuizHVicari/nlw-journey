from typing import TypedDict

from src.models.repositories.trips_repositories import TripsRepository

FindTripErrorDict = TypedDict('FindTripBodyDict', {'error': str, 'message': str})
FindTripBodyDict = TypedDict('FindTripBodyDict', {'id': str, 'destination': str, 'starts_at': str, 'ends_at': str, 'status': str})
FindTripDict = TypedDict('FindTripDict', {'body': FindTripBodyDict | FindTripErrorDict, 'status_code': int})

class TripFinder():
  def __init__(self, trips_repository: TripsRepository, *args, **kwargs):
    self.__trips_repository = trips_repository

  
  def find_trip_details(self, trip_id: str) -> FindTripDict:
    try:
      trip = self.__trips_repository.find_trip_by_id(trip_id)
      if not trip: raise Exception('No trip found')

      return {
        'body': {
          'trip': {
            'id': trip[0],
            'destination': trip[1],
            'starts_at': trip[2],
            'ends_at': trip[3],
            'status': trip[6],
          },
        },
        'status_code': 200
      }
    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      }
  