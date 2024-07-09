import uuid
import pytest
from src.models.settings.db_connection_handler import db_connection_hanlder
from .emails_to_invite_repository import EmailToInviteRepository

db_connection_hanlder.connect()
trip_id = str(uuid.uuid4())

@pytest.mark.skip(reason='interacao com o banco')
def test_register_email():
  conn = db_connection_hanlder.get_connection()
  emails_to_invite_repository = EmailToInviteRepository(conn)

  email_trips_infos = {
    'id': str(uuid.uuid4()),
    'trip_id': trip_id,
    'email' : 'email@email.com'
  }

  emails_to_invite_repository.register_email(email_trips_infos)


@pytest.mark.skip(reason='interacao com o banco')
def test_find_emails_from_trip():
  conn = db_connection_hanlder.get_connection()
  emails_to_invite_repository = EmailToInviteRepository(conn)

  emails = emails_to_invite_repository.find_emails_from_trip(trip_id)
  print(emails)
