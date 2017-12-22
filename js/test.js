/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

var demoRealm = "crossbardemo";
var demoPrefix = "io.crossbar.demo";

// the URL of the WAMP Router (Crossbar.io)
//
var wsuri = "ws://127.0.0.1:8080/ws";


var httpUri = "http://127.0.0.1:8080/lp";

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   // url: wsuri,
   transports: [
      {
         'type': 'websocket',
         'url': wsuri
      },
      {
         'type': 'longpoll',
         'url': httpUri
      }
   ],
   realm: "test"
});


// fired when connection is established and session attached
connection.onopen = function (session, details) {

   main(session);

};

function main (session) {

    console.log('main');

    //
    // Camera
    //
    
    // subscribe the status of the camera
    session.subscribe("test.camera.heartbeat", function(args) {
    	console.log('Sub for test.camera.heartbeat received.');
        $('#camera_heartbeat').val(args[0]);
        $('#camera_heartbeat_status').addClass('running');
        $('#camera_heartbeat_status').css({'background-color':'green'});
        $.when($('#camera_heartbeat_status').stop(true, true)
        		                     .css({'background-color':'green'})
                                     .fadeIn(1000).fadeOut(1000)
                                     .fadeIn(1000).fadeOut(1000)
                                     .fadeIn(1000).fadeOut(1000)
        							 .fadeIn(1000)).then(function(){
        								 $('#camera_heartbeat_status').css({'background-color':'red'});
        							 });
    });

    // subscribe trigger of the camera
    session.subscribe("test.camera.captured", function(args) {
    	console.log('Sub for test.camera.trigger received.');
    	console.log(args);
        $('#camera_captured').html('Yes').show().fadeOut(10000);
    	var img_src = args[0];
        $('#camera_image').html('');
    	var img = $('<img>');
        img.attr('src', img_src);
        img.attr('width', 200);
        img.appendTo('#camera_image');
    });

    // trigger button
    $("#camera_capture").click(function() {
        console.log('camera capture fired');
        session.publish("test.camera.capture", [1], {}, {acknowledge: true, exclude_me: false}).then(
                function(publication) {
                   console.log("test.camera.capture published", publication);
                },
                function(error) {
                   console.log("test.camera.capture publication error", error);
                }
        );
        console.log('end');
        
    });
   
    //
    // calculate
    //
    // subscribe the status of the calculate
    session.subscribe("test.calculate.heartbeat", function(args) {
    	console.log('Sub for test.calculate.heartbeat received.');
        $('#calculate_heartbeat').val(args[0]);
        $('#calculate_heartbeat_status').css({'background-color':'green'});
        $.when($('#calculate_heartbeat_status').stop(true, true)
        		                     .css({'background-color':'green'})
                                     .fadeIn(1000).fadeOut(1000)
                                     .fadeIn(1000).fadeOut(1000)
                                     .fadeIn(1000).fadeOut(1000)
        							 .fadeIn(1000)).then(function(){
        								 $('#calculate_heartbeat_status').css({'background-color':'red'});
        							 });
    });
    // subscribe calculate finished
    session.subscribe("test.calculate.finished", function(args) {
    	console.log('Sub for test.calculate.finished received.');
    	console.log(args);
        $('#calculate_finished').html('Yes').show().fadeOut(10000);
        var result = args[0];
        console.log(result);
        var table = $('<table></table>').addClass('table table-condesed table-striped table-hover');
        table.append($('<tr><th>Species</th><th>Percentage</th></tr>'));
        $.each(result['result'], function(i, v) {
        	console.log(v);
        	table.append($('<tr><td>' + v[0] + '</td><td>' + v[1] + '</td></tr>'));
        });
        console.log('b');

        $('#calculate_result').append(table);
        $('#calculate_image').html('');
    	var img = $('<img>');
    	var img_src = result['image'];
    	console.log(img_src);
        img.attr('src', img_src);
        img.attr('width', 200);
        img.appendTo('#calculate_image');
        console.log('-finished');
    });

    //
    // LoRa
    //
    // subscribe the status of the lora
    session.subscribe("test.lora.heartbeat", function(args) {
    	console.log('Sub for test.lora.heartbeat received.');
        $('#lora_heartbeat').val(args[0]);
        $('#lora_heartbeat_status').css({'background-color':'green'});
        $.when($('#lora_heartbeat_status').stop(true, true)
        		                     .css({'background-color':'green'})
                                     .fadeIn(1000).fadeOut(1000)
                                     .fadeIn(1000).fadeOut(1000)
                                     .fadeIn(1000).fadeOut(1000)
        							 .fadeIn(1000)).then(function(){
        								 $('#lora_heartbeat_status').css({'background-color':'red'});
        							 });
    });
    // subscribe LoRa Sent
    session.subscribe("test.lora.sent", function(args) {
    	console.log('Sub for test.lora.sent received.');
    	console.log(args);
        $('#lora_sent').html('Yes').show().fadeOut(10000);
        var result = args[0];
        console.log(result);
    });
    
    
    //
    // Overall status
    //
    $('#connection_status').html("Connection established.");
}


// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {

   console.log("Connection lost: " + reason);
   $('#connection_status').html("Connection lost: " + reason);

}


// now actually open the connection
//
connection.open();