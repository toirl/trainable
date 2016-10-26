<%inherit file="/main.mako" />
<%
mapping={'app_title': h.get_app_title()}
%>
<div class="page-header">
<h1>Home</h1>
</div>
% if request.user:
<%include file="/logininfo.mako" />
% endif

% if not request.user:
  <p>
    <a href="${request.route_path('login')}" class="btn btn-primary btn-large" title="${_('Login in the application')}">${_('Login')}</a>
  </p>
% else:
  <h2>Add training</h2>
  <p>
    <a href="${request.route_path('trainings-create')}" class="btn btn-primary btn-large" title="${_('Log a new training')}">${_('Log a new training')}</a>
  </p>
  <h2>Strava Sync</h2>
  % if not request.user.profile[0].strava_client_id:
  <p>
    Your profile is missing the client ID from strava. This id is needed to
    connect your account at trainable with strava.
  </p>
  <p>
    <a href="${request.route_path('profiles-update', id=request.user.id, q={"backurl":request.route_path('home')})}" class="btn btn-primary btn-large" title="${_('Update Profile')}">${_('Update Profile')}</a>
  </p>
  % else: 
    % if not request.user.profile[0].strava_access_key:
    <p>
      You did not authorize trainable to access your data on strava.</br>
      <a href="${strava_auth_url}" class="btn btn-primary btn-large" title="${_('Authorize with Strava')}">${_('Authorize with Strava')}</a>
    </p>
    % endif
  % endif
  % if request.user.profile[0].strava_access_key and request.user.profile[0].strava_client_id:
  <p>
    <a href="${request.route_path('syncstrava')}" class="btn btn-primary btn-large" title="${_('Synchronize with Strava')}">${_('Synchronize with Strava')}</a>
  </p>
  % endif
% endif
