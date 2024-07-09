import pytest
import uuid
from src.models.settings.db_connection_handler import db_connection_handler

from .emails_to_invite_repository import EmailToInviteRepository
from .links_repository import LinksRepository, LinkInfoDict


db_connection_handler.connect()
trip_id = str(uuid.uuid4())
link_id = str(uuid.uuid4())


@pytest.mark.skip(reason='interacao com o banco')
def test_registry_link():
  conn = db_connection_handler.get_connection()
  link_repository = LinksRepository(conn)

  link_infos : LinkInfoDict = {
    'id': link_id,
    'trip_id': trip_id,
    'link': 'link.com',
    'title': 'Hotel'
  }

  link_repository.register_link(link_infos)


@pytest.mark.skip(reason='interacao com o banco')
def test_find_links_from_trip():
  conn = db_connection_handler.get_connection()
  link_repository = LinksRepository(conn)

  response = link_repository.find_links_from_trip(trip_id)
  print(response)

  assert isinstance(response, list)
  assert isinstance(response[0], tuple)