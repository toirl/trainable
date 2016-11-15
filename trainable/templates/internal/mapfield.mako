<div class="maprenderer" id="map_${field.id}">${field._form._item}</div>
<script>
  var map_${field.id} = L.map('map_${field.id}', {center: [${field._form._item.coord_lat}, ${field._form._item.coord_lon}], zoom: 14});
  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map_${field.id});

  function addDataToMap(data, map) {
      var dataLayer = L.geoJson(data.data);
      dataLayer.addTo(map);
  }

  ##$.getJSON("${request.route_path(renderer._config.routename, id=field._form._item.id)}",
  ##          function(data) { addDataToMap(data, map_${field.id}); });
</script>
