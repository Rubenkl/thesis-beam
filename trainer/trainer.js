var fs = require('fs');
var socket = require('socket.io-client')('http://thesis-backend.ruub.eu');


socket.on('connect', function (data) {
    socket.emit('machinelearner', { name: 'Ruben PC'});
    console.log('Connected');
  });

socket.on('hello', function(data) {
  console.log("got the hello");
});

socket.on('sensorData', function(data) {
  console.log(data);
})

socket.on('disconnect', function(){
  console.log("DISCONNECTED FROM THE SERVER");
});



process.stdin.resume();//so the program will not close instantly

process.on('SIGINT', function() {
  socket.close();
  setTimeout(function() {process.exit()} ,1500);
});
