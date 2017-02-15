var app = require('http').createServer(handler);
var io = require('socket.io')(app);
var fs = require('fs');

var sensorData = [];
var machineLearners = [];

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
    console.log('New client has connected to frontend');
  });

  socket.on('training', function(data) {
    console.log(data);
    sensorData.push(data);
    notifyLearners();
  });

  socket.on('machinelearner', function(data) {
    machineLearners.push(socket.id);
    console.log('machinelearner added: ' + socket.id);
    notifyLearners();
  });


  function notifyLearners() {
    console.log('notify learners, data length: ' + sensorData.length + ', learners: ' + machineLearners.length);

    while (sensorData.length>0 && machineLearners.length > 0) {
      var sensorPoint = sensorData.shift();
      for (var i = 0; i < machineLearners.length; i++) {
        io.to(machineLearners[i]).emit('sensorData', sensorPoint);
      }
    }
  }
});

io.on('error', function() {});
