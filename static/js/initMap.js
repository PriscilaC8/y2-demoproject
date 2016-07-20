$(document).ready(function(){
	
	function initMap(){
		var map = new google.maps.Map(document.getElementById("map"), {center: {lat: 32.279457, lng:35.72052}, zoom:12});
	};

	initMap();
});