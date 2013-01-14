$(document).ready(function() {
    $('#map').hide();
    $('#GUIInputForm')[0].reset();
    uSim.simState.simTimer = {};
    uSim.user.data = {};
    uSim.user.data.mapClicks = {};
    uSim.user.data.reports = []
    

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
                update_sim();
                uSim.glo.agentLayer.setVisibility(true);

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

    });

    $('#submitReportButton').click(function() {
    //var report = $("#GUIInputForm").serialize();   
    //uSim.user.data.reports.push(report)
    //var numReports=uSim.user.data.reports.length
   // var report_name="report_"+(numReports-1)
    //$('<input type="hidden">').attr({value:report,name:report_name}).appendTo("#sendReports")
     
    $('#resetReportButton').click()
        
    })

    $('#resetReportButton').click(function() {
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
        $("#GUI2Position").attr("class", "GUI2CompleteBorder")
        $("#GUI2_click_frame").val(uSim.log.sim_frame)
        $("#GUI2ClickStateX").val(uSim.user.clicks.clickLayer.features[0].geometry.x)
        $("#GUI2ClickStateY").val(uSim.user.clicks.clickLayer.features[0].geometry.y)
        
    })
}

function GUIInputs() {

    this.inputs = [];

}

GUIInputs.prototype.setGUIInput = function(GUIType, ID) {

    var inputLength = this.inputs.length
    var array = []
    switch(GUIType) {
        case "select":
            array[0] = GUIType;
            array[1] = ID;
            array[2] = $(ID).val();
            this.inputs.push(array);
            break;
        case "timeStampTicks":
            array[0] = GUIType;
            array[1] = ID;
            array[2] = ID.getTicks();
            this.inputs.push(array);
            break;
        case "timeStampTime":
            array[0] = GUIType;
            array[1] = ID;
            array[2] = ID.getTime();
            this.inputs.push(array);
            break;

        case "mapPoint":
            array[0] = GUIType;
            array[1] = ID;
            array[2] = ID.geometry
            this.inputs.push(array);
            break;

        case "default":
            array[0] = null;
            array[1] = null;
            array[2] = null;
            break;
    }

}
GUIInputs.prototype.getGUIInput = function(ID) {
    var arrayIndex1 = -1;
    $.each(this.inputs, function(index, value) {
        var arrayIndex2 = $.inArray(ID, value)
        if (arrayIndex2 >= 0) {
            arrayIndex1 = index;
        }
    })
    if (arrayIndex1 <= -1) {
        return null;
    } else {
        var value = this.inputs[arrayIndex1][2];
        return value
    }

}
GUIInputs.prototype.getAllInputs = function() {

    return this.inputs;
}
GUIInputs.prototype.updateInputs = function() {

    var array = this.inputs
    var elementID;

    $.each(array, function(index, innerArray) {

        var inputType = innerArray[0]
        switch(inputType) {
            case "select":
                elementID = innerArray[1]
                innerArray[2] = $(elementID).val();
                array[index] = innerArray;
                break;
            case "timeStampTicks":
                elementID = innerArray[1]
                innerArray[2] = elementID.getTicks()
                array[index] = innerArray;
                break;
            case "timeStampTime":
                elementID = innerArray[1]
                innerArray[2] = elementID.getTime()
                array[index] = innerArray;
                break;
            case "mapPoint":
                elementID = innerArray[1]
                innerArray[2] = elementID.geometry;
                array[index] = innerArray;
                break;
        }
    })

    this.inputs = array;
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

