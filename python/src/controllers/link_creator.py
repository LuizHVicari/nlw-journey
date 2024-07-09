from typing import TypedDict, Dict
from uuid import uuid4

from src.models.repositories.links_repository import LinksRepository


CreateLinkErrorDict = TypedDict('CreateLinkErrorDict', {'error': str, 'message': str})
CreateLinkBodyDict = TypedDict('CreateLinkBodyDict', {'linkId': str})
CreateLinkDict = TypedDict('CreateLinkDict', {'body': CreateLinkBodyDict | CreateLinkErrorDict, 'status_code': int})


class LinkCreator():
  def __init__(self, link_repository: LinksRepository) -> None:
    print('aqui')

    self.__link_repository = link_repository

  
  def create(self, body: Dict, trip_id) -> CreateLinkDict:
    try: 
      link_id = str(uuid4())
      link_infos = {
        'link': body['url'],
        'title': body['title'],
        'id': link_id,
        'trip_id': trip_id
      }
      self.__link_repository.register_link(link_infos)
      return {
        'body' : {'linkId': link_id},
        'status_code': 201
      }
    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      }