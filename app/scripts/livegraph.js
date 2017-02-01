var dps = []; // dataPoints

google.charts.load('current', {'packages':['corechart']});


var xVal = 0;
var yVal = 100;
var updateInterval = 100;
var dataLength = 500; // number of dataPoints visible at any point


var chart = $('#chartContainer').CanvasJSChart({
  title: {
    text: 'Alpha data'
  },
  data: [{
    type: 'line',
    dataPoints: dps
  }]
});


$(document).ready(function() {

  updateChart(dataLength);
  setInterval(function() { updateChart() }, updateInterval);

});

var updateChart = function(count) {
  count = count || 2;
  // count is number of times loop runs to generate random dataPoints.

  for (var j = 0; j < count; j++) {
    yVal = yVal + Math.round(5 + Math.random() * (-5 - 5));
    dps.push({
      x: xVal,
      y: alpha
    });
    xVal++;
  };
  if (dps.length > dataLength) {
    dps.shift();
  }

  $('#chartContainer').CanvasJSChart().render();

};
