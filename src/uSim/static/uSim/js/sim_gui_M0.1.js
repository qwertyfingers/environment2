$(document).ready(function() {
    $('#map').hide();
    $('#GUIInputForm')[0].reset();
    uSim.simState.simTimer = {};
    uSim.user.data = {};
    uSim.user.data.mapClicks = {};
    uSim.user.data.reports = []
    uSim.GUI={}
    uSim.GUI.report_data={}
    uSim.GUI.report_data.start_report_time=-1;
    uSim.GUI.report_data.start_report_frame=-1;
    uSim.GUI.report_data.end_report_time=-1;
    uSim.GUI.report_data.end_report_frame=-1;
    uSim.GUI.report_data.click_state_time=-1;
    uSim.GUI.report_data.click_state_frame=-1;
    uSim.GUI.report_data.color_select_time=-1;
    uSim.GUI.report_data.color_select_frame=-1;
    uSim.GUI.report_data.size_select_time=-1;
    uSim.GUI.report_data.size_select_frame=-1;
    uSim.GUI.report_data.action_select_time=-1;
    uSim.GUI.report_data.action_select_frame=-1;
    
    
        

    // Once the simulation has loaded, make the view(simulation) visible
    //Bind the function to simLoad, which is a trigger set by the kernel

    $('#map').bind('simLoad', function() {
        var counter = 0;
        uSim.glo.viewLayer.setVisibility(true);
        $('#map').show();
        
        $('#userStartButton').click(function() { //user clicks start button
            if (counter <= 0) {
                bindGUIControls();
                $('#resetReportButton').click(); //reset gui controls at launch
                $("#userStartButton").css("visibility","hidden") // make start button invisible
                $("#GUI2StartFinished").css("visibility","hidden")//keep finished state hidden
                $("#GUI2StartRunning").css("visibility","visible")// make running state visible

                counter = counter + 1;
                uSim.simState.simPlaying = true;
                uSim.glo.mapLayer.setVisibility(true);

// Create a porgress bar and attach it to a div
                var newProgressBar= new GUIProgressBar();
                newProgressBar.initialise(0, 0, uSim.view_settings.views[0].end_frame);
                newProgressBar.setID('#simProgressBar');
                newProgressBar.attachToDiv();
                uSim.simState.GUIProgressBar=newProgressBar;

                var clicks = new GUIClicks()
                var clickLayerStyle = new OpenLayers.StyleMap({
                    "default" : new OpenLayers.Style({
                        pointRadius : 20,
                        fillOpacity : 0.5,
                        fillColor : "#e9f6fd"
                    })
                })

                clicks.setupClickLayer("User Clicks", uSim.glo.map, clickLayerStyle);
                clicks.attachDrawControl();
                uSim.user.clicks = clicks
                uSim.user.clicks.clickLayer.events.register('featureadded', uSim.user.clicks.clickLayer, handleUserClick);
            
            update_sim();
            uSim.glo.agentLayer.setVisibility(true);
            }
        })
    })
})
function bindGUIControls() {
    $('.GUI2ActionButton').click(function() {
        $('.GUI2ActionButton').removeClass('GUI2ButtonSelected');
        $(this).addClass('GUI2ButtonSelected');
        $("#grid1").attr("class", "GUI2CompleteBorder");
        $('#GUI2ActionState').val($(this).val())
        var tf=get_time_and_frame()
        uSim.GUI.report_data.action_select_time=tf[0];
        uSim.GUI.report_data.action_select_frame=tf[1];    

    });

    $('#submitReportButton').click(function() {
    tf=get_time_and_frame()
    uSim.GUI.report_data.end_report_time=tf[0]
    uSim.GUI.report_data.end_report_frame=tf[1]
    $("#GUI2StartReportTime").val(uSim.GUI.report_data.start_report_time)
    $("#GUI2StartReportFrame").val(uSim.GUI.report_data.start_report_frame)
    $("#GUI2EndReportTime").val(uSim.GUI.report_data.end_report_time)
    $("#GUI2EndReportFrame").val(uSim.GUI.report_data.end_report_frame)
    $("#GUI2ClickStateTime").val(uSim.GUI.report_data.click_state_time)
    $("#GUI2ClickStateFrame").val(uSim.GUI.report_data.click_state_frame)
    $("#GUI2ColorSelectTime").val(uSim.GUI.report_data.color_select_time)
    $("#GUI2ColorSelectFrame").val(uSim.GUI.report_data.color_select_frame)
    $("#GUI2ActionSelectTime").val(uSim.GUI.report_data.action_select_time)
    $("#GUI2ActionSelectFrame").val(uSim.GUI.report_data.action_select_frame)
    $("#GUI2SizeSelectTime").val(uSim.GUI.report_data.size_select_time)
    $("#GUI2SizeSelectFrame").val(uSim.GUI.report_data.size_select_frame)
    
    
    
    
    
    
    
    var report=$("#GUIInputForm").serialize();
    uSim.user.data.reports.push(report) 
    var numReports=uSim.user.data.reports.length
    var report_name="report_"+(numReports-1)
    $('<input type="hidden">').attr({value:report,name:report_name}).appendTo("#form_send_reports")
     
    $('#resetReportButton').click()
        
    })

    $('#resetReportButton').click(function() {
    tf=get_time_and_frame()   
    uSim.GUI.report_data.start_report_time=tf[0];
    uSim.GUI.report_data.start_report_frame=tf[1];
    uSim.GUI.report_data.end_report_time=-1;
    uSim.GUI.report_data.end_report_frame=-1;
    uSim.GUI.report_data.click_state_time=-1;
    uSim.GUI.report_data.click_state_frame=-1;
    uSim.GUI.report_data.color_select_time=-1;
    uSim.GUI.report_data.color_select_frame=-1;
    uSim.GUI.report_data.size_select_time=-1;
    uSim.GUI.report_data.size_select_frame=-1;
    uSim.GUI.report_data.action_select_time=-1;
    uSim.GUI.report_data.action_select_frame=-1;
        
        
        
        
        $('#GUIInputForm')[0].reset();
        resetGUIStyle();
        if ( typeof uSim.user.clicks === "undefined") {
        } else {
            if (uSim.user.clicks.clickLayer.features.length > 0) {
                uSim.user.clicks.clickLayer.features[0].destroy()
            }
        }
    })
    function resetGUIStyle() {

        $("#GUI2Time").attr("class", "GUI2NotCompleteBorder")
        $("#GUI2AgentDescription").attr("class", "GUI2NotCompleteBorder")
        $('.GUI2ActionButton').removeClass('GUI2ButtonSelected');
        $("#grid1").attr("class", "GUI2NotCompleteBorder");
        $("#GUI2Position").attr("class", "GUI2NotCompleteBorder")

    }


    $('#colorSelect').change(function() {
        var tf=get_time_and_frame()
        uSim.GUI.report_data.color_select_time=tf[0]
        uSim.GUI.report_data.color_select_frame=tf[1] 

        var selected = $(this).find('option:selected')
        var sizeSelected = $("#sizeSelect").find('option:selected')
        if (selected.val() == "none") {
            $("#GUI2AgentDescription").attr("class", "GUI2NotCompleteBorder")
        } else if (sizeSelected.val() == "none") {
            $("#GUI2AgentDescription").attr("class", "GUI2NotCompleteBorder")
        } else {
            $("#GUI2AgentDescription").attr("class", "GUI2CompleteBorder")
        }

    })

    $('#sizeSelect').change(function() {
        var tf=get_time_and_frame()
        uSim.GUI.report_data.size_select_time=tf[0]
        uSim.GUI.report_data.size_select_frame=tf[1]      
        var selected = $(this).find('option:selected')
        var colorSelected = $("#colorSelect").find('option:selected')
        if (selected.val() == "none") {
            $("#GUI2AgentDescription").attr("class", "GUI2NotCompleteBorder")
        } else if (colorSelected.val() == "none") {
            $("#GUI2AgentDescription").attr("class", "GUI2NotCompleteBorder")
        } else {
            $("#GUI2AgentDescription").attr("class", "GUI2CompleteBorder")
        }

    })

    $('#submitGUIForm').click(function() {
 
    })

    $('#map').bind('userPointCreated', function() {
        
        var tf=get_time_and_frame()
        uSim.GUI.report_data.click_state_time=tf[0]
        uSim.GUI.report_data.click_state_frame=tf[1]
        
        $("#GUI2Position").attr("class", "GUI2CompleteBorder")
        $("#GUI2_click_frame").val(uSim.log.sim_frame)
        $("#GUI2ClickStateX").val(uSim.user.clicks.clickLayer.features[0].geometry.x)
        $("#GUI2ClickStateY").val(uSim.user.clicks.clickLayer.features[0].geometry.y)   
    })



   $('#map').bind('simTick',function(){
       if (uSim.log.sim_frame <=uSim.view_settings.views[0].end_frame){
           uSim.simState.GUIProgressBar.tickAndUpdateBar();
       }
       else{
       uSim.simState.simPlaying=false
       
       $("#submit_to_server").css("visibility","visible")
       $("#resetReportButton").css("visibility","hidden")
       $("#submitReportButton").css("visibility","hidden")
       $('#submitReportButton').unbind()
       $("#userStartButton").css("visibility","hidden") // make start button invisible
       $("#GUI2StartFinished").css("visibility","visible")//keep finished state hidden
       $("#GUI2StartRunning").css("visibility","hidden")// make running state visible
       $("#GUI2StartRunning")
       alert('Sim finished. Click Finish to submit the reports')
       
       
       }
       })

}



