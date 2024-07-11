from uuid import uuid4
from typing import Dict

from src.models.repositories.emails_to_invite_repository import EmailToInviteRepository, EmailInfoDict
from src.models.repositories.participants_repository import ParticipantsRepository, ParticipantsInfoDict


class ParticipantCreator():
  def __init__(self, participants_repository: ParticipantsRepository, email_repository: EmailToInviteRepository):
    self.__participants_repository = participants_repository
    self.__email_repository = email_repository

  
  def create(self, body: dict, trip_id: str) -> Dict:
    try:
      participant_id = str(uuid4())
      email_id = str(uuid4())

      email_infos: EmailInfoDict = {
        'id': email_id,
        'email': body['email'],
        'trip_id': trip_id
      }

      participant_infos: ParticipantsInfoDict = {
        'id': participant_id,
        'trip_id': trip_id,
        'emails_to_invite_id': email_id,
        'name': body['name']
      }

      self.__email_repository.register_email(email_infos)
      self.__participants_repository.register_participants(participant_infos)

      return {
        'body': {'participantId': participant_id},
        'status_code': 201
      }
  
    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      } 
