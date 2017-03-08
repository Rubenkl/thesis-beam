var Promise = Promise || ES6Promise.Promise; //for some weird shit
var gn = new GyroNorm();
var noSleep = new NoSleep();

var alpha, beta, gamma;
var ax, ay, az;

var dataTimer;
var clicks = 0;
var streaming = false;
var gnArgs = {
  decimalCount: 4,
  logger: logger
};


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


function startButtonClicked() {
  clicks++;
  streaming = true;
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', true);
  $('.startButton').hide();
  $('.stopButton').attr('disabled', false);
  $('.stopButton').show();
  noSleep.enable();

  socket.emit('newRecorder', 'CLASSIFIER');
}

function stopButtonClicked() {

  streaming = false;
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', false);
  $('.stopButton').hide();
  $('.startButton').show();
  $('.stopButton').attr('disabled', true);
  noSleep.disable();
}


// Code copied from here: 
// https://github.com/dorukeker/gyronorm.js/blob/master/demo/index.html
gn.init(gnArgs).then(function() {
  gn.start(function(data) {
    var isAvailable = gn.isAvailable();
    if(!isAvailable.deviceOrientationAvailable) {
      logger('Device orientation is not available.'); 
      gn.stop();
    }
    if(!isAvailable.accelerationIncludingGravityAvailable) {
      logger('Device acceleration incl. gravity is not available.');
      gn.stop();
    } 
    if(!isAvailable.rotationRateAvailable) {
      logger('Device rotation rate is not available.');
      gn.stop();
    }

    //console.log("alpha "+ data.dm.alpha);
    $('#ga').text('Alpha: ' + data.dm.alpha);
    $('#gb').text('Beta: ' + data.dm.beta);
    $('#gg').text('Gamma: ' + data.dm.gamma);

    $('#ax').text('X: ' + data.dm.gx);
    $('#ay').text('Y: ' + data.dm.gy);
    $('#az').text('Z: ' + data.dm.gz);


    if (streaming) {
      socket.emit('training', {
        time: Date.now(),
        sessionCount: clicks,
        movement: 'NULL',
        actionType: 'classify',
        alpha: data.dm.alpha,
        beta: data.dm.beta,
        gamma: data.dm.gamma,
        accX: data.dm.gx,
        accY: data.dm.gy,
        accZ: data.dm.gz
      });
    }
  });
}).catch(function(e) {
  // Accelerometer & Gyroscope not supported
  logger('No Accelerometer & Gyroscope detected..');
});

function logger(data) {
  var html = ` 
  <div class="alert alert-warning alert-dismissible fade in" role="alert">
  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  <strong>Warning!</strong> ` + data + `
</div>
  `;
  $(html).insertAfter('.header');

}
