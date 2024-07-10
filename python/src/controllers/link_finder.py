from typing import TypedDict, List

from src.models.repositories.links_repository import LinksRepository


FindTripErrorDict = TypedDict('FindTripErrorDict', {'error': str, 'message': str})
FindTripBodyDict = TypedDict('FindTripBodyDict', {'id': str, 'url': str, 'title': str})
FindTripDict = TypedDict('FindTripDict', {'body': List[FindTripBodyDict] | FindTripErrorDict, 'status_code': int})


class LinkFinder():
  def __init__(self, link_repository: LinksRepository) -> None:
    self.__link_repository = link_repository

  
  def find(self, tripId: str) -> FindTripDict:
    try:
      links = self.__link_repository.find_links_from_trip(tripId)

      formatted_links = [{
        'id': link[0],
        'url': link[2],
        'title': link[3]
        } for link in links]

      return {
        'body': {'links': formatted_links},
        'status_code': 200
      }

    except Exception as exception:
      return {
        'body': {'error': 'Bad Request', 'message': str(exception)},
        'status_code': 400
      }