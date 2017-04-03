var app = require('http').createServer(handler);
var io = require('socket.io')(app);
var fs = require('fs');



var DATA_LIMIT = 20000;

var sensorData = [];
var machineLearners = [];
var observers = [];
var recorderID = null;
var args = process.argv.slice(2);


app.listen(9292);

// Verbose mode -v to output the raw data that was received.
if (args[0] == "-v") {
  console.log('[VERBOSE MODE]');
}

function handler(req, res) {
  fs.readFile(__dirname + '/index.html',
    function(err, data) {
      if (err) {
        res.writeHead(500);
        return res.end('Error loading index.html');
      }

      res.writeHead(200);
      res.end(data);
    });
}

io.on('connection', function(socket) {
  socket.emit('hello', { hello: 'world' });

  socket.on('helloClient', function(data) {
    console.log('New recorder connected ' + socket.id);
  });

  socket.on('newRecorder', function(data) {
    recorderID = socket.id;
    console.log('New recorder was assigned: ' + socket.id + '(' + data + ')');
  });

  socket.on('training', function(data) {
    if (socket.id == recorderID) {
      data.recorderID = recorderID.replace(/[^a-zA-Z0-9]/g, '');
      if (args[0] == "-v") {
        console.log(data);
      }
      sensorData.push(data);
      notifyLearners();
      notifyObservers(data);


      //check if the sensor data isn't too large
      checkDataOverFlow();
    }

  });

  socket.on('classify', function(data) {
    if (socket.id == machineLearners[machineLearners.length - 1]) { // this is the last added machine learner in the array
      notifyObservers(data, 'classify');
      console.log("Latest machinelearner classified: " + data);
    } else {
      console.log("Other machinelearner classified: " + data);
    }
  });

  socket.on('machinelearner', function(data) {
    machineLearners.push(socket.id);
    console.log('machinelearner added: ' + socket.id);
    notifyLearners();
  });

  socket.on('observer', function(data) {
    observers.push(socket.id);
    console.log('observer added: ' + socket.id);
  });


  // UNTESTED CODE!!
  // won't receive a disconnect event now... Maybe that works only from client to server instead of other way round.
  socket.on('disconnect', function(data) {
    var deleteID = machineLearners.indexOf(socket.id);
    if (deleteID !== -1) {
      console.log("Machinelearner disconnect (" + machineLearners[deleteID] + ")");

      machineLearners.splice(deleteID, 1);
      console.log("Machinelearners left: " + machineLearners.length);
    } else {
      deleteID = observers.indexOf(socket.id);
      if (deleteID !== -1) {
        console.log("Observer disconnect (" + observers[deleteID] + ")");
        observers.splice(deleteID, 1);
      }
    }

  });

  function notifyLearners() {
    console.log('broadcasting, data: ' + sensorData.length + ', learners: ' + machineLearners.length + ", observers: " + observers.length);

    while (sensorData.length > 0 && machineLearners.length > 0) {
      var sensorPoint = sensorData.shift();
      for (var i = 0; i < machineLearners.length; i++) {
        io.to(machineLearners[i]).emit('sensorData', sensorPoint);
      }
    }

  } 

// type='data' is only supported in Node V6.0 >= !!
  function notifyObservers(data, type='data') {
    if (observers.length > 0) {
      for (var i = 0; i < observers.length; i++) {
        if (type == 'data') {
          io.to(observers[i]).emit('sensorData', data);
        } else if (type == 'classify') {
          io.to(observers[i]).emit('classify', data);
        }
      }
    }
  }

});

// Overflow prevention, must be removed later.
function checkDataOverFlow() {
  if (sensorData.length > DATA_LIMIT) {
    console.log("FLUSHING DATA, SENSOR ARRAY FULL");
    sensorData = []; //maybe use sensorData.shift() to just leave out the first one (quite memory intensive)
  }
}

io.on('error', function() {});
