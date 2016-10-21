#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

log = logging.getLogger(__name__)


@view_config(route_name="syncstrava")
def web_sync(request):
    sync(request)
    return HTTPFound(location=request.route_path("home"))


def sync(request):
    """Will sync the trainings with the workout stored on strava"""
    log.info("Synced with strava")
    return {}
