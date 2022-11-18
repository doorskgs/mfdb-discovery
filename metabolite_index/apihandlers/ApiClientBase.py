from abc import ABCMeta, abstractmethod

from ..dal import ExternalDBEntity


class ApiClientBase(metaclass=ABCMeta):

    @abstractmethod
    def fetch_api(self, edb_id) -> ExternalDBEntity:
        pass
