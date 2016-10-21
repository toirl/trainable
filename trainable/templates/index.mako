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
  <p>
    <a href="${request.route_path('syncstrava')}" class="btn btn-primary btn-large" title="${_('Synchronize with Strava')}">${_('Synchronize with Strava')}</a>
  </p>
% endif
