var fs = require('fs');
var socket = require('socket.io-client')('http://thesis-backend.ruub.eu');

var CLASSIFY_TIME = 4000; //5 seconds


var folder = Date.now();

// train/test
var recorderID = 0;
var filepath, stream, lastMovement, lastActionType, sessionCount;

// classify
var cPath, cStream, cSessionCount, cRecorderID = 0, cFirstTime;

socket.on('connect', function (data) {
    socket.emit('machinelearner', { name: 'Ruben PC'});
    console.log('Connected');
  });

socket.on('hello', function(data) {
  console.log("Received hello.");
});

socket.on('sensorData', function(data) {
  if (data.actionType == 'classify') {
    classifyData(data);
  } else {
    testtrainData(data);
  }
});


socket.on('disconnect', function(){
  console.log("DISCONNECTED FROM THE SERVER");
});


function testtrainData(data) {
  console.log(data);
  if (data.recorderID == recorderID && data.sessionCount == sessionCount && data.actionType == lastActionType && data.movement == lastMovement) {
    writeData(stream, data.time + ',' + data.alpha + ',' + data.beta + ',' + data.gamma +','+data.accX + ',' + data.accY + ',' + data.accZ + ',' + data.movement + '\n');
  } else {
    recorderID = data.recorderID;
    lastMovement = data.movement;
    lastActionType = data.actionType;
    lastTime = data.time;
    sessionCount = data.sessionCount;

    filepath = 'data/' + data.actionType + '-' + data.movement + '-' + recorderID + '-' + sessionCount + '.csv';
    initWriteFile(filepath);

  }
}


function initWriteFile(filename) {
  var firstLine = 'timestamp,alpha,beta,gamma,accX,accY,accZ,movement\n';
  stream = fs.createWriteStream(filepath);
  stream.write(firstLine);
}

// universal streamtype
function writeData(streamType, data) {
  streamType.write(data);
}

// ------- CLASSIFY -------

function classifyData(data) {

  if (data.recorderID == cRecorderID && data.sessionCount == cSessionCount && (Date.now() - cFirstTime) < CLASSIFY_TIME) {
    writeData(cStream, data.time + ',' + data.alpha + ',' + data.beta + ',' + data.gamma +','+data.accX + ',' + data.accY + ',' + data.accZ + ',' + "NULL" + '\n');
  } else {
    if (cStream)
      cStream.end();
    cFirstTime = Date.now();
    cRecorderID = data.recorderID;
    cLastTime = data.time;
    cSessionCount = data.sessionCount;

    cPath = 'data/CLASSIFY/' + cRecorderID + '-' + cSessionCount + '-' + cFirstTime +  '.csv';

    var firstLine = 'timestamp,alpha,beta,gamma,accX,accY,accZ,movement\n';
    cStream = fs.createWriteStream(cPath);
    cStream.write(firstLine);

    console.log("[CLASSIFY] New datafile created - " + cSessionCount);
  }
}

// ----------- CLOSING ----------------

process.stdin.resume();//so the program will not close instantly

process.on('SIGINT', function() {
  socket.close();
  setTimeout(function() {process.exit();} ,1500);
});
