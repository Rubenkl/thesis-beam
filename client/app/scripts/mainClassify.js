var noSleep = new NoSleep();
var alpha, beta, gamma;
var ax, ay, az;

var dataTimer;
var clicks = 0;


$(document).ready(function() {
  $('.startButton').click(function() {
    startButtonClicked();
  });

  $('.stopButton').click(function() {
    stopButtonClicked();
  });
});


// Remove this test stuff
var socket = io('http://thesis-backend.ruub.eu');
$('.infobar').text('Connecting..');

socket.on('hello', function(data) {
  console.log(data);
  socket.emit('helloClient', 'hello');
});

socket.on('disconnect', function() {
  $('.infobar').html('DISCONNECTED &#10060;');
});

socket.on('connect', function() {
  $('.infobar').html('Connected &#10004;');
});


// DEPRECATED ON HTTP STREAMS!!
window.addEventListener('devicemotion', function(e) {
  ax = e.accelerationIncludingGravity.x;
  ay = e.accelerationIncludingGravity.y;
  az = e.accelerationIncludingGravity.z;
});

window.ondeviceorientation = function(e) {
  alpha = Math.round(event.alpha);
  beta = Math.round(event.beta);
  gamma = Math.round(event.gamma);
};


function startButtonClicked() {
  clicks++;
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', true);
  $('.startButton').hide();
  $('.stopButton').attr('disabled', false);
  $('.stopButton').show();
  startDataStream();
  noSleep.enable();

  socket.emit('newRecorder', 'CLASSIFIER');
}

function stopButtonClicked() {
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', false);
  $('.stopButton').hide();
  $('.startButton').show();
  $('.stopButton').attr('disabled', true);
  clearInterval(dataTimer);
  noSleep.disable();
}

function startDataStream() {
  dataTimer = setInterval(function() {
    $('#ga').text('Alpha: ' + alpha);
    $('#gb').text('Beta: ' + beta);
    $('#gg').text('Gamma: ' + gamma);

    $('#ax').text('X: ' + Math.round(Math.abs(ax)));
    $('#ay').text('Y: ' + Math.round(Math.abs(ay)));
    $('#az').text('Z: ' + Math.round(Math.abs(az)));


    socket.emit('training', {
      time: Date.now(),
      sessionCount: clicks,
      movement: 'NULL',
      actionType: 'classify',
      alpha: this.alpha,
      beta: this.beta,
      gamma: this.gamma,
      accX: ax,
      accY: ay,
      accZ: az
    });

  }, 50);
}
