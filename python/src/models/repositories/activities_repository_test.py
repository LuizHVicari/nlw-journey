import uuid
import pytest
from datetime import datetime

from src.models.settings.db_connection_handler import db_connection_handler
from .activities_repository import ActivitiesRepository, ActivityInfoDict

db_connection_handler.connect()
trip_id = str(uuid.uuid4())

@pytest.mark.skip(reason='interacao com o banco')
def test_register_activity():
  conn = db_connection_handler.get_connection()
  activities_repository = ActivitiesRepository(conn)

  activity_infos: ActivityInfoDict = {
    'id': str(uuid.uuid4()),
    'trip_id': trip_id,
    'title': 'super título',
    'occurs_at': datetime.strptime('02-01-2024', '%d-%m-%Y')
  }

  activities_repository.register_activity(activity_infos)


@pytest.mark.skip(reason='interacao com o banco')
def test_find_activities_from_trip():
  conn = db_connection_handler.get_connection()
  activities_repository = ActivitiesRepository(conn)

  activities = activities_repository.find_activities_from_trip(trip_id)
