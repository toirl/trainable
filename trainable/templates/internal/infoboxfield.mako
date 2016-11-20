## -*- coding: utf-8 -*-
<% 
from trainable.model.activity import velocity2pace
activity = field._form._item %>
<%def name="minmaxavg(label, unit, stream, converter)">
% if stream:
<tr>
  <td>
    ${label}
  </td>
  <td class="text-right">
    ${converter(min(stream))}
  </td class="text-right">
  <td class="text-right">
    ${converter(max(stream))}
  </td>
  <td class="text-right">
    ${converter(round(sum(stream) / len(stream), 2))}
  </td>
  <td class="text-right">
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
        ${activity.get_pace(1000)}<br/><small>[min/km]</small>
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
          <th class="text-right">Min</th>
          <th class="text-right">Max</th>
          <th class="text-right">Avg</th>
          <th></th>
        </tr>
        ${minmaxavg(_('Altitude'), "m", activity.altitude_stream, lambda x: x)}
        % if activity.sport == 1:
          ${minmaxavg(_('Pace'), "min/km", activity.velocity_smooth_stream, lambda x: velocity2pace(x, 1000))}
        % else:
          ${minmaxavg(_('Speed'), "m/s", activity.velocity_smooth_stream, lambda x: x)}
        % endif
        ${minmaxavg(_('Heartrate'), "bpm", activity.heartrate_stream, lambda x: x)}
        % if activity.sport == 1:
          ${minmaxavg(_('Cadence (1L)'), "spm", activity.cadence_stream, lambda x: x)}
        % else:
          ${minmaxavg(_('Cadence'), "rpm", activity.cadence_stream, lambda x: x)}
        % endif
        ${minmaxavg(_('Power'), "W", activity.watts_stream, lambda x: x)}
        ${minmaxavg(_('Grade'), "%", activity.grade_smooth_stream, lambda x: x)}
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
