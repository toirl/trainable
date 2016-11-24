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
      <div class="card">
        <div class="card-header">
          ${_('Workload')}
        </div>
        <div class="card-content">
          TODO
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <%include file="/index/stravasync.mako" />
    </div>
  </div>
% endif




