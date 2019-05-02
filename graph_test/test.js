var trace1 = {
  x: [0.001,
    0.002,
    0.004,
    0.008,
    0.016,
    0.032,
    0.064,
    0.128,
    0.256,
    0.512,
    1.024,
    2.048,
    4.096,
    8.192
  ],
  y: [27.8019,
    22.7035,
    17.0309,
    13.0461,
    9.4542,
    7.2952,
    6.1115,
    5.6269,
    5.3649,
    5.2685,
    5.2488,
    5.2466,
    5.2369,
    5.2366
  ],
  mode: 'lines+markers',
  name: 'asd',
  type: 'scatter'
}
var trace2 = {
  x: [2, 3, 4, 5],
  y: [16, 5, 11, 9],
  mode: 'lines+markers',
  name: 'Lines'
};

var trace3 = {
  x: [1, 2, 3, 4],
  y: [12, 9, 15, 12],
  mode: 'lines+markers',
  name: 'Scatter and Lines'
};

var data = [trace1, trace2, trace3];

var layout = {
  title: 'Miss Rate (%) VS. Cache Size',
  yaxis: {
    title: 'Miss Rate %'
  },
  xaxis: {
    title: 'Cache Size KB'
  }
};

Plotly.newPlot('myDiv', data, layout);