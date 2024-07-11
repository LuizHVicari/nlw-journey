from typing import Dict

from src.models.repositories.activities_repository import ActivitiesRepository


class ActivityFinder():
  def __init__(self, activity_repository: ActivitiesRepository) -> None:
    self.__activity_repository = activity_repository

  
  def find_activity_from_trip(self, trip_id: str) -> Dict:
    try:
      activities = self.__activity_repository.find_activities_from_trip(trip_id)

      formatted_activities = [{
        'id': activity[0],
        'title': activity[2],
        'occurs_at': activity[3]
      } for activity in activities]
      
      return {
        'body': {'activities': formatted_activities},
        'status_code': 200}

    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      }