import sqlalchemy as sa
from ringo.model import Base
from ringo.model.base import BaseItem
from ringo.model.mixins import (
Owned
)

class Training(BaseItem, Owned, Base):
    __tablename__ = 'trainings'
    _modul_id = 1000
    id = sa.Column(sa.Integer, primary_key=True)
