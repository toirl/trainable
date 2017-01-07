## -*- coding: utf-8 -*-
<div id="workload" style="width: 100%; height: 100%;" class="plotly-graph-div"></div>
<script type="text/javascript">
  (function(){
    initPlot('workload', ${workload.get_diagram_values()});
  }());
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
