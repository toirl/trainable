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

    name = sa.Column('name', sa.String, nullable=False, default='')
    highlight_1_date = sa.Column('highlight_1_date', sa.Date)
    highlight_1_title = sa.Column('highlight_1_title', sa.String, nullable=False, default='')
    highlight_1_desc = sa.Column('highlight_1_desc', sa.String, nullable=False, default='')
    weekly_hours = sa.Column('weekly_hours', sa.Integer, nullable=False)

    def get_mondays(self):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def get_duration(self):
        return [2, 2, 3, 3, 4, 5, 4, 3, 2, 2]

    def get_intensity(self):
        return [1, 1, 2, 2, 2, 2, 3, 4, 4, 2]

    def get_pensum(self):
        pensum = []
        for p in zip(self.get_duration(), self.get_intensity()):
            pensum.append(p[0] * p[1])
        return pensum
