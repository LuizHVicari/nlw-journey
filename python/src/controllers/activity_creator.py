from uuid import uuid4
from typing import Dict

from src.models.repositories.activities_repository import ActivitiesRepository, ActivityInfoDict


class ActivityCreator:
  def __init__(self, activities_repository: ActivitiesRepository) -> None:
    self.__activities_repository = activities_repository

  
  def create(self, body: dict, trip_id: str) -> Dict:
    try:
      id = str(uuid4())
      activity_infos : ActivityInfoDict = {
        'id': id,
        'trip_id': trip_id,
        'title': body['title'],
        'occurs_at' : body['occurs_at']
      }

      self.__activities_repository.register_activity(activity_infos)

      return {
        'body': {'activityId': id},
        'status_code': 201
      }
  
    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      } 