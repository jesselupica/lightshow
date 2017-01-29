var base_url = 'http://192.168.2.13:5001'
base_url = 'http://localhost:5001'


$(document).ready(function(){

    $("#offLights").click(function(){
        $.post(base_url + '/api/toggleLights',
        {},
        toggleLights);
    });

    $("#toggleFade").click(function(){
    	
    	fade_card_active = !fade_card_active

        $.post(base_url + '/api/toggleFade',
        { default:true, rate:10 }, toggleLights);
    });

    $("#toggleVisMusic").click(function(){
        
        $.post(base_url + '/api/toggleVisMusic',
        {});
    });

    $(".spectrum-button").click(function(){
        
        $.post(base_url + '/api/setSpectrum',
        {spectrum:$(this).attr('data-spec')});
    });

    $(".static-color-button").click(function(){
        
        $.post(base_url + '/api/setStaticColor',
        {color:$(this).attr('id')});
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

function toggleLights(data, status) {
	if ($("#offLights").text() == 'Off') {
        $("#offLights").text("On");
    } else {
        $("#offLights").text("Off");
    }
}
