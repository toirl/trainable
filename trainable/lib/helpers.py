#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ringo.model.base import get_item_list
from ringo_diagram.model import Dataprovider

from trainable.model.trainingplan import Trainingplan
from trainable.model.activity import Activity


def get_trainingplans_for_user(request):
    """TODO: Docstring for get_trainingplans_for_user.
    :returns: TODO
    """
    plans = get_item_list(request, Trainingplan, user=request.user)
    return plans.items


def get_activities_for_user(request, tp=None):
    activities = get_item_list(request, Activity, user=request.user)
    if tp:
        start_date = tp.start_date
        end_date = tp.end_date
        filter_stack = [(">= {}".format(start_date), "date", False),
                        ("<= {}".format(end_date), "date", False)]
        activities.filter(filter_stack)
    activities.sort(field="date", order="asc")
    return activities.items


def get_workload_for_trainingplan(request, tp, activities):
    """TODO: Docstring for get_workload_for_trainingplan.
    :returns: TODO
    """
    # Build Dataprovider with workload
    _ = request.translate
    dataprovider = Dataprovider(tp.get_weeks(), None, _("Week"), _("Workload"))
    dataprovider.add_series("Duration [min]", tp.get_duration())
    dataprovider.add_series("Training Duration [min]", tp.get_activities_duration(activities))
    dataprovider.add_series("Intensity [b]", tp.get_intensity())
    dataprovider.add_series("Training Intensity [b]", tp.get_activities_intensity(activities))
    return dataprovider
