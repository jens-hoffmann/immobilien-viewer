$(document).ready(function() {

	$(document).on('click','#btn-slide-out',function() {
		if($('#slide-in').hasClass('in')) {
			$('#slide-in').removeClass('in')
		}
	});

	const map = L.map('map', { zoomControl: false, measureControl: true }).setView([51.505, -0.09], 13);
	const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	L.control.zoom({
		position: 'topright'
	}).addTo(map);

	L.control.scale().addTo(map);

	var countriesGeoJSON = false;
	fetch('/immoviewer/api/geojson/list/',{
				method: 'GET'
			})
			.then(response => response.json())
			.then(json => {
				countriesGeoJSON = L.geoJSON(json, {
						style: function (feature) {
								return {
									fillOpacity: 0,
									weight: 0.3
								};
						},
				}).on('click', function(event){
					var uuid = event.layer.feature.id;
					var title = event.layer.feature.properties.title;
					var location = event.layer.feature.properties.location;

					if($('#slide-in').hasClass('in')) {
						$('#slide-in').removeClass('in')
					}
					$('#immo-information').html(title);
					$('#immo-detail-link').attr('href', '/immoviewer/immobilie/detail/'+event.layer.feature.id+'/');
					$('#slide-in').addClass('in')


				})
				.addTo(map);
			map.fitBounds(countriesGeoJSON.getBounds());

	}).catch(error => console.log(error.message));

	var lankreiseGeoJSON = false;
	fetch('/static/landkreise_simplify20.geojson',{
				method: 'GET'
			})
			.then(response => response.json())
			.then(json => {

				lankreiseGeoJSON = L.geoJSON(json, {
					style: function (feature) {
							return {
								fillOpacity: 0.1,
								fillColor: '#000',
								color: '#000',
								opacity: 0.3
							};
					},
                    onEachFeature: function(feature,layer) {
						layer.on('mouseover',function() {
							layer.setStyle({fillOpacity: 0.5})
                        })
                        layer.on('mouseout',function() {
                            layer.setStyle({fillOpacity: 0.1})
                        })
                        layer.on('click',function() {
                            layer.setStyle({fillOpacity: 0.5, fillColor: '#4db93f',color: '#4db93f'});
                            console.log(layer.feature.properties.GEN);
                        })
                    }
				}).addTo(map);
			console.log(json);
	}).catch(error => console.log(error.message));
});



