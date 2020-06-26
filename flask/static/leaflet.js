var mymap = L.map('mapid').setView([30, 0], 16);

function defMap(){
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 2,
        id: 'mapbox.light',
        accessToken: 'pk.eyJ1IjoidGFpbmFhZSIsImEiOiJjam04N2h4NHUwMWhzM3dwZmo1MjZjdXQ0In0.BCSwddDjuO0EPdupfyu06Q'
    }).addTo(mymap);
    
    legend.addTo(mymap);
    return mymap;
}

function getColor(d) {
    return d > 100 ? '#49006a' :
        d > 80  ? '#7a0177' :
        d > 60  ? '#ae017e' :
        d > 40  ? '#dd3497' :
        d > 20  ? '#f768a1' :
        d > 10  ? '#fa9fb5' :
        d > 5  ? '#fcc5c0' :
                '#fde0dd' ;
}   

function style(feature) {
    return {
        fillColor: getColor(feature),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function clearStyle(feature) {
    return {
        //fillColor: getColor(feature),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0
    };
}


/*function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}


function resetHighlight(e) {
    geojson.resetStyle(e.target);
    postDataCallback(receivedData, "");
}*/

function zoomToFeature(e) {
    mymap.fitBounds(e.target.getBounds());
}


function onEachFeature(feature, layer) {
    layer.on({
        //mouseover: highlightFeature,
        //mouseout: resetHighlight,
        click: zoomToFeature
    });
}


var legend = L.control({position: 'bottomright'});

legend.onAdd = function (mymap) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 5, 10, 20, 40, 60, 80, 100],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(mymap);

