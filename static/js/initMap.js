$(document).ready(function(){

	var region = {lat: 32.279457, lng:35.72052};

	function initMap(){
		var map = new google.maps.Map(document.getElementById("map"), {center: {lat: region['lat'], lng:region['lng']}, zoom:12});

		google.maps.event.addListener(map,'bounds_changed',function(){
			var bounds = map.getBounds();
			console.log("Bounds:");
			console.log(bounds)
			//console.log("bounds: ");
			//console.log(bounds);
			$.ajax({
				url:'/getcomments',
				data: JSON.stringify(bounds),
				type: 'GET',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			})


		});
	};

	function getMarkers(){

	}

	initMap();
});