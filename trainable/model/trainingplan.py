import re
import datetime
import sqlalchemy as sa
from ringo.model import Base
from ringo.model.base import BaseItem
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


def split_code(code):
    """Code for trainingsplan is formated in a specific format. There
    are different phases in the plan which are devided by a '-' sign.
    Each of this phases is divided by '*' where the first part defines
    how often the phase will be repeated and the second part defines
    details on the phase phase itself (Type, length in weeks etc). The
    details are irrelevant in the this place and are handled later in
    the
    get_mesocycle_factory."""
    for phase in code.split("-"):
        repetitions, phase = phase.split("*")
        repetitions = int(repetitions)
        for r in range(repetitions):
            yield (phase, r, repetitions)


def get_start_end(hours, start, end, length, current_repeat):
    start_hours = hours*start
    end_hours = hours*end
    total_gain = end_hours - start_hours
    gain_per_week = total_gain / length

    return (round(start_hours + (current_repeat * gain_per_week), 2),
            round(start_hours + ((current_repeat+1) * gain_per_week), 2))


def maintainance_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration):
    name = "Maintainance {}".format(repeat)
    intensity = 10
    start_hours, end_hours = get_start_end(weekly_hours, 1.0, 1.0, repetitions, repeat)
    start_intensity, end_intensity = get_start_end(intensity, 1.0, 1.0, repetitions, repeat)
    return MesoCycle(name, int(length_phase),
                     start_hours, end_hours,
                     start_intensity, end_intensity,
                     regeneration_length=int(length_regeneration))


def preparation_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration):
    name = "Preparation {}".format(repeat)
    intensity = 10
    start_hours, end_hours = get_start_end(weekly_hours, 0.5, 0.5, repetitions, repeat)
    start_intensity, end_intensity = get_start_end(intensity, 1.0, 1.0, repetitions, repeat)
    return MesoCycle(name, int(length_phase),
                     start_hours, end_hours,
                     start_intensity, end_intensity,
                     regeneration_length=int(length_regeneration))


def foundation_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration):
    name = "Founddation {}".format(repeat)
    intensity = 13
    start_hours, end_hours = get_start_end(weekly_hours, 0.5, 0.7, repetitions, repeat)
    start_intensity, end_intensity = get_start_end(intensity, 0.8, 1.0, repetitions, repeat)
    return MesoCycle(name, int(length_phase),
                     start_hours, end_hours,
                     start_intensity, end_intensity,
                     regeneration_length=int(length_regeneration))


def build_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration):
    name = "Build {}".format(repeat)
    intensity = 16
    start_hours, end_hours = get_start_end(weekly_hours, 0.7, 1.0, repetitions, repeat)
    start_intensity, end_intensity = get_start_end(intensity, 0.8, 1.0, repetitions, repeat)
    return MesoCycle(name, int(length_phase),
                     start_hours, end_hours,
                     start_intensity, end_intensity,
                     regeneration_length=int(length_regeneration))


def get_mesocycle_factory(phase, repetitions, repeat, weekly_hours):

    maintainance = re.compile("(\d{1})M(\d{1})R")
    preparation = re.compile("(\d{1})P(\d{1})R")
    foundation = re.compile("(\d{1})F(\d{1})R")
    build = re.compile("(\d{1})B(\d{1})R")

    length_phase = 4
    length_regeneration = 1

    def get_length(match):
        return match.group(1), match.group(2)

    is_maintainance = maintainance.match(phase)
    if is_maintainance:
        length_phase, length_regeneration = get_length(is_maintainance)
        return maintainance_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration)

    is_preparation = preparation.match(phase)
    if is_preparation:
        length_phase, length_regeneration = get_length(is_preparation)
        return preparation_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration)

    is_foundation = foundation.match(phase)
    if is_foundation:
        length_phase = is_foundation.group(1)
        length_regeneration = is_foundation.group(2)
        return foundation_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration)

    is_build = build.match(phase)
    if is_build:
        length_phase = is_build.group(1)
        length_regeneration = is_build.group(2)
        return build_mescycle_factory(repeat, repetitions, weekly_hours, length_phase, length_regeneration)


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
    category = sa.Column('category', sa.Integer, nullable=False)
    plan = sa.Column('plan', sa.String)

    def get_mesocycles(self):
        plans = {
                    "1": "1*2P0R-3*4F1R-3*4B1R",
                    "2": "3*8M1R"
                }
        if self.category == 0:
            plan_code = self.plan
        else:
            plan_code = plans[str(self.category)]
        cycles = []
        for phase, repeat, repetitions in split_code(plan_code):
            cycles.append(get_mesocycle_factory(phase, repetitions, repeat, self.weekly_hours))
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

    def get_start_end(self):
        intensity = []
        cycles = self.get_mesocycles()
        for c in cycles:
            for w in c.weeks:
                intensity.append(w.intensity)
        return intensity

    def get_intensity(self):
        intensities = []
        cycles = self.get_mesocycles()
        for c in cycles:
            for w in c.weeks:
                intensities.append(w.intensity)
        return intensities

    def get_activities_intensity(self, activities):
        intensities = []
        activities = week2activities(activities)
        for week in self.get_weeks():
            intensity = 0
            week_activities = activities.get(self.start_week + week-1, [])
            for a in week_activities:
                intensity += a._intensity if a._intensity else 7
            if len(week_activities) > 0:
                intensities.append(intensity/len(week_activities))
            else:
                intensities.append(intensity)
        return intensities

    def get_pensum(self):
        pensum = []
        for p in zip(self.get_duration(), self.get_start_end()):
            pensum.append(p[0] * p[1])
        return pensum

    def get_activities_pensum(self, activities):
        pensum = []
        for p in zip(self.get_activities_duration(activities), self.get_activities_intensity(activities)):
            pensum.append(p[0] * p[1])
        return pensum
