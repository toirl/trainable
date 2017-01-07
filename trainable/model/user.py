import sqlalchemy as sa
from ringo.model.user import (
    Profile,
    User,
    Usergroup,
    nm_user_usergroups
)


class TrainableUser(User):
    """User to set a custom relation to the profile."""
    profile = sa.orm.relation("TrainableProfile", cascade="all, delete-orphan")
    usergroup = sa.orm.relationship("TrainableUsergroup", uselist=False, cascade="delete, all", foreign_keys=[User.default_gid])


class TrainableUsergroup(Usergroup):
    """User to set a custom relation to the profile."""
    members = sa.orm.relationship("TrainableUser", secondary=nm_user_usergroups)


class TrainableProfile(Profile):
    """Profile for the user with Strava specific attributes."""

    strava_client_id = sa.Column(sa.String)
    strava_access_key = sa.Column(sa.String)
    max_heartrate = sa.Column(sa.Integer)
