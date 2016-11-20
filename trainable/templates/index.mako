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
  <div class="row">
    <div class="col-md-8">TODO</div>
    <div class="col-md-4">
      % if not request.user.profile[0].strava_client_id:
        ${clientkey_missing()}
      % elif not request.user.profile[0].strava_access_key:
        ${accesskey_missing()}
      % else:
        ${sync()}
      % endif
    </div>
  </div>
% endif

<%def name="strava_header()">
  <div class="card-header .card-header.strava">
    <img src="${request.static_path('trainable:static/images/strava/icon.png')}"/>
    <img src="${request.static_path('trainable:static/images/strava/Strava_Logo.jpg')}"/>
  </div>
</%def>

<%def name="clientkey_missing()">
<div class="card">
  ${strava_header()}
  <div class="card-content">
    <p>In order to link your account with Strava you must
      enter your Strava Client-ID in your profile.</p>
    <p>To find out your Client-ID login to Strava and call <a href="https://www.strava.com/settings/api" target="_blank">Settings Page</a> and select "API".</p>
  </div>
  <div class="card-buttons">
    <a href="${request.route_path('profiles-update', id=request.user.id, _query={"backurl":request.route_path('home')})}" class="btn btn-default modalform" title="${_('Update Profile')}">${_('Update Profile')}</a>
  </div>
</div>
</%def>

<%def name="accesskey_missing()">
<div class="card">
  ${strava_header()}
  <div class="card-content">
    <p>Before your can sync your activities you need to authorize Trainable to access your data.</p>
    <p>Trainable only need read access to your activity data. No data will be modified.</p>
  </div>
  <div class="card-buttons">
    <a href="${strava_auth_url}" class="btn btn-default" title="${_('Authorize with Strava')}">${_('Authorize with Strava')}</a>
  </div>
</div>
</%def>
<%def name="sync()">
<div class="card">
  ${strava_header()}
  <div class="card-content">
    <p>${strava_syncform}</p>
  </div>
</div>
</%def>



