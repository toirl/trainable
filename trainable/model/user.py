import sqlalchemy as sa
from ringo.model.user import (
    Profile,
    User
)


class TrainableUser(User):
    """User to set a custom relation to the profile."""
    profile = sa.orm.relation("TrainableProfile", cascade="all, delete-orphan")


class TrainableProfile(Profile):
    """Profile for the user with Strava specific attributes."""

    strava_client_id = sa.Column(sa.String)
    strava_access_key = sa.Column(sa.String)
