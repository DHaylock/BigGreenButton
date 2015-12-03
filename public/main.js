var markers = [];
var map;
var markersId = [];
var markerClusterer;
var maxID;
window.markersArray = [];
//----------------------------------------------------------------------
function init(fid) {
    map = new L.Map('pledgemap');
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);

    map.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

    markerClusterer = new L.MarkerClusterGroup({spiderfyOnMaxZoom: true,zoomToBoundsOnClick: true});

    var bristol = new L.LatLng(51.4419797,-2.5954907);
    map.setView(bristol, 13);
    $.getJSON("getData.php?get", function(json1) {
        $.each(json1, function(key, data) {
            var markerLocation = new L.LatLng(data.lat, data.lng);
            var marker = new L.Marker(markerLocation);
            markerClusterer.addLayer(marker);
            markersId.push(data.id);

            var pledgetitle = ""

            if(pledgetitle == undefined) {
                pledgetitle = "Not yet assigned";
            }
            else {
                pledgetitle = data.pledge;
            }
            var contentString = '<div>' +
                                    '<div align="center">' +
                                        '<h4>Pledge</h4>' +
                                        '<h5>'+ pledgetitle + '</h5>' +
                                        '<h4>Pledger</h4>' +
                                        '<h5>'+ data.pledgename +'</h5>' +
                                        '<p>Pledge was created at: ' + data.timestamp + ' ' + 'and made at: '+ data.updated_at + '</p>' +
                                        // '<p>Pledge ID: ' + data.pledgeid + '</p>' +
                                        '<img width="240px" height="100px" src="./assets/logo-bristol2015-2row-@2x.png">'+
                                    '</div>' +
                                '</div>';

            var popup = L.popup({
                title: data.pledgeid
            }).setContent(contentString);
            marker.bindPopup(popup);
            markers.push(marker);
        });
    });
    map.addLayer(markerClusterer);
}
//----------------------------------------------------------------------
function findPledge() {
    for (var i = 0; i < markers.length; i++) {
        if (markers[i]._popup.options.title == document.getElementById("get").value) {
            map.panTo(new L.LatLng(markers[i]._latlng.lat, markers[i]._latlng.lng));
            $('#edit').animate({
                opacity: "1",
            }, 1000).css('visibility','visible');
            markers[i].openPopup();
            markers[i].bounce({duration: 500, height: 100}, function(){console.log("done")});
            document.getElementById("pledgeLabel").innerHTML = "Pledge Id: "+document.getElementById("get").value;
            $('#pledgeid').attr('value',document.getElementById("get").value);
        }
    }
}
//----------------------------------------------------------------------
function findPledgeReturn(fid) {
    console.log("Find: "+ fid);
    for (var i = 0; i < markers.length; i++) {
        if (markers[i]._popup.options.title == fid) {
            var m = markers[i];
            map.panTo(new L.LatLng(m._latlng.lat, m._latlng.lng));
            setTimeout(function() {
                markerClusterer.zoomToShowLayer(m, function () {
                    setTimeout(function() {
                        m.openPopup();
                    },1000);
                });
            },500);
        }
    }
}
//------------------------------------------------------------------------------
function addNewMarker() {
    maxID = markersId[markersId.length-1];
    $.getJSON("getData.php?newMarkers&maxID="+maxID, function(json1) {
        console.log("Getting Data");
        $.each(json1, function(key, data) {
            var markerLocation = new L.LatLng(data.lat, data.lng);
            var marker = new L.Marker(markerLocation,{bounceOnAdd: true, draggable:false});
            markerClusterer.addLayer(marker)
            markersId.push(data.id);

            var pledgetitle = ""

            if(pledgetitle == undefined) {
                pledgetitle = "Not yet assigned";
            }
            else {
                pledgetitle = data.pledge;
            }
            var contentString = '<div>' +
                                    '<div align="center">' +
                                        '<h4>Pledge</h4>' +
                                        '<h5>'+ pledgetitle + '</h5>' +
                                        '<h4>Pledger</h4>' +
                                        '<h5>'+ data.pledgename +'</h5>' +
                                        '<p>Pledge was created at: ' + data.timestamp + ' ' + 'and made at: '+ data.updated_at + '</p>' +
                                        // '<p>Pledge ID: ' + data.pledgeid + '</p>' +
                                        '<img width="240px" height="100px" src="./assets/logo-bristol2015-2row-@2x.png">'+
                                    '</div>' +
                                '</div>';

            var popup = L.popup()
                .setContent(contentString)

            marker.bindPopup(popup);
            markersId.push(data.id);
            markers.push(marker);
        });

    }).done(function() {
        console.log("Added New Marker");
        $('#alertBar').animate({
            opacity: 1
        },500).delay(2000).animate({
                opacity: 0
            },1000);
    });
}
//----------------------------------------------------------------------
$(document).ready(function() {
    init(id);

    setInterval(function () {
        addNewMarker();
    }, 5000);
});
