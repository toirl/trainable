% if field._form._item.coord_lat:
<div class="maprenderer" id="map_${field.id}">${field._form._item}</div>
<script>
  var map_${field.id} = getMap('map_${field.id}', ${field._form._item.coord_lat}, ${field._form._item.coord_lon}, 14,
                               '${request.route_path(renderer._config.routename, id=field._form._item.id)}');
</script>
% endif
