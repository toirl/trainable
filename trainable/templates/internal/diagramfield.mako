## -*- coding: utf-8 -*-
<div style="height:140px;width:100%" id="${field.name}"></div>
<script>
  var data = "${getattr(field._form._item, field.name).get_diagram_data()}";
  var id = "${field.name}";
  var title = "${getattr(field._form._item, field.name).get_diagram_titel()}";
  var ylabel = "${getattr(field._form._item, field.name).get_diagram_ylabel()}";
  var xlabel = "${getattr(field._form._item, field.name).get_diagram_xlabel()}";
  var fieldname = "${field.name}";
  var errorBars = ${str(getattr(field._form._item, field.name).errors_enabled()).lower()};
  g = renderDiagram(id, data, title, xlabel, ylabel, fieldname, errorBars, false, showMarkerOnMap);
  % if renderer._config.sync:
  diagram_syncs.push(g);
  % endif
</script>
