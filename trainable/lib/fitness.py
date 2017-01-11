#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from ringo_diagram.model import Dataprovider
from datetime import timedelta, date

"""Module to calculate CTL, ATL and TSB. Calculation are basically based
on Jürgen Pansky's blog entry.
See: http://jpansy.at/2014/09/09/ctl-atl-tsb-erklaert/"""


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + timedelta(n)

def build_intensity_trend(activities):
    start_date = activities[0].date.date()
    end_date = date.today()

    days = collections.OrderedDict()
    for day in daterange(start_date, end_date):
        days[str(day)] = 0

    for activity in activities:

        days[str(activity.date.date())] += activity.trimp

    return days

def get_form(request, activities):
    """TODO: Docstring for get_workload_for_trainingplan.
    :returns: TODO
    """
    # Build Dataprovider with workload
    _ = request.translate
    print(build_intensity_trend(activities))
    #dataprovider = Dataprovider(tp.get_weeks(), None, _("Week"), _("Workload"))
    #dataprovider.add_series("Duration [min]", tp.get_duration())
    #dataprovider.add_series("Training Duration [min]", tp.get_activities_duration(activities))
    #dataprovider.add_series("Intensity [b]", tp.get_intensity())
    #dataprovider.add_series("Training Intensity [b]", tp.get_activities_intensity(activities))
    #return dataprovider
    return None


def get_start_CTL(intensity):
    """Will return the initial CTL value based on the TSS (trimp)
    values. Usally this are the TSS values of the last 4 weeks."""
    if len(intensity) == 0:
        return 0
    return float(sum(intensity)/len(intensity or 1)) / 7


def get_start_ATL(intensity):
    """Will return the initial ATL value based on the TSS (trimp)
    values. Usally this are the TSS values of the last week."""
    if len(intensity) == 0:
        return 0
    return sum(intensity) / 7


def get_CTL(ctl, intensity):
    """Will calculate the Chronic Training Load = „Fitness“ from the
    given series of training intensities based on TRIMP"""
    # CTL(d) = CTL(d-1)+[TSS(d)-CTL(d-1)]*[1-exp^(-1/42)]
    return ctl - (ctl/42.0) + (intensity/42.0)


def get_ATL(atl, intensity):
    """Will calculate the Acute Training Load = „Fatigue“ from the
    given series of training intensities based on TRIMP"""
    return atl - (atl/7.0) + (intensity/7.0)


def get_TSB(ctl, atl):
    """Will calculate the Training Stress Balance = „Form“ based on the
    given CTL and ATL series"""
    return ctl - atl


def get_fitness(ctl, atl, activities):
    intensities = build_intensity_trend(activities)
    fitness = []
    for training_date in intensities:
        intensity = intensities[training_date]
        ctl = get_CTL(ctl, intensity)
        atl = get_ATL(atl, intensity)
        tsb = get_TSB(ctl, atl)
        fitness.append((training_date, intensity, ctl, atl, tsb))
    dataprovider = Dataprovider([f[0] for f in fitness], None, "Days", "Fitness")
    dataprovider.add_series("TRIMP", [f[1] for f in fitness])
    dataprovider.add_series("CTL", [f[2] for f in fitness])
    dataprovider.add_series("ATL", [f[3] for f in fitness])
    dataprovider.add_series("TSB", [f[4] for f in fitness])
    return dataprovider