function GUIClicks() {
}

GUIClicks.prototype.setupClickLayer = function(layerName, map, layerStyle) {
    if ( typeof layerStyle == 'undefined') {
        this.clickLayer = new OpenLayers.Layer.Vector(layerName);
    } else {
        this.clickLayer = new OpenLayers.Layer.Vector(layerName, {
            styleMap : layerStyle
        })
    }
    this.map = map;
    this.map.addLayer(this.clickLayer);
}
GUIClicks.prototype.attachDrawControl = function() {
    this.clickHandler = new OpenLayers.Control.DrawFeature(this.clickLayer, OpenLayers.Handler.Point)
    this.map.addControl(this.clickHandler)
    this.clickHandler.activate();

}

function handleUserClick(e) {
    if (uSim.user.clicks.clickLayer.features.length >= 2) {
        uSim.user.clicks.clickLayer.features[0].destroy()
    }
    $('#map').trigger('userPointCreated')
}






function GUIProgressBar(){
    this.ID=""; //jQuery div ID
    this.currentValue;//absolute value 
    this.finalValue;//the final value of progress bar
    this.startValue;//the start value of progress bar
    this.customProgress; //user defined progress - ignores start and final values
    this.progress; //the relative progress of bar
}

GUIProgressBar.prototype.setID=function(ID){
    this.ID=ID;
}
GUIProgressBar.prototype.setProgress=function(progress){
    this.customProgress=progress;
};
GUIProgressBar.prototype.setStartValue=function(startValue){
    this.startValue=startValue;
};
GUIProgressBar.prototype.setFinalValue=function(finalValue){
    this.finalValue=finalValue;
};
GUIProgressBar.prototype.setCurrentValue=function(currentValue){
    this.currentValue=currentValue;
};

GUIProgressBar.prototype.initialise=function(startValue,currentValue,finalValue){
    this.setStartValue(startValue);
    this.setCurrentValue(currentValue);
    this.setFinalValue(finalValue);
    var progress=this.getProgress();
    return progress;
}

GUIProgressBar.prototype.getProgress=function(){
    var progress;
            try{
                var percent=(this.finalValue-this.startValue)/100;
                progress=(this.currentValue-this.startValue)/percent;
            }
            catch(err){}
    this.progress=progress;
    return progress
};

GUIProgressBar.prototype.attachToDiv=function(){   
  $(this.ID).progressbar({value: this.progress});     
};

GUIProgressBar.prototype.tickAndUpdateBar=function(){
    var progress;
    currentValue=this.currentValue+1
    this.currentValue=currentValue;
    
    if (currentValue>this.finalValue){
    progress=100;    
    }
    else{
        progress=this.getProgress()
    }
   $(this.ID).progressbar( "option", "value", progress );
    
    
};






