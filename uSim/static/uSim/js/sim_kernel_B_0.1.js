
//namespace for this javascript
var uSim = {};

// Create objects to store sim data (if available) 
uSim.sim_settings={}
uSim.agent_settings={}
uSim.view_settings={}


// Log data
uSim.log={}


uSim.simData = {}; // used to store simData from file
uSim.page = { 
    "play":"#playPauseButton", //
    "pause":"#playPauseButton",//
    "reset":"#resetButton", //
    "simDataForm":"#simForm",//
    "simDataFile":"#simFile",
    "mapOL":"map",
    "map":"#map"
}

//gloabl varaibles
uSim.glo = {

    "googleProjection": new OpenLayers.Projection("EPSG:900913"),//projection from
    "defaultProjection": new OpenLayers.Projection("EPSG:4326"),//projection to
    "mapLayer": new OpenLayers.Layer.OSM(),
    "map":"",
    "agentLayer":"",
    "agentStyleSymbolizer":"",
    "numAgents":""
}

uSim.simState = {
"fileLoaded":null, //is simulation loaded, and what 
"agents":[], //stores agent data, as this changes with sim state
"simPlaying":false //default simPlaying state
}


uSim.user={};

//*************************************************************************

//this sets the style for individual agents, and applies it to the default style of the layer
uSim.glo.agentStylesymbolizer = OpenLayers.Util.applyDefaults(
{
    pointRadius: '${size}', 
    fillColor: '${fillColour}',
    strokeColor: '${strokeColour}',
    strokeWidth: '${strokeWidth}',
    strokeOpacity: '${strokeOpacity}',
    fillOpacity: '${fillOpacity}'
},
OpenLayers.Feature.Vector.style["default"]);

uSim.glo.viewStyle= new OpenLayers.StyleMap({
        "default": new OpenLayers.Style({
            fillColor: "#79ACC5",
            fillOpacity: 0.1,
            strokeColor: "#85A8BE",
            strokeWidth: 2,
            strokeOpacity: 0.5
              
        })
    });


uSim.glo.agentStyle=new OpenLayers.StyleMap(uSim.glo.agentStylesymbolizer);









//Main script
//**********************************************************************

/*
The main script runs as follows

Once document is ready:
1. Check if sim,agent and view settings are available
2. If sim settings are available, load the simulation
3. If agent settings are available, load the agents
4. If a view is available, load the view
5. Wait for the map to finish loading before proceeding
6. Send a trigger theat the sim is loaded
7. Make layers visible as sim is ready to run
8. Update sim - keep updating until the sim is stopped. This essentially runs the simulation frame to frame
*/


$(document).ready(function() {
    
    gui_available=false

    set_settings()                                      //1
                                                      
    if (uSim.log.sim_settings_available){               //2 
        init_map()
        uSim.glo.mapLayer.setVisibility(false); 
    
        if (uSim.log.agent_settings_available){             //3
        add_agent_layer();
        uSim.glo.agentLayer.setVisibility(false);    
        init_agents();
        
            if (uSim.log.view_settings_available){              //4
            add_view_layer();
            uSim.glo.viewLayer.setVisibility(false);
            init_view();
            }
        }
    }
    if (gui_available){
    // Do some stuff    
    }
     
    var count=0;
    uSim.glo.mapLayer.events.register("loadend", uSim.glo.mapLayer, function () {   //5
          
        if (count<=0){   
            $('#map').trigger('simLoad')                                                //6
            uSim.simState.simPlaying=true; //Take this out once GUI in place
        
            if (uSim.log.sim_settings_available){
                uSim.glo.mapLayer.setVisibility(true);                                      //7
                if(uSim.log.agent_settings_available){
                    if(uSim.log.view_settings_available){     
                    uSim.glo.viewLayer.setVisibility(true);
                    }
                var agents=uSim.simState.agents
                var view=uSim.user.viewBox;
                var j=0;

                for (j=0; j<uSim.glo.numAgents; j++){
                    
                    agents[j].animateAgent();
        
                    if (uSim.log.view_settings_available){
                        isAgentVisible(agents[j],view);
        
                    if(agents[j].visible==true){
                        agents[j].f.attributes.visible="visible"}
                    else if(agents[j].visible==false){
                        agents[j].f.attributes.visible="notVisible"}
                    }
                    }    
   
                  uSim.glo.agentLayer.setVisibility(true); 
                  count=count+1; 
                  update_sim();                                                                     //8
                  
                }    
            }
        }
    });
});





//************************************************************




function init_map(){
    var lon=uSim.sim_settings.simulationSettings[0].centre[0];
    var lat=uSim.sim_settings.simulationSettings[0].centre[1];
var map_options={
    controls: [
        //new OpenLayers.Control.Navigation(),
        new OpenLayers.Control.ArgParser(),
        new OpenLayers.Control.Attribution()
    ]
}
    uSim.glo.map = new OpenLayers.Map(uSim.page.mapOL,map_options);
    uSim.glo.map.addLayer(uSim.glo.mapLayer); 
    uSim.glo.map.setCenter
    (new OpenLayers.LonLat(lon, lat)
        ,uSim.sim_settings.simulationSettings[0].zoomLevel // Zoom level
        );      
}

function add_agent_layer(){
    //based on example found here:http://openlayers.org/dev/examples/stylemap.html
var visible = {
        "visible": {display: ""},
        "notVisible": {display: "none"}
    }
    uSim.glo.agentStyle.addUniqueValueRules("default", "visible", visible);
    uSim.glo.agentLayer = new OpenLayers.Layer.Vector("Agent Layer", {
    styleMap: uSim.glo.agentStyle           
    }); 
    uSim.glo.map.addLayer(uSim.glo.agentLayer);
}

function init_agents() {
    var j=0;
    uSim.glo.numAgents=uSim.agent_settings.agents.length;
  
    
    
    for (j=0;j<uSim.glo.numAgents;j++){
        var newAgent= new createAnAgent();
        newAgent.setWaypoints(json_agent_settings.agents[j].waypoints);
       
        newAgent.setAgentSize(json_agent_settings.agents[j].size);
        newAgent.setAgentColour(json_agent_settings.agents[j].fillColour, json_agent_settings.agents[j].strokeColour,json_agent_settings.agents[j].strokeWidth);
        
        newAgent.setAgentOpacity(json_agent_settings.agents[j].fillOpacity, json_agent_settings.agents[j].strokeOpacity);
        //adds agent to agentLayer
        addAgent(newAgent,uSim.glo.agentLayer);
           
    } 

}

function update_sim(){
 var tickStart=new Date()   
 $(uSim.page.map).trigger("simTick")   
    
    var agents=uSim.simState.agents
    var view=uSim.user.viewBox;
    
    var j=0;
    
    
    
    for (j=0; j<uSim.glo.numAgents; j++){
        
        agents[j].animateAgent();
        
        if (uSim.log.view_settings_available){
        isAgentVisible(agents[j],view);
        
        if(agents[j].visible==true){
                agents[j].f.attributes.visible="visible"}
            else if(agents[j].visible==false){
                agents[j].f.attributes.visible="notVisible"}
        }
          
    
}

if (uSim.simState.simPlaying){
    var tickEnd=new Date()
    var processTime=(tickEnd-tickStart)/1000;
    var timeout=json_sim_settings.simulationSettings[0].mapUpdateTime-processTime;
    if (timeout<=0){
        timeout=0;
   }
     setTimeout("update_sim();", timeout)    
       
    }
}
   
function addAgent(agent,layer){

    var agentLocation = new OpenLayers.LonLat(agent.x, agent.y)
    var geometry = new OpenLayers.Geometry.Point
    (agentLocation.lon,agentLocation.lat);
    var feature = new OpenLayers.Feature.Vector(geometry,
    {
        "size": agent.size,
        "fillColour": agent.fillColour,
        "strokeColour" : agent.strokeColour,
        "strokeWidth" : agent.strokeWidth,
        "strokeOpacity":agent.strokeOpacity,
        "fillOpacity": agent.fillOpacity
            
    });
    layer.addFeatures(feature);
    agent.f=feature;

    agent.f.attributes.visible="visible";
        
      
    uSim.simState.agents.push(agent);
        
}  
    

    

