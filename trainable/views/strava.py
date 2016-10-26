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
from trainable.model.training import Training

log = logging.getLogger(__name__)


@view_config(route_name="syncstrava")
def web_sync(request):
    sync(request)
    return HTTPFound(location=request.route_path("home"))


def get_access_token(request):
    """Returns the configured access token from the configuration"""
    settings = request.registry.settings
    return settings.get("strava.access_token")


def activity2training(activity):
    training = {}
    training["strava_id"] = activity.id
    training["title"] = activity.name
    training["distance"] = float(activity.distance)
    training["duration"] = serialize(activity.moving_time)
    training["elevation"] = float(activity.total_elevation_gain)
    if activity.type == "Run":
        training["sport"] = 1
    elif activity.type == "Ride":
        training["sport"] = 2
    elif activity.type == "Swim":
        training["sport"] = 3
    training["date"] = serialize(activity.start_date)
    training["heartrate"] = activity.average_heartrate
    return training


def sync(request):
    """Will sync the trainings with the workout stored on strava"""
    client = Client(access_token=get_access_token(request))
    trainings = []
    for activity in client.get_activities():
        trainings.append(activity2training(activity))
    importer = JSONImporter(Training)
    items = importer.perform(json.dumps(trainings),
                             request.user, use_uuid=False,
                             alternative_load_key="strava_id")
    imported_items = _handle_save(request, items, None)
    log.info("Synced with strava")
    return {}
