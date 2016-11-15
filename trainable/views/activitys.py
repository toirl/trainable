#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config
from ringo.lib.helpers import get_action_routename
from ringo.views.base import update
from ringo.views.request import get_item_from_request
from ringo.views.response import JSONResponse

from trainable.model.activity import Activity
from trainable.views.strava import sync_activity


@view_config(route_name=get_action_routename(Activity, "sync"), renderer="/default/update.mako")
def syncwithstrava(request):
    """Will update the activity with strava in with all details."""
    request.item = sync_activity(request)
    _ = request.translate
    msg = _('The activity was successfully synchronized with Strava')
    request.session.flash(msg, "success")
    return update(request)

def a2gj(item):
    return [{
        "type": "Feature",
        "properties": {
            "id": item.id
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [[c[1], c[0]] for c in item.latlng_stream]}
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [item.latlng_stream[0][1], item.latlng_stream[0][0]]}
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [item.latlng_stream[-1][1], item.latlng_stream[-1][0]]}
    }]



@view_config(route_name="mapdata", renderer="json")
def mapdata(request):
    """Will return the track data of the activity as Geojson."""
    item = get_item_from_request(request)
    if item.has_streams:
        gj = a2gj(item)
    else:
        gj = {}
    return JSONResponse(True, gj)
