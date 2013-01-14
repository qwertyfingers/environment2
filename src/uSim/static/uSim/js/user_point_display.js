
var test_map;
var markers;
var test_point_x=-287765.66311784;
var test_point_y=6710921.3156023;
var test_lon=-287467.67814;
var test_lat=6710727.3168309;
var size = new OpenLayers.Size(21,25);
var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
var icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png',size,offset); 
var markerArray=[]
var tickArray=[]
var sim_tick=0
var timer=true 
var timeout=40 
var num_entries
var database_array

$(document).ready(function() {
database_array=reports_array //from external javascript/database
 
init_map()   
add_marker_layer() //marker layer is called 'markers'   

num_entries=database_array.length
var j=0;
for (j=0; j<num_entries; j++){
markerArray.push(new OpenLayers.Marker(new OpenLayers.LonLat(parseFloat(database_array[j][0]),parseFloat(database_array[j][1]))))

if (timer==false){
markers.addMarker(markerArray[markerArray.length - 1])
}
else{
tickArray.push(database_array[j][2])    
}
}





if (timer){
tick_forward()
  
}




})



function tick_forward(){ 
    
var j=0;

for (j=0; j<num_entries; j++){

if (tickArray[j]==sim_tick){
newMarker=new OpenLayers.Marker(new OpenLayers.LonLat(parseFloat(database_array[j][0]),parseFloat(database_array[j][1])))
markers.addMarker(newMarker)
}

}
   
   
       
sim_tick=sim_tick+1 
setTimeout("tick_forward();", timeout)    
}





function init_map(){
    
var map_options={
    controls: [
        //new OpenLayers.Control.Navigation(),
        new OpenLayers.Control.ArgParser(),
        new OpenLayers.Control.Attribution()
    ]
}
    test_map = new OpenLayers.Map("map",map_options);
    test_map.addLayer(new OpenLayers.Layer.OSM()); 
    test_map.setCenter
    (new OpenLayers.LonLat(test_lon, test_lat)
        ,16 // Zoom level
        );      
}

function add_marker_layer(){
    markers = new OpenLayers.Layer.Markers( "Markers" );
    test_map.addLayer(markers); 
}