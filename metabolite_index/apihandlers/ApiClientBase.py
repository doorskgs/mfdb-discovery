from abc import ABCMeta, abstractmethod

from ..views.MetaboliteConsistent import MetaboliteConsistent


class ApiClientBase(metaclass=ABCMeta):

    @abstractmethod
    def fetch_api(self, edb_id) -> MetaboliteConsistent:
        pass
