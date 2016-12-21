import datetime
import sqlalchemy as sa
from ringo.model import Base
from ringo.model.base import BaseItem, get_item_list
from ringo.model.mixins import (
    Owned
)


def week2activities(activities):
    w2a = {}
    for activity in activities:
        week = activity.date.isocalendar()[1]
        if week not in w2a:
            w2a[week] = []
        w2a[week].append(activity)
    return w2a


class MicroCycle(object):

    """A Microcyle is usually a week within a MesoCycle."""

    def __init__(self, hours, intensity):
        self.hours = hours
        self.intensity = intensity


class MesoCycle(object):
    """The Trainingyear (Saison) is devided into mesocycles. A mesocycle
    has usually a length from 2 up to 8 weeks. A mesocycle defines the
    weekly hours and intensity. By setting a start and end value for the
    intensity you can define an increasing, steady or decreasing
    workload of the mesocycle. Additionally there is a regeneration week
    which will be scheduled with 50% of the maximum intensity and hours
    of the mesocycle."""

    def __init__(self, name, length,
                 hours_start, hours_end,
                 intensity_start, intensity_end,
                 regeneration_length=1,
                 regeneration_hours=None, regeneration_intesity=None):
        self.name = name
        """Name of the Mesocycle e.g 'Foundation'"""

        # Calculate the weekly gain in hours and intensity within the
        # mesocycle.
        gain_hours = (float(hours_end) - hours_start) / (length-regeneration_length-1)
        gain_intesity = (float(intensity_end) - intensity_start) / (length-regeneration_length-1)

        # Now add a new Microcycle (Week) to the mesocycle with the
        # calculated intensity and hours.
        self.weeks = []
        for x in range(length-regeneration_length):
            hours = hours_start + (x * gain_hours)
            intensity = intensity_start + (x * gain_intesity)
            self.weeks.append(MicroCycle(hours, intensity))

        # In case the mesocycle has a configured regeneration than add
        # the regeneration also
        if regeneration_length > 0:
            # Set default regeneration hours and intensity based on the
            # maximum hours and intensity in with Mesocycle
            if regeneration_hours is None:
                regeneration_hours = hours_end * 0.5
            if regeneration_intesity is None:
                regeneration_intesity = intensity_end * 0.5

            for x in range(regeneration_length):
                self.weeks.append(MicroCycle(regeneration_hours, regeneration_intesity))


class Trainingplan(BaseItem, Owned, Base):
    __tablename__ = 'trainingplans'
    _modul_id = 1001
    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column('name', sa.String, nullable=False, default='')
    highlight_1_date = sa.Column('highlight_1_date', sa.Date)
    highlight_1_title = sa.Column('highlight_1_title', sa.String, nullable=False, default='')
    highlight_1_desc = sa.Column('highlight_1_desc', sa.String, nullable=False, default='')
    weekly_hours = sa.Column('weekly_hours', sa.Integer, nullable=False)

    def get_mesocycles(self):
        cycles = []
        cycles.append(MesoCycle("Foundation 0", 2, 5, 5, 8, 8,  regeneration_length=0))
        cycles.append(MesoCycle("Foundation 2", 4, 5, 7, 8, 8, regeneration_length=1))
        cycles.append(MesoCycle("Foundation 3", 4, 7, 8, 8, 8, regeneration_length=1))
        cycles.append(MesoCycle("Foundation 4", 4, 8, 9, 8, 10, regeneration_length=1))
        cycles.append(MesoCycle("Build 1", 4, 9, 10, 9, 14, regeneration_length=1))
        cycles.append(MesoCycle("Build 2", 4, 10, 10, 13, 14, regeneration_length=1))
        cycles.append(MesoCycle("Build 3", 4, 10, 9, 10, 10, regeneration_length=1))
        return cycles

    @property
    def start_date(self):
        return self.highlight_1_date - datetime.timedelta(days=7*self.length)

    @property
    def start_week(self):
        return self.start_date.isocalendar()[1]

    @property
    def end_date(self):
        return self.highlight_1_date

    @property
    def end_week(self):
        return self.end_date.isocalendar()[1]

    @property
    def length(self):
        cycles = self.get_mesocycles()
        return sum(len(c.weeks) for c in cycles)

    def get_weeks(self):
        weeks = []
        cycles = self.get_mesocycles()
        idx = 1
        for cycle in cycles:
            end = len(cycle.weeks) + idx
            weeks.extend(range(idx, end))
            idx = end
        return weeks

    def get_duration(self):
        durations = []
        cycles = self.get_mesocycles()
        for c in cycles:
            for w in c.weeks:
                durations.append(w.hours*60)
        return durations

    def get_activities_duration(self, activities):
        durations = []
        activities = week2activities(activities)
        for week in self.get_weeks():
            duration = datetime.timedelta(minutes=0)
            for a in activities.get(self.start_week + week-1, []):
                duration += a.duration
            durations.append(round(duration.total_seconds()/60))
        return durations

    def get_intensity(self):
        intensity = []
        cycles = self.get_mesocycles()
        for c in cycles:
            for w in c.weeks:
                intensity.append(w.intensity)
        return intensity

    def get_activities_intensity(self, activities):
        intensities = []
        activities = week2activities(activities)
        for week in self.get_weeks():
            intensity = 0
            week_activities = activities.get(self.start_week + week-1, [])
            for a in week_activities:
                intensity += a.intensity if a.intensity else 7
            if len(week_activities) > 0:
                intensities.append(intensity/len(week_activities))
            else:
                intensities.append(intensity)
        return intensities

    def get_pensum(self):
        pensum = []
        for p in zip(self.get_duration(), self.get_intensity()):
            pensum.append(p[0] * p[1])
        return pensum

    def get_activities_pensum(self, activities):
        pensum = []
        for p in zip(self.get_activities_duration(activities), self.get_activities_intensity(activities)):
            pensum.append(p[0] * p[1])
        return pensum
