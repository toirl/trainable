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
    <div class="col-md-12">
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="card-header">
              ${_('Overall fitness trend')}
            </div>
            <div class="card-content">
              <div id="fitness" style="width: 100%; height: 100%;" class="plotly-graph-div"></div>
              <script type="text/javascript">
                (function(){
                  initFitnessPlot('fitness', ${fitness.get_diagram_values()});
                }());
              </script>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-8">
    </div>
    <div class="col-md-4">
      <%include file="/index/stravasync.mako" />
    </div>
  </div>
% endif




