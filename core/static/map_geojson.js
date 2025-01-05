const map = L.map('map').setView([51.505, -0.09], 13);
const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var countriesGeoJSON = false;
fetch('/immoviewer/api/geojson/list/',{
			method: 'GET'
		})
		.then(response => response.json())
		.then(json => {
		    console.log(json);
			countriesGeoJSON = L.geoJSON(json, {
					style: function (feature) {
							return {
								fillOpacity: 0,
								weight: 0.3
							};
					}
			}).addTo(map);
        map.fitBounds(countriesGeoJSON.getBounds());

}).catch(error => console.log(error.message));