## -*- coding: utf-8 -*-
<% activity = field._form._item %>
<%def name="minmaxavg(label, unit, stream)">
% if stream:
<tr>
  <td>
    ${label}
  </td>
  <td>
    ${min(stream)}
  </td>
  <td>
    ${max(stream)}
  </td>
  <td>
    ${round(sum(stream) / len(stream), 2)}
  </td>
  <td>
    ${unit}
  </td>
</tr>
% endif
</%def>
<div id="infobox">
  <div class="row">
    <div class="col-md-4">
      <center>
      <h4>${_("Duration")}</h4>
      ${activity.duration}<br/><small>[HH:MM:SS]</small>
      </center>
    </div>
    <div class="col-md-4">
      <center>
      <h4>${_("Distance")}</h4>
      ${activity.distance}<br/><small>[m]</small>
      </center>
    </div>
    <div class="col-md-4">
      <center>
      % if activity.sport == 1:
        <h4>${_("Pace")}</h4>
        ${activity.speed}
      % else:
        <h4>${_("Speed")}</h4>
        ${activity.speed}<br/><small>[km/h]</small>
      % endif
      </center>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      &nbsp;
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <table class="table table-condesed">
        % if activity.elevation:
        <tr>
          <td>
            ${"Total elevation"}
          </td>
          <td>
            ${activity.elevation}
          </td>
          <td>
            m
          </td>
        </tr>
        % endif
        % if activity.watts_per_kg:
        <tr>
          <td>
            ${"Watt per KG"}
          </td>
          <td>
            ${activity.watts_per_kg}
          </td>
          <td>
            W/kg
          </td>
        </tr>
        % endif
      </table>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      &nbsp;
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <table class="table table-condesed">
        <tr>
          <th></th>
          <th>Min</th>
          <th>Max</th>
          <th>Avg</th>
          <th></th>
        </tr>
        ${minmaxavg(_('Altitude'), "m", activity.altitude_stream)}
        ${minmaxavg(_('Speed'), "m/s", activity.velocity_smooth_stream)}
        ${minmaxavg(_('Heartrate'), "bpm", activity.heartrate_stream)}
        ${minmaxavg(_('Cadence'), "rpm", activity.cadence_stream)}
        ${minmaxavg(_('Power'), "W", activity.watts_stream)}
        ${minmaxavg(_('Grade'), "%", activity.grade_smooth_stream)}
      </table>
    </div>
  </div>
  % if activity.description:
  <div class="row">
    <div class="col-md-12">
      <small>
        <h5>${_('Description')}</h5>
        <p>${activity.description}</p>
      </small>
    </div>
  </div>
  % endif
  <div class="row">
    <div class="col-md-12">
      <a class="btn btn-default btn-block" href="https://www.strava.com/activities/${activity.strava_id}" target="_blank"><img src="${request.static_path('trainable:static/images/strava_sync.png')}"/> ${_('Open activity on Strava')}</a>
    </div>
  </div>
</div>
