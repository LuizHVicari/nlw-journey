from typing import Dict, TypedDict
from uuid import uuid4

from src.models.repositories.trips_repositories import TripsRepository
from src.models.repositories.emails_to_invite_repository import EmailToInviteRepository


CreateTripDictType = TypedDict('CreateTripDictType', {'body': Dict, 'status_code': int})


class TripCreator(): 
  def __init__(self, trips_repository: TripsRepository, emails_repository: EmailToInviteRepository, *args, **kwargs):
    self.__trip_repository = trips_repository
    self.__emails_repository = emails_repository


  def create(self, body: Dict) -> CreateTripDictType:
    try:
      emails = body.get('emails_to_invite')
      
      trip_id = str(uuid4())
      trip_infos = {**body, 'id': trip_id}

      self.__trip_repository.create_trip(trip_infos)

      if emails:
        for email in emails:
          self.__emails_repository.register_email({
            'email': email,
            'trip_id': trip_id,
            'id': str(uuid4())
          })

      return {
        'body' : {'id': trip_id},
        'status_code': 201
      }
    
    except Exception as exception:
      return {
        'body': {'error' : 'Bad Request', 'message': str(exception)},
        'status_code' : 400
      }
