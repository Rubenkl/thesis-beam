var alpha, beta, gamma;
var ax, ay, az;

var dataTimer;

$(document).ready(function() {
  $('#chartContainer').attr('disabled', true);
  $('.stopbutton').attr('disabled', true);
  $('.stopbutton').hide();

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
socket.on('hello', function(data) {
  console.log(data);
  socket.emit('helloClient', 'hello' );
});

socket.on('disconnect', function() {
  $('.infobar').text('DISCONNECTED');
});

socket.on('connect', function() {
  $('.infobar').text('Connected');
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
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', true);
  $('.startButton').hide();
  $('.stopButton').show();
  $('.stopButton').attr('disabled', false);

  $('#chartContainer').attr('disabled', false);
  $('#chartContainer').show();

  startDataStream();
  socket.emit('my other event', { test: 'Pressed button' });
}

function stopButtonClicked() {
  clearInterval(dataTimer);
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


    socket.emit('training', {
      alpha: this.alpha,
      beta: this.beta,
      gamma: this.gamma,
      accX: ax,
      accY: ay,
      accZ: az
    });

  }, 300);
}
