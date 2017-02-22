var fs = require('fs');
var socket = require('socket.io-client')('http://thesis-backend.ruub.eu');

var folder = Date.now();

var recorderID = 00000;
var filepath, stream, lastMovement, lastActionType, sessionCount;

socket.on('connect', function (data) {
    socket.emit('machinelearner', { name: 'Ruben PC'});
    console.log('Connected');
  });

socket.on('hello', function(data) {
  console.log("got the hello");
});

socket.on('sensorData', function(data) {
  console.log(data);
  if (data.recorderID == recorderID && data.sessionCount == sessionCount && data.actionType == lastActionType && data.movement == lastMovement) {
    writeData(data.time + ',' + data.alpha + ',' + data.beta + ',' + data.gamma +','+data.accX + ',' + data.accY + ',' + data.accZ + ',' + data.movement + '\n');
  } else {
    recorderID = data.recorderID;
    lastMovement = data.movement;
    lastActionType = data.actionType;
    lastTime = data.time;
    sessionCount = data.sessionCount;

    filepath = 'data/' + data.actionType + '-' + data.movement + '-' + recorderID + '-' + sessionCount + '.csv';
    initWriteFile(filepath);

  }

})

socket.on('disconnect', function(){
  console.log("DISCONNECTED FROM THE SERVER");
});

function initWriteFile(filename) {
  var firstLine = 'timestamp,alpha,beta,gamma,accX,accY,accZ,movement\n';
  stream = fs.createWriteStream(filepath);
  stream.write(firstLine);
}

function writeData(data) {
  stream.write(data);
}


process.stdin.resume();//so the program will not close instantly

process.on('SIGINT', function() {
  socket.close();
  setTimeout(function() {process.exit()} ,1500);
});
