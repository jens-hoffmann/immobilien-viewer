$("#district-selection").select2();

const map = L.map('map', { zoomControl: false, measureControl: true }).setView([51.505, -0.09], 13);
const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.control.zoom({
    position: 'topright'
}).addTo(map);

L.control.scale().addTo(map);

select = document.getElementById('district-selection');

var lankreiseGeoJSON = false;
fetch('/static/gemeinden_simplify20.geojson',{
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


                        const gemeinde = layer.feature.properties.GEN;
                        console.log(gemeinde);


                        /* Iterate options of select element */
                        for (const option of document.querySelectorAll('#district-selection option')) {

                          /* If option value contained in values, set selected attribute */
                          if (gemeinde === option.text) {
                            if (option.hasAttribute('selected')) {
                                option.removeAttribute('selected');
                            } else {
                                option.setAttribute('selected', 'selected');
                            }
                            $('#district-selection').trigger('change');
                          }
                        }
                    })
                }
            }).addTo(map);
        map.fitBounds(lankreiseGeoJSON.getBounds());
        console.log(json);
}).catch(error => console.log(error.message));