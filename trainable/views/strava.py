#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
from stravalib import Client

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from ringo.lib.imexport import JSONImporter
from ringo.lib.helpers import serialize
from ringo.views.base.import_ import _handle_save
from ringo.views.home import index_view
from ringo.model.base import get_item_list

from trainable.model.activity import Activity

log = logging.getLogger(__name__)


@view_config(route_name="syncstrava")
def web_sync(request):
    sync(request)
    return HTTPFound(location=request.route_path("home"))


@view_config(route_name='authstrava', renderer='/index.mako')
def strava_authorisation_view(request):
    values = index_view(request)
    code = request.GET.get("code")
    client = Client()
    client_id = request.user.profile[0].strava_client_id
    client_secret = request.registry.settings.get("strava.client_secret")
    access_token = client.exchange_code_for_token(client_id=client_id,
                                                  client_secret=client_secret,
                                                  code=code)
    request.user.profile[0].strava_access_key = access_token
    request.session.flash("Authorized client", "success")
    return values


def get_access_token(request):
    """Returns the configured access token from the configuration"""
    return request.user.profile[0].strava_access_key


def get_strava_activity_type(trainable):
    if trainable.sport == 1:
        return "Run"
    elif trainable.sport == 2:
        return "Ride"
    elif trainable.sport == 3:
        return "Swim"


def get_trainable_activity_type(strava):
    if strava.type == "Run":
        return 1
    elif strava.type == "Ride":
        return 2
    elif strava.type == "Swim":
        return 3


def strava2trainable(strava):
    trainable = {}
    trainable["strava_id"] = strava.id
    trainable["title"] = strava.name
    trainable["distance"] = float(strava.distance)
    trainable["duration"] = serialize(strava.moving_time)
    trainable["elevation"] = float(strava.total_elevation_gain)
    trainable["sport"] = get_trainable_activity_type(strava)
    trainable["date"] = serialize(strava.start_date)
    trainable["heartrate"] = strava.average_heartrate
    return trainable


def get_new_and_updated_activities(request, trainings, activities):
    """Will return a list with activity items from strava which seems to
    be not existant or newer than the ones in the trainable database."""

    for a in activities:
        print(a.external_id)
        print(a.upload_id)


def update_trainable(request):
    """Will update and create new trainable entries based on the data on
    strava."""
    client = Client(access_token=get_access_token(request))
    activities = []
    for activity in client.get_activities():
        activities.append(strava2trainable(activity))
    importer = JSONImporter(Activity)
    items = importer.perform(json.dumps(activities),
                             request.user, load_key="strava_id")
    return _handle_save(request, items, None)


def update_strava(request):
    """Will upload all training entries which are not yet uploaded to
    strava to strava."""
    client = Client(access_token=get_access_token(request))
    activities = get_item_list(request, Activity)
    for activity in activities:
        # If the strava_id is None than the activity as not uploaded
        # before.
        if activity.strava_id is None:
            log.debug("Upload of traing {id} to strava".format(id=activity.id))
            strava = client.create_activity(activity.title,
                                            get_strava_activity_type(activity),
                                            activity.date,
                                            activity.duration.seconds,
                                            activity.description,
                                            activity.distance)
            activity.strava_id = strava.id


def sync(request):
    """Will sync the trainings with the workout stored on strava"""
    # Update Strava
    update_strava(request)
    # Update trainable
    update_trainable(request)
    log.info("Synced with strava")
    return {}