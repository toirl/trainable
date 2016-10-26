from pyramid.view import view_config
from ringo.views.home import index_view

from stravalib import Client


@view_config(route_name='home', renderer='/index.mako')
def trainable_index_view(request):
    values = index_view(request)
    if request.user:
        client = Client()
        client_id = request.user.profile[0].strava_client_id
        redirect_uri = request.route_url("authstrava")
        url = client.authorization_url(client_id=client_id,
                                       redirect_uri=redirect_uri,
                                       scope="write")
        values["strava_auth_url"] = url
    return values
