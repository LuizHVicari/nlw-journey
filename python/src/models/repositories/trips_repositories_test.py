from .trips_repositories import TripsRepository
from src.models.settings.db_connection_handler import db_connection_handler
import uuid
from datetime import datetime, timedelta
import pytest


db_connection_handler.connect()
id = str(uuid.uuid4())


@pytest.mark.skip(reason='interacao com o banco')
def test_create_trip():
  conn = db_connection_handler.get_connection()
  trips_repository = TripsRepository(conn)

  trips_infos = {
    'id' :id,
    'destination': 'Osasco',
    'start_date': datetime.strptime('02-01-2024', '%d-%m-%Y'),
    'end_date': datetime.strptime('02-01-2024', '%d-%m-%Y') + timedelta(days=5),
    'owner_name': 'Osvaldo',
    'owner_email': 'osvaldo@email.com'
  }

  trips_repository.create_trip(trips_infos)


@pytest.mark.skip(reason='interacao com o banco')
def test_find_trip():
  conn = db_connection_handler.get_connection()
  trips_repository = TripsRepository(conn)

  trip = trips_repository.find_trip_by_id(id)
  print(trip)


@pytest.mark.skip(reason='interacao com o banco')
def test_update_trip_statu():
  conn = db_connection_handler.get_connection()
  trips_repository = TripsRepository(conn)

  trip = trips_repository.update_trip_status(id)
  print(trip)



