#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config
from ringo.lib.helpers import get_action_routename
from ringo.views.base import update

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
