import sqlalchemy as sa
from ringo.model import Base
from ringo.model.base import BaseItem
from ringo.model.mixins import (
Owned
)

class Trainingplan(BaseItem, Owned, Base):
    __tablename__ = 'trainingplans'
    _modul_id = 1001
    id = sa.Column(sa.Integer, primary_key=True)
