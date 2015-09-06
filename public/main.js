var markers = []
var map;
var markersId = [];
var maxID;
window.markersArray = []
function initialize() {
  var myLatlng = new google.maps.LatLng(51.4419797, -2.5954907);
  var mapOptions = {
    zoom: 11,
    center: myLatlng,
    streetViewControl: false,
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
      position: google.maps.ControlPosition.BOTTOM_LEFT
    },
    panControl: true,
    panControlOptions: {
      position: google.maps.ControlPosition.RIGHT_CENTER
    },
    zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.MEDIUM,
      position: google.maps.ControlPosition.RIGHT_CENTER
    }
  };
   var styles = [
  {
    "elementType": "labels.text.fill",
    "stylers": [
      { "weight": 3.8 },
      { "visibility": "on" },
      { "color": "#000000" }
    ]
  },{
    "elementType": "geometry",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      { "visibility": "on" },
      { "color": "#000000" }
    ]
  },{
    "featureType": "landscape",
    "elementType": "geometry",
    "stylers": [
      { "visibility": "on" },
      { "color": "#ffffff" }
    ]
  },{
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      { "visibility": "on" },
      { "hue": "#0088ff" },
      { "saturation": 35 }
    ]
  },{
    "elementType": "geometry"  }
];
// [
//   {
//     "featureType": "landscape",
//     "stylers": [
//       {
//         "hue": "#FFBB00"
//       },
//       {
//         "saturation": 43.400000000000006
//       },
//       {
//         "lightness": 37.599999999999994
//       },
//       {
//         "gamma": 1
//       }
//     ]
//   },
//   {
//     "featureType": "road.highway",
//     "stylers": [
//       {
//         "hue": "#FFC200"
//       },
//       {
//         "saturation": -61.8
//       },
//       {
//         "lightness": 45.599999999999994
//       },
//       {
//         "gamma": 1
//       }
//     ]
//   },
//   {
//     "featureType": "road.arterial",
//     "stylers": [
//       {
//         "hue": "#FF0300"
//       },
//       {
//         "saturation": -100
//       },
//       {
//         "lightness": 51.19999999999999
//       },
//       {
//         "gamma": 1
//       }
//     ]
//   },
//   {
//     "featureType": "road.local",
//     "stylers": [
//       {
//         "hue": "#FF0300"
//       },
//       {
//         "saturation": -100
//       },
//       {
//         "lightness": 52
//       },
//       {
//         "gamma": 1
//       }
//     ]
//   },
//   {
//     "featureType": "water",
//     "stylers": [
//       {
//         "hue": "#0078FF"
//       },
//       {
//         "saturation": -13.200000000000003
//       },
//       {
//         "lightness": 2.4000000000000057
//       },
//       {
//         "gamma": 1
//       }
//     ]
//   },
//   {
//     "featureType": "poi",
//     "stylers": [
//       {
//         "hue": "#00FF6A"
//       },
//       {
//         "saturation": -1.0989010989011234
//       },
//       {
//         "lightness": 11.200000000000017
//       },
//       {
//         "gamma": 1
//       }
//     ]
//   }
// ];

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  map.setOptions({styles:styles});

  // var populationOptions = {
  //     strokeColor: '#FF0000',
  //     strokeOpacity: 0.8,
  //     strokeWeight: 2,
  //     fillColor: '#FF0000',
  //     fillOpacity: 0.35,
  //     map: map,
  //     center: new google.maps.LatLng(51.4419797, -2.5954907),
  //     radius: 20000
  //   };
    // Add the circle for this city to the map.
    // var cityCircle = new google.maps.Circle(populationOptions);

  var image = './assets/marker.png';
  $.getJSON("http://localhost:8888/getData.php?get", function(json1) {
    console.log("Getting Data");
    $.each(json1, function(key, data) {
      var latLng = new google.maps.LatLng(data.lat, data.lng);
      // Creating a marker and putting it on the map
      var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        title: data.pledgeid,
        icon:image,
        clickable: true
      });

      var contentString = '<div>' +
        '<h1>Pledge: ' + data.pledge + '</h1>' +
        '<h3>Pledge Id: ' + data.pledgeid + '</h3>' +
        '<h3>Pledger: ' + data.pledgename + '</h3>' +
        '<h5>Pledge was created at: ' + data.timestamp + '</h5>' +
        '<h5>and made at: ' + data.updated_at + '</h5>' +
        '</div>';

      var infowindow = new google.maps.InfoWindow({
        content: contentString,
        maxWidth:700
      });

      google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
      });
      markersId.push(data.id);
      markers.push(marker);
    });
  }).done(function() {
        markerClusterer = new MarkerClusterer(map, markers, {
            gridSize: 100
        });
        // console.log(markersId);
        maxID = markersId[markersId.length-1];
        // console.log(maxID);
        console.log("Got the Data!");
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

function changeTitle() {
  for (var i = 0; i < markers.length; i++) {
    if (markers[i].getTitle() == document.getElementById("get").value) {
      AnimatingMarker(i);
      map.panTo(markers[i].getPosition());
      map.setZoom(15);
      $('#edit').animate({
        opacity: "1",

    }, 500).css('visibility','visible');
      document.getElementById("pledgeLabel").innerHTML = "Pledge Id: "+document.getElementById("get").value;
      $('#pledgeid').attr('value',document.getElementById("get").value);
    }
  }
}
function AnimatingMarker(m) {
  markers[m].setAnimation(google.maps.Animation.BOUNCE);
  setTimeout(function () {
    markers[m].setAnimation(null);
  }, 1400);
}

function addNewMarker() {
    var image = './assets/marker.png';
    maxID = markersId[markersId.length-1];
    $.getJSON("http://localhost:8888/getData.php?newMarkers&maxID="+maxID, function(json1) {
        console.log("Getting Data");
        $.each(json1, function(key, data) {
            var latLng = new google.maps.LatLng(data.lat, data.lng);
                // Creating a marker and putting it on the map
                var marker = new google.maps.Marker({
                  position: latLng,
                  map: map,
                  title: data.pledgeid,
                  icon:image,
                  clickable: true
                });

                var contentString = '<div>' +
                  '<h1>Pledge: ' + data.pledge + '</h1>' +
                  '<h3>Pledge Id: ' + data.pledgeid + '</h3>' +
                  '<h3>Pledger: ' + data.pledgename + '</h3>' +
                  '<h5>Pledge was created at: ' + data.timestamp + '</h5>' +
                  '<h5>and made at: ' + data.updated_at + '</h5>' +
                  '</div>';

                var infowindow = new google.maps.InfoWindow({
                  content: contentString,
                  maxWidth:700
                });

                google.maps.event.addListener(marker, 'click', function() {
                  infowindow.open(map, marker);
                });
                markerClusterer.addMarker(marker);
            markersId.push(data.id);
            console.log(data.id);
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


$(document).ready(function() {
  setInterval(function () {
    addNewMarker();
  }, 5000);
});
