$(document).ready(function() {

    var latitude_nord_est = 48.9532;
    var longitude_nord_est = 2.5008;
    var latitude_sud_ouest = 48.7865;
    var longitude_sud_ouest = 2.0689;

    map_markers = [];
    var intervalle = setInterval(check_adresse, 10000);

    function check_adresse() {
    const url_api = "https://api-adresse.data.gouv.fr/search/?q=";

    var empt_rue = document.forms["form1"]["Rue"].value;
    var empt_n_rue = document.forms["form1"]["N_rue"].value;
    if ((empt_rue == "" && empt_n_rue == "") || empt_rue == "" || empt_n_rue == "")
        {
        return false;
        }
    else
        {
        // appeler l'api et prendre les résultats

        fetch(url_api + empt_n_rue + " " + empt_rue + "&limit=1").then((response)=>{
            return response.json();  // converting byte data to json
            }).then(data=>{

                // suppression du marker déjà présent
                if (map_markers.length > 0){for(i=0;i<map_markers.length;i++) {
                    map.removeLayer(map_markers[i]);
                        };
                    }
                else {};

                var latitude = data["features"][0]["geometry"]["coordinates"][1];
                var longitude = data["features"][0]["geometry"]["coordinates"][0];

                var new_marker = L.marker([latitude, longitude]);
                map_markers.push(new_marker);
                new_marker.addTo(map);

                // remplissage des champs GPS uniqueent si la latitude la longitude sont dans  l'aire parisienne
                // 48.7865,2.0689 au sud_ouest, 48.9532,2.5008 au nord-est
                if(latitude > latitude_sud_ouest && latitude < latitude_nord_est && longitude < longitude_nord_est && longitude > longitude_sud_ouest){
                document.getElementById('Latitude_x').value = latitude;
                document.getElementById('Longitude_y').value = longitude;
                }
                else{
                document.getElementById('Latitude_x').value = '';
                document.getElementById('Longitude_y').value = '';
                }
            });

        return true;
        }

};
intervalle;



            // Création de la carte à l'id "map"
            var map = L.map('map', {
                zoomControl: true
                }).setView(new L.LatLng(48.8542, 2.3484), 12);

            // Usage des tuiles de carte d'OpenStreetMap puis ajout à la carte map
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '<a href="openstreetmap.org">OpenStreetMap</a> | <a href="www.paris-historique.org">Association Paris Historique</a> | Maxime Challon',
                maxNativeZoom: 100
            }).addTo(map);


            // récupération de la latitude et de la longitude lors d'un clic sur la carte
            map.on('click', function(e) {
                if (confirm("Valider cette position?"))
                    {
                    if (map_markers.length > 0){for(i=0;i<map_markers.length;i++) {
                    map.removeLayer(map_markers[i]);
                        };
                    }
                else {};

                    var lat = e.latlng.lat;
                    document.getElementById('Latitude_x').value = lat;
                    var long = e.latlng.lng;
                    document.getElementById('Longitude_y').value = long;

                    // ajout d'un marqueur à l'endroit du clic
                    marker = L.marker([lat, long]);
                    marker.addTo(map);

                    // arrêt de la recherche dans l'API
                    clearInterval(intervalle);
                    }
                });
});