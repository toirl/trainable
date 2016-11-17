var x2coord = null;
var pathmarker = null;

/* Code to sync the diagram to the
configured map The map is stored in a global variable "map_map".
Definition is found in mapfield.mako.  The global variable x2coord map
the x distance value to the latlng coordinats on the map. So every time
a point in the diagram gets highlighted we get the x value and search
for the coordinates. If we can find a new coordinate than a new marker
is put on the map.*/
function showMarkerOnMap(e, x, p){
  var latlng = x2coord[x];
    if (pathmarker != undefined) {
      map_map.removeLayer(pathmarker);
      pathmarker = undefined;
    }
    if (latlng !== undefined) {
      pathmarker = new L.marker(latlng).addTo(map_map);
    }
  };

function getMap(element, lat, lng, zoom, dataUrl) {
  map = L.map(element, {center: [lat, lng], zoom: zoom});
  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);
  $.getJSON(dataUrl, function(data) { addDataToMap(data, map); });
  return map;
}


function addDataToMap(data, map) {
  var myStyle = {
    "color": "#ff7800",
    "weight": 4,
    "opacity": 0.9
  };

  var dataLayer = L.geoJSON(data.data, {style: myStyle});
  dataLayer.addTo(map);
  map.fitBounds(dataLayer.getBounds());
  x2coord = data.data[0].properties.x2coordmap;
}
