var x2coord = null;
var pathmarker = null;

var curPosIcon;
var startPosIcon;
var endPosIcon;

function buildIcons() {
    /* Will create three different icons which will be used on the map */
    var LeafIcon = L.Icon.extend({
        options: {
            shadowUrl: '/trainable-static/leaflet/images/marker-shadow.png',
            iconAnchor:   [12, 41],
            shadowAnchor: [12, 41],
        }
    });
    curPosIcon = new LeafIcon({iconUrl: '/trainable-static/images/mapmarker/marker-current-position.png'});
    startPosIcon = new LeafIcon({iconUrl: '/trainable-static/images/mapmarker/marker-start-position.png'});
    endPosIcon = new LeafIcon({iconUrl: '/trainable-static/images/mapmarker/marker-end-position.png'});
};


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
      pathmarker = new L.marker(latlng, {icon: curPosIcon}).addTo(map_map);
    }
  };

function getMap(element, lat, lng, zoom, dataUrl) {
  buildIcons();
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

  var path = data.data[0];
  var scoord = data.data[1].geometry.coordinates
  var ecoord = data.data[2].geometry.coordinates;

  /* Put custom start and end marker on the map */
  L.marker([scoord[1], scoord[0]], {icon: startPosIcon}).addTo(dataLayer);
  L.marker([ecoord[1], ecoord[0]], {icon: endPosIcon}).addTo(dataLayer);

  /* Put track on the map */
  var dataLayer = L.geoJSON(path, {style: myStyle});
  dataLayer.addTo(map);

  /* Fit map to the track */
  map.fitBounds(dataLayer.getBounds());

  /* Set x2coord mapping. Mapping is later used by the diagrams to identify a
   * certain coordinate to a given x-value out of the diagram.*/
  x2coord = data.data[0].properties.x2coordmap;
}
