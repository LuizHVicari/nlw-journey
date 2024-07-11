from typing import Dict

from src.models.repositories.participants_repository import ParticipantsRepository


class ParticipantFinder():
  def __init__(self, participant_repository: ParticipantsRepository) -> None:
    self.__participant_repository = participant_repository

  
  def find_participants_from_trip(self, trip_id) -> Dict:
    try:
      participants = self.__participant_repository.find_participants_from_trip(trip_id)

      participants_infos = [{
        'id': participant[0],
        'name': participant[1],
        'is_confirmed': participant[2],
        'email': participant[3]
        } for participant in participants]
      
      return {
        'body': {'participants': participants_infos},
        'status_code': 200}

    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      }