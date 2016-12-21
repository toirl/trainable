from pyramid.view import view_config

from stravalib import Client
from formbar.config import Config, load
from formbar.form import Form

from ringo.model.base import get_item_list
from ringo.views.home import index_view
from ringo.lib.form import get_path_to_form_config, get_eval_url
from ringo_diagram.model import Dataprovider

from trainable.views.strava import sync
from trainable.model.trainingplan import Trainingplan
from trainable.model.activity import Activity


def get_trainingplans_for_user(request):
    """TODO: Docstring for get_trainingplans_for_user.
    :returns: TODO
    """
    plans = get_item_list(request, Trainingplan, user=request.user)
    return plans.items


def get_activities_for_user(request, tp):
    start_date = tp.start_date
    end_date = tp.end_date

    activities = get_item_list(request, Activity, user=request.user)
    filter_stack = [(">= {}".format(start_date), "date", False),
                    ("<= {}".format(end_date), "date", False)]
    activities.filter(filter_stack)
    return activities.items


def get_workload_for_trainingplan(request, tp, activities):
    """TODO: Docstring for get_workload_for_trainingplan.
    :returns: TODO
    """
    # Build Dataprovider with workload
    _ = request.translate
    dataprovider = Dataprovider(tp.get_weeks(), None, _("Week"), _("Workload"))
    dataprovider.add_series("Duration [min]", tp.get_duration())
    dataprovider.add_series("Intensity [b]", tp.get_intensity())
    dataprovider.add_series("Pensum [B]", tp.get_pensum())
    dataprovider.add_series("Training Duration [min]", tp.get_activities_duration(activities))
    dataprovider.add_series("Training Intensity [b]", tp.get_activities_intensity(activities))
    dataprovider.add_series("Training Pensum [B]", tp.get_activities_pensum(activities))
    return dataprovider


@view_config(route_name='home', renderer='/index.mako')
def trainable_index_view(request):
    values = index_view(request)
    if request.user:
        client = Client()
        client_id = request.user.profile[0].strava_client_id
        redirect_uri = request.route_url("authstrava")
        url = client.authorization_url(client_id=client_id,
                                       redirect_uri=redirect_uri,
                                       scope="view_private")
        _ = request.translate
        config = Config(load(get_path_to_form_config('strava.xml')))
        form_config = config.get_form('syncform')
        form = Form(form_config, csrf_token=request.session.get_csrf_token(),
                    translate=_, locale="de", eval_url=get_eval_url())

        if request.POST and form.validate(request.params):
            sync(request, form.data.get("sport"),
                 form.data.get("start"), form.data.get("end"),
                 form.data.get("commute"))


        tps = []
        for tp in get_trainingplans_for_user(request):
            activities = get_activities_for_user(request, tp)
            workload = get_workload_for_trainingplan(request, tp, activities)
            tps.append((tp, workload))

        values["trainingplans"] = tps
        values["strava_auth_url"] = url
        values["strava_syncform"] = form.render()
    return values
