var noSleep = new NoSleep();
var alpha = 0, beta = 0, gamma = 0;
var ax = 0, ay = 0, az =0;
var dataTime = Date.now();

var dataTimer;

$(document).ready(function() {
  $('#chartContainer').attr('disabled', true);
  $('.stopButton').attr('disabled', true);
  $('.stopButton').hide();

  $('#chartContainer').hide();


  $('.startButton').click(function() {
    startButtonClicked();
  });

  $('.stopButton').click(function() {
    stopButtonClicked();
  });
});


// Remove this test stuff
var socket = io('http://thesis-backend.ruub.eu');
$('.infobar').text('Connecting...');

socket.on('hello', function(data) {
  console.log(data);
});

socket.on('disconnect', function() {
  $('.infobar').text('DISCONNECTED');
});

socket.on('connect', function() {
  socket.emit('observer', 'hello' );

  $('.infobar').text('Connected');
});

socket.on('sensorData', function(data) {
  dataTime = data.time;
  alpha = data.alpha;
  beta = data.beta;
  gamma = data.gamma;
  ax = data.accX;
  ay = data.accY;
  az = data.accZ;
});


function startButtonClicked() {
  noSleep.enable();
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', true);
  $('.startButton').hide();
  $('.stopButton').show();
  $('.stopButton').attr('disabled', false);

  $('#chartContainer').attr('disabled', false);
  $('#chartContainer').show();

  startDataStream();
}

function stopButtonClicked() {
  clearInterval(dataTimer);
  noSleep.disable();
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', false);
  $('.startButton').show();
  $('.stopButton').hide();
  $('.stopButton').attr('disabled', true);
  $('#chartContainer').attr('disabled', true);
  $('#chartContainer').hide();

}

function startDataStream() {
  dataTimer = setInterval(function() {
    $('#ga').text('Alpha: ' + alpha);
    $('#gb').text('Beta: ' + beta);
    $('#gg').text('Gamma: ' + gamma);

    $('#ax').text('X: ' + Math.round(Math.abs(ax)));
    $('#ay').text('Y: ' + Math.round(Math.abs(ay)));
    $('#az').text('Z: ' + Math.round(Math.abs(az)));

  }, 100);
}
