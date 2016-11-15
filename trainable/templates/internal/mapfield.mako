% if field._form._item.coord_lat:
<div class="maprenderer" id="map_${field.id}">${field._form._item}</div>
<script>
  var map_${field.id} = L.map('map_${field.id}', {center: [${field._form._item.coord_lat}, ${field._form._item.coord_lon}], zoom: 14});
  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map_${field.id});

  function addDataToMap(data, map) {
    var myStyle = {
      "color": "#ff7800",
      "weight": 4,
      "opacity": 0.9
    };

    //L.geoJSON(data.data, {
    //style: myStyle
    //}).addTo(map);

    var dataLayer = L.geoJSON(data.data, {style: myStyle});
    dataLayer.addTo(map);
    map.fitBounds(dataLayer.getBounds());
  }

  $.getJSON("${request.route_path(renderer._config.routename, id=field._form._item.id)}",
            function(data) { addDataToMap(data, map_${field.id}); });
</script>
% endif
