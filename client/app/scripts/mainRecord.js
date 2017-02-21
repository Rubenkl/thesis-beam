var noSleep = new NoSleep();
var alpha, beta, gamma;
var ax, ay, az;

var dataTimer;
var movement = 'updown';
var actionType= 'training';

$(document).ready(function() {
  $('.stopButton').attr('disabled', true);
  $('.stopButton').hide();

  $('.startButton').click(function() {
    startButtonClicked();
  });

  $('.stopButton').click(function() {
    stopButtonClicked();
  });

  //movement selection:
  $('.btns-movement > .btn').click(function() {
    $('.btns-movement > .btn').removeClass('active');
    $(this).addClass('active');
    movement = $(this).data('action');
    console.log('movement: ' + movement);
  });

  $('.btns-actiontype > .btn').click(function() {
    $('.btns-actiontype > .btn').removeClass('active');
    $(this).addClass('active');
    actionType = $(this).data('action');
    console.log('action type: ' + actionType);
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
  noSleep.enable();
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', true);
  $('.startButton').hide();
  $('.stopButton').show();
  $('.stopButton').attr('disabled', false);

  startDataStream();

  socket.emit('newRecorder', 'new recorder taking over');
}

function stopButtonClicked() {
  noSleep.disable();
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', false);
  $('.startButton').show();
  $('.stopButton').hide();
  $('.stopButton').attr('disabled', true);
  clearInterval(dataTimer);
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
      movement: movement,
      actionType: actionType,
      alpha: this.alpha,
      beta: this.beta,
      gamma: this.gamma,
      accX: ax,
      accY: ay,
      accZ: az
    });

  }, 100);
}
