## -*- coding: utf-8 -*-
<table width="100%" style="margin: 10px 0 20px 0">
  <tr>
    <td width="75%">
      % if getattr(field._form._item, field.name).has_diagram_data():
        <div style="height:200px;width:100%" id="${field.name}"></div>
      % else:
        ${_('No data available.')}
      % endif
    </td>
    <td width="5%">
      &nbsp;
    </td>
    <td width="20%" style="vertical-align:top">
      <div id="${field.name+'_legend'}"></div>
    </td>
  </tr>
</table>
<script>
  var data = "${getattr(field._form._item, field.name).get_diagram_data()}";
  var id = "${field.name}";
  var title = "${getattr(field._form._item, field.name).get_diagram_titel()}";
  var ylabel = "${getattr(field._form._item, field.name).get_diagram_ylabel()}";
  var xlabel = "${getattr(field._form._item, field.name).get_diagram_xlabel()}";
  var fieldname = "${field.name}";
  var errorBars = ${str(getattr(field._form._item, field.name).errors_enabled()).lower()};
  g = renderDiagram(id, data, title, xlabel, ylabel, fieldname, errorBars, showMarkerOnMap);
  % if renderer._config.sync:
  diagram_syncs.push(g);
  % endif
</script>
