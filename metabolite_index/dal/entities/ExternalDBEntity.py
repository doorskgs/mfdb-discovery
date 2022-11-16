from .MetaboliteMixin import MetaboliteMixin
from .sqlbase import EntityBase


class ExternalDBEntity(MetaboliteMixin, EntityBase):
    __tablename__ = 'edb'

    def __init__(self, **kwargs):
        self.meta_id = kwargs.get('meta_id')
