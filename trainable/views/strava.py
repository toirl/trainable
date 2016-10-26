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
from ringo.model.base import get_item_list
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


def get_activity_type(training):
    if training.sport == 1:
        return "Run"
    elif training.sport == 2:
        return "Ride"
    elif training.sport == 3:
        return "Swim"


def get_training_type(activity):
    if activity.type == "Run":
        return 1
    elif activity.type == "Ride":
        return 2
    elif activity.type == "Swim":
        return 3


def activity2training(activity):
    training = {}
    training["strava_id"] = activity.id
    training["title"] = activity.name
    training["distance"] = float(activity.distance)
    training["duration"] = serialize(activity.moving_time)
    training["elevation"] = float(activity.total_elevation_gain)
    training["sport"] = get_training_type(activity)
    training["date"] = serialize(activity.start_date)
    training["heartrate"] = activity.average_heartrate
    return training


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
    trainings = []
    for activity in client.get_activities():
        trainings.append(activity2training(activity))
    importer = JSONImporter(Training)
    items = importer.perform(json.dumps(trainings),
                             request.user, load_key="strava_id")
    return _handle_save(request, items, None)


def update_strava(request):
    """Will upload all training entries which are not yet uploaded to
    strava to strava."""
    client = Client(access_token=get_access_token(request))
    trainings = get_item_list(request, Training)
    for training in trainings:
        # If the strava_id is None than the training as not uploaded
        # before.
        if training.strava_id is None:
            log.debug("Upload of traing {id} to strava".format(id=training.id))
            activity = client.create_activity(training.title,
                                              get_activity_type(training),
                                              training.date,
                                              training.duration.seconds,
                                              training.description,
                                              training.distance)
            training.strava_id = activity.id


def sync(request):
    """Will sync the trainings with the workout stored on strava"""
    # Update Strava
    update_strava(request)
    # Update trainable
    update_trainable(request)
    log.info("Synced with strava")
    return {}
