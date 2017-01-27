var base_url = 'http://192.168.2.13:5001'
base_url = 'http://10.132.2.77:5001'

var fader_card_html = "<div class=\"demo-charts mdl-color--white mdl-shadow--2dp mdl-cell mdl-cell--12-col mdl-grid\">\n" +
"<div style=\"padding:10px 0px 0px 26px; width:100%;color:rgba(0, 0, 0, 0.54)\">\n" + 
                "<strong>Hue</strong>\n" +
              "</div>\n" + 
              "<p style=\"width:100%\">\n" + 
                "<input class=\"mdl-slider mdl-js-slider\" type=\"range\" id=\"s1\" min=\"0\" max=\"100\" value=\"4\" step=\"1\">\n" +
              "</p>\n" + 
              "</div>\n"

var fade_card_active = false




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
        {}, toggleFade);
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

function toggleFade(data, status) {
    if(!fade_card_active) { 
            document.getElementById('faderCard').innerHTML = fader_card_html;
        } else {
            document.getElementById('faderCard').innerHTML = '';

        }
}