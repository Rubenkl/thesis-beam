var dps = []; // dataPoints

google.charts.load('current', { 'packages': ['corechart'] });



var time = 0;
var updateInterval = 400;
var dataLength = 50; // number of dataPoints visible at any point

var chart, data, options;
/*
var chart = $('#chartContainr').CanvasJSChart({
  title: {
    text: 'Alpha data'
  },
  data: [{
    type: 'line',
    dataPoints: dps
  }]
});
*/

$(document).ready(function() {
  google.charts.setOnLoadCallback(drawChart);
  setInterval(function() { updateChart() }, updateInterval);
});


function drawChart() {
  chart = new google.visualization.LineChart(document.getElementById('chartContainer'));
  
  dps = [
    ['Time', 'X', 'Y', 'Z']
  ];

  data = google.visualization.arrayToDataTable(dps,false);

   options = {
    title: 'Alpha data',
    curveType: 'function',
    legend: { position: 'bottom' }
  };

  chart.draw(data, options);
}


var updateChart = function(count) {
  time++;
  dps.push([time, ax, ay, az]);
  console.log('x: ' + ax + ' y: '+ ay);
  
  if (dps.length > dataLength) {
    dps.shift();
    dps[0] = ['Time', 'X', 'Y', 'Z'];
  }

  data = google.visualization.arrayToDataTable(dps,false);
  chart.draw(data,options);
};