function add_view_layer(){
        var viewLayer= new OpenLayers.Layer.Vector("View Layer",{styleMap:uSim.glo.viewStyle
        }); 
        uSim.glo.map.addLayer(viewLayer);    
        uSim.glo.viewLayer=viewLayer;
        
    }

function init_view(){
 

 var simView=uSim.view_settings.views[0].viewport;
 var view=new createAView(simView);

 uSim.user.viewBox=view;
 uSim.glo.viewLayer.addFeatures(view.feature);
 var mapOptions={
     restrictedExtent:view.viewBounds}
 uSim.glo.map.setOptions(mapOptions);
 uSim.glo.map.zoomToExtent(view.viewBounds)
}

function createAView(boundsIn)
    {
     
        this.viewBounds= new OpenLayers.Bounds(boundsIn[0],boundsIn[1],boundsIn[2],boundsIn[3]);
        this.geometry=this.viewBounds.toGeometry();
        this.feature= new OpenLayers.Feature.Vector();
        this.feature.geometry=this.geometry;
    
    } 
    
 function isAgentVisible(agent,view){

        //check if agent should be seen by view. If 
        if(agent.visible && !view.viewBounds.contains(agent.x,agent.y,false))
        {
            agent.visible=false; //these store the state of the agent with respect to current view
        }
        else if(!agent.visible && view.viewBounds.contains(agent.x,agent.y,false))
        {
            agent.visible=true;
        } 
    }
    
function UserSetup(){
}    
UserSetup.prototype.setAttribute=function(attribute,value){
try{
this[attribute]=value;    
}
catch(err){}
}
function createAnAgent(){


    //initilaise some agent variables
    this.dx=0; // move agent by this amount in x direction
    this.dy=0; // move agent by this amount in y direction
    this.active=true; // is agent moving
    this.persist=true; // should agent stay rendered when finished moving?

    this.visible=true;
    //function to add waypoints to an agent. Takes an array of waypoints as input
    this.setWaypoints=function(waypoints){
        this.waypoints = waypoints; // array of waypoints
        this.waypointsIndex = 0; // index that maintains the reference of current waypoint in list
        this.x= this.waypoints[0][0]; // current poistion of agent (may not be waypoint once animated)
        this.y=this.waypoints[0][1];
    }

    this.setAgentSize=function(agentSize){   
        this.size=agentSize   
    }    

    this.setAgentColour=function(fillColour,strokeColour,strokeWidth){   
        this.fillColour=fillColour;
        this.strokeColour=strokeColour;
        this.strokeWidth=strokeWidth;
    }
 
    this.setAgentOpacity=function(fillOpacity,strokeOpacity){
        this.fillOpacity=fillOpacity;
        this.strokeOpacity=strokeOpacity;
    }
                   
    
    
    //function that interpolates the points between two waypoints based on agent speed,
    //and the simulation tick rate

    

    // function that aniamtes the agent in its layer based on the interpolated point
    
}
createAnAgent.prototype.animateAgent=function(){

        if (this.active){
            
            var x=this.waypoints[this.waypointsIndex][0];
            var y=this.waypoints[this.waypointsIndex][1];
            var xNext=this.waypoints[this.waypointsIndex+1][0];
            var yNext=this.waypoints[this.waypointsIndex+1][1];
            this.f.geometry.move(xNext-x,yNext-y)  
            this.f.layer.drawFeature(this.f);
            this.waypointsIndex++
        }
    }

function set_settings(){
    if (typeof json_sim_settings !== 'undefined'){
        uSim.sim_settings=json_sim_settings
        uSim.log.sim_settings_available=true}
    else{
    uSim.log.sim_settings_available=false 
    }
    if (typeof json_agent_settings !== 'undefined'){
        uSim.agent_settings=json_agent_settings
        uSim.log.agent_settings_available=true}
    else{
        uSim.log.agent_settings_available=false 
    }
    if (typeof json_view_settings !== 'undefined'){
        
        uSim.view_settings=json_view_settings
        uSim.log.view_settings_available=true}
    else{
        uSim.log.view_settings_available=false 
    }
    results={
    "sim": uSim.log.sim_settings_available,
    "agent":uSim.log.agent_settings_available,
    "view":uSim.log.view_settings_available  
    }
    return results    
}

