var base_url = 'http://192.168.2.13:5001'
base_url = 'http://localhost:5001'


$(document).ready(function(){

    $("#offLights").click(function(){
        $.post(base_url + '/api/toggleLights',
        {},
        toggleLights);
    });

    $("#toggleFade").click(function(){
    	
        $.post(base_url + '/api/toggleFade',
        {}, updateSliders);
    });

    $("#toggleVisMusic").click(function(){
        
        $.post(base_url + '/api/toggleVisMusic',
        {}, updateSliders);
    });

    $(".spectrum-button").click(function(){
        
        $.post(base_url + '/api/setSpectrum',
        {spectrum:$(this).attr('data-spec')}, updateSliders);
    });

    $(".static-color-button").click(function(){
        console.log("stuff")
        $.post(base_url + '/api/setStaticColor',
        {color:$(this).attr('id')}, updateSliders);
    });
    
});

function hueChanged(value, max) {
    console.log("I hate front end " + value);
    $.post(base_url + '/api/setHue',
        {hue:value/max});
}

function satChanged(value, max) {
    $.post(base_url + '/api/setSat',
        {sat:value/max});
}

function brightChanged(value, max) {
    $.post(base_url + '/api/setBri',
        {bri:value/max});
}

function updateSliders() {
    console.log('is this getting called');
    $.getJSON( base_url + '/api/state', {} )
      .done(function( json ) {
        console.log( "JSON Data: " + json.hue);
        $("#hueSlider").get(0).MaterialSlider.change(json.hue * $("#hueSlider").attr('max'));
        $("#satSlider").get(0).MaterialSlider.change(json.saturation * $("#satSlider").attr('max'));
        $("#brightSlider").get(0).MaterialSlider.change(json.value * $("#brightSlider").attr('max'));

      })
      .fail(function( jqxhr, textStatus, error ) {
        var err = textStatus + ", " + error;
        console.log( "Request Failed: " + err );
    });

}

function toggleLights(data, status) {
	if ($("#offLights").text() == 'Off') {
        $("#offLights").text("On");
    } else {
        $("#offLights").text("Off");
    }
}
