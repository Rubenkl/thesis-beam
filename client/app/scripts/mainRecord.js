var noSleep = new NoSleep();

var Promise = Promise || ES6Promise.Promise; //for some weird shit
var gn = new GyroNorm();
var alpha, beta, gamma;
var ax, ay, az;

var dataTimer;
var movement = 'updown';
var actionType= 'training';
var clicks = 0;
var streaming = false;

var gnArgs = {
  decimalCount: 4,
  logger: logger
};

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



function startButtonClicked() {
  clicks++;
  streaming = true;
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', true);
  $('.startButton').hide();
  $('.stopButton').attr('disabled', false);
  $('.stopButton').show();
  
  // 10 seconds temporary training:
  setTimeout(function(){ stopButtonClicked(); }, 10000);
  noSleep.enable();

  socket.emit('newRecorder', 'new recorder taking over');
}

function stopButtonClicked() {
  $('.startButton').removeClass('btn-danger');
  $('.startButton').attr('disabled', false);
  $('.stopButton').hide();
  $('.startButton').show();
  $('.stopButton').attr('disabled', true);
  clearInterval(dataTimer); //<-- DELETE WHEN USING GYRONORM
  streaming = false;
  noSleep.disable();
}


gn.init(gnArgs).then(function() {
  gn.start(function(data) {
    //console.log("alpha "+ data.dm.alpha);
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
        movement: movement,
        actionType: actionType,
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
