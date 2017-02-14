console.log('\'Allo \'Allo!');


// Initialize Firebase
var configFirebase = {
  apiKey: 'AIzaSyDzpvQAbtBMg5dd7Aajiy7itsYvkg499z4',
  authDomain: 'waterbeam-98538.firebaseapp.com',
  databaseURL: 'https://waterbeam-98538.firebaseio.com',
  storageBucket: 'waterbeam-98538.appspot.com',
  messagingSenderId: '733938813147'
};
firebase.initializeApp(configFirebase);


var alpha, beta, gamma;
var ax, ay, az;

var state = {};


$(document).ready(function() {
  $('#chartContainer').attr('disabled', true);

  $('#startButton').click(function() {
    startButtonClicked();
  });
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
  $('#startButton').removeClass('btn-danger');
  $('#startButton').attr('disabled', true);
  $('#startButton').hide();
  $('#chartContainer').attr('disabled', false);

  startDataStream();


}


function startDataStream() {
  setInterval(function() {
    $('#ga').text('Alpha: ' + alpha);
    $('#gb').text('Beta: ' + beta);
    $('#gg').text('Gamma: ' + gamma);

    $('#ax').text('X: ' + Math.round(Math.abs(ax)));
    $('#ay').text('Y: ' + Math.round(Math.abs(ay)));
    $('#az').text('Z: ' + Math.round(Math.abs(az)));

  }, 1000 / 20);
}

