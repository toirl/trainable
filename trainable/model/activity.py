import json
import sqlalchemy as sa
from ringo.model import Base
from ringo.model.base import BaseItem
from ringo.model.mixins import (
    Owned
)
from ringo.lib.helpers import literal
from ringo_diagram.model import Dataprovider


class Json(sa.TypeDecorator):

    impl = sa.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)


def render_strava_sync_status(request, item, field, tableconfig):
    _ = request.translate
    if not item.strava_id:
        return ""
    elif not item.time_stream:
        filename = request.static_path('trainable:static/images/strava_sync.png')
        title = _("Activity basically synced with strava")
    else:
        filename = request.static_path('trainable:static/images/strava_full_sync.png')
        title = _("Activity completely synced with strava")
    return literal('<img src="{}" title="{}"/>'.format(filename, title))


class Activity(BaseItem, Owned, Base):
    __tablename__ = 'activitys'
    _modul_id = 1000
    id = sa.Column(sa.Integer, primary_key=True)
    strava_id = sa.Column(sa.Integer)
    """Id of the activity on Strava. Primarily used for syncing issues."""
    date = sa.Column('date', sa.DateTime)
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
    temperature = sa.Column('temperature', sa.Float)
    """Temperatur during the workout."""
    wind = sa.Column('wind', sa.Integer)
    """How windy was it during the activity"""
    weather = sa.Column('weather', sa.Integer)
    """How was the weather during your activity"""
    sleep = sa.Column('sleep', sa.Integer)
    """How well was the sleep of the athlet"""
    pain = sa.Column('pain', sa.Integer)
    """Was the activity acomplished under/with pain?"""
    restheartrate = sa.Column('restheartrate', sa.Integer)
    """What was the resting heartrate"""
    weight = sa.Column('weigth', sa.Float)
    """Was the activity acomplished under/with pain?"""

    # Streams from Strava. See https://strava.github.io/api/v3/streams/
    heartrate_stream = sa.Column('heartrate_stream', Json)
    """integer BPM"""
    time_stream = sa.Column('time_stream', Json)
    """floats seconds"""
    latlng_stream = sa.Column('latlng_stream', Json)
    """floats [latitude, longitude]"""
    distance_stream = sa.Column('distance_stream', Json)
    """float meters"""
    altitude_stream = sa.Column('altitude_stream', Json)
    """float meters"""
    velocity_smooth_stream = sa.Column('velocity_smooth_stream', Json)
    """float meters per second"""
    cadence_stream = sa.Column('cadence_stream', Json)
    """integer RPM"""
    watts_stream = sa.Column('watts_stream', Json)
    """integer watts"""
    temp_stream = sa.Column('temp_stream', Json)
    """integer degrees Celsius"""
    moving_stream = sa.Column('moving_stream', Json)
    """boolean"""
    grade_smooth_stream = sa.Column('grade_smooth_stream', Json)
    """float percent"""

    def render(self, request):
        # https://www.iconfinder.com/iconsets/sports-android-l-lollipop-icon-pack
        if self.sport == 1:
            img_url = request.static_path('trainable:static/images/sport_icons/running.png')
        elif self.sport == 2:
            img_url = request.static_path('trainable:static/images/sport_icons/regular_biking.png')
        else:
            img_url = request.static_path('trainable:static/images/sport_icons/swimming.png')
        out = []
        out.append('<img src="{}" style="width:55px;"/> '.format(img_url))
        out.append("{} ".format(self.title))
        out.append("<small>")
        out.append("{}".format(self.date))
        out.append("</small>")
        return literal("".join(out))

    @property
    def watts_per_kg(self):
        if self.weight and self.watts_stream:
            return round((sum(self.watts_stream)/len(self.watts_stream))/self.weight, 3)

    @property
    def has_streams(self):
        """Returns True if the activity is completely synced with
        strava. In this case there are streams available. In this case
        the time stream is available In this case the time stream is
        available."""
        return self.time_stream and len(self.time_stream) > 0

    @property
    def coord_lat(self):
        if self.latlng_stream and len(self.latlng_stream) > 0:
            return self.latlng_stream[0][0]

    @property
    def coord_lon(self):
        if self.latlng_stream and len(self.latlng_stream) > 0:
            return self.latlng_stream[0][1]

    @property
    def _has_streams(self):
        """Workaround for the form to make the information available if
        the activity has streams."""
        return self.has_streams

    @property
    def _heartrate_dataprovider(self):
        """Dataprovider for BPM"""
        dp = Dataprovider(self.distance_stream,
                          "",
                          "Distance [m]",
                          "Heartrate [bpm]")
        dp.add_series("Heartrate [bpm]", self.heartrate_stream)
        return dp

    @property
    def _velocity_dataprovider(self):
        """Dataprovider for Velocity"""
        dp = Dataprovider(self.distance_stream,
                          "",
                          "Distance [m]",
                          "Velocity [m/s]")
        dp.add_series("Velocity [m/s]", self.velocity_smooth_stream)
        return dp

    @property
    def _altitude_dataprovider(self):
        """Dataprovider for Altitude"""
        dp = Dataprovider(self.distance_stream,
                          "",
                          "Distance [m]",
                          "Altitude [m]")
        dp.add_series("Altitude [m]", self.altitude_stream)
        return dp

    @property
    def _cadence_dataprovider(self):
        """Dataprovider for Cadence"""
        dp = Dataprovider(self.distance_stream,
                          "",
                          "Distance [m]",
                          "Cadence [rpm]")
        dp.add_series("Cadence [m]", self.cadence_stream)
        return dp

    @property
    def _watts_dataprovider(self):
        """Dataprovider for Watts"""
        dp = Dataprovider(self.distance_stream,
                          "",
                          "Distance [m]",
                          "Power [W]")
        dp.add_series("Power [W]", self.watts_stream)
        return dp

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
