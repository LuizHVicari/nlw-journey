import uuid
import pytest
from datetime import datetime

from src.models.settings.db_connection_handler import db_connection_handler
from .participants_repository import ParticipantsRepository, ParticipantsInfoDict

db_connection_handler.connect()
trip_id = str(uuid.uuid4())
email_id = str(uuid.uuid4())
p_id = str(uuid.uuid4())


# @pytest.mark.skip(reason='interacao com o banco')
def test_register_participants():
  conn = db_connection_handler.get_connection()
  participants_repository = ParticipantsRepository(conn)

  pariticipant_infos: ParticipantsInfoDict = {
    'id': p_id,
    'trip_id': trip_id,
    'emails_to_invite_id': email_id,
    'name': 'nome'
  }

  participants_repository.register_participants(pariticipant_infos)


@pytest.mark.skip(reason='interacao com o banco')
def test_find_participants_from_trip():
  conn = db_connection_handler.get_connection()
  participants_repository = ParticipantsRepository(conn)

  participants_repository.find_participants_from_trip(trip_id)


def test_update_participant_status():
  conn = db_connection_handler.get_connection()
  participants_repository = ParticipantsRepository(conn)

  participant = participants_repository.update_participant_status(p_id)
  

