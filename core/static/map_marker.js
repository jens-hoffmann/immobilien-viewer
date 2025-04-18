const map = L.map('map').setView(mapLatitudeLongitude, 13);
const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const marker = L.marker(mapLatitudeLongitude).addTo(map)
		.bindPopup(mapAdress).openPopup();