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
    <div class="col-md-8">
      <div class="row">
        <div class="col-md-12">
          % for tp, workload in trainingplans:
          <div class="card">
            <div class="card-header">
              ${tp}
            </div>
            <div class="card-content">
              <div style="height:200px;width:100%" id="workload"></div>
              <script>
                var data = "${workload.get_diagram_data()}";
                var id = "workload";
                var title = "${workload.get_diagram_titel()}";
                var ylabel = "${workload.get_diagram_ylabel()}";
                var xlabel = "${workload.get_diagram_xlabel()}";
                var fieldname = "workload";
                var errorBars = false;
                g = renderDiagram(id, data, title, xlabel, ylabel, fieldname, errorBars, false);
              </script>
              <div>
                <table class="table">
                  <tr>
                    <td>${_('Start date')}</td>
                    <td>${tp.start_date} (${_('CW')}${tp.start_week})</td>
                    <td>${_('End date')}</td>
                    <td>${tp.end_date} (${_('CW')}${tp.end_week})</td>
                    <td>${_('Length')}</td>
                    <td>${tp.length}</td>
                  </tr>
                  <tr>
                  </tr>
                </table>
              </div>
            </div>
          </div>
          % endfor
          % if len(trainingplans) == 0:
            Oh! It seems you do not have any active trainingplan.</br>
            Start now and create a new <a
              href="${request.route_path('trainingplans-create', _query={"backurl": request.route_path('home')})}">Trainingplan</a>!
          % endif
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <%include file="/index/stravasync.mako" />
    </div>
  </div>
% endif




