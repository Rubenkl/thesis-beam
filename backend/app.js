var app = require('http').createServer(handler);
var io = require('socket.io')(app);
var fs = require('fs');

var sensorData = [];
var machineLearners = [];
var observers = [];

app.listen(9292);

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
    console.log('New Recorder has connected to frontend');
  });

  socket.on('training', function(data) {
    console.log(data);
    sensorData.push(data);
    notifyLearners();
    notifyObservers(data);
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
      console.log("Machinelearner disconnect ("+machineLearners[deleteID]+")");

      machineLearners.splice(deleteID, 1);
      console.log("Machinelearners left: " + machineLearners.length);
    } else {
      deleteID = observers.indexOf(socket.id);
      if (deleteID !== -1) {
        console.log("Observer disconnect ("+observers[deleteID]+")");
        observers.splice(deleteID, 1);
      }
    }

  });

  function notifyLearners() {
    console.log('notify learners, data length: ' + sensorData.length + ', learners: ' + machineLearners.length);

    while (sensorData.length > 0 && machineLearners.length > 0) {
      var sensorPoint = sensorData.shift();
      for (var i = 0; i < machineLearners.length; i++) {
        io.to(machineLearners[i]).emit('sensorData', sensorPoint);
      }
    }

  }

  function notifyObservers(data) {
    if (observers.length > 0) {
      for (var i=0; i< observers.length; i++) {
        io.to(observers[i]).emit('sensorData', data);
      }
    }
  }

});

io.on('error', function() {});
