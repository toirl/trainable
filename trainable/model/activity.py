import sqlalchemy as sa
from ringo.model import Base
from ringo.model.base import BaseItem
from ringo.model.mixins import (
    Owned
)


class Activity(BaseItem, Owned, Base):
    __tablename__ = 'activitys'
    _modul_id = 1000
    id = sa.Column(sa.Integer, primary_key=True)
    strava_id = sa.Column(sa.Integer)
    """Id of the activity on Strava. Primarily used for syncing issues."""
    date = sa.Column('date', sa.Date)
    """Date of the training"""
    duration = sa.Column('duration', sa.Interval)
    """Duration of the training"""
    sport = sa.Column('sport', sa.Integer)
    """Which sport was trainined"""
    rating = sa.Column('rating', sa.Integer)
    """Subjective rating of the training. How well was the trainig?"""
    intensity = sa.Column('intensity', sa.Integer)
    """Subjective rating of the training. How intense was the training.
    Used to calculate the workload of your training. Intensity is
    calculated using the  The Borg Scale of Perceived Exertion:

        6 - None (Reading a Book)
        7,8 - Very, Very light (Binding shoes)
        9,10 - Very light (Easy tasks like folding clothes)
        11,12 - Fairly Light (Light speed up breathing)
        13,14 - Somewhat hard (Still can speak)
        15,16 - Hard (Breating fast)
        17,18 - Very hard (Highest level of activity you can sustain)
        19,20 - Very, Very Hard (Maximum, can not maintain this for long time)

    For information on
    https://www.hsph.harvard.edu/nutritionsource/borg-scale/
    """
    distance = sa.Column('distance', sa.Integer)
    """Distance in training in meters"""
    elevation = sa.Column('elevation', sa.Integer)
    """Accumulated elevation in training in meters"""
    heartrate = sa.Column('heartrate', sa.Integer)
    """Averange hearrate"""
    title = sa.Column('title', sa.String, nullable=False, default='')
    """A title for the training"""
    description = sa.Column('description', sa.String, nullable=False, default='')
    """A short description of the training"""

    @property
    def speed(self):
        """Returns the averange speed in this training"""
        if self.distance and self.duration:
            # calculate meters per second
            mps = float(self.distance) / self.duration.seconds
            # calculate meters per hour
            mph = mps * 60 * 60
            # calculate meters per hour
            kmph = mph / 1000
            return round(kmph, 2)
        return ""
