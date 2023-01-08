let GraphDiv = document.getElementById('map');
let traceA = {
  x: [1, 2, 3, 4, 16, 17, 26],
  y: [1, 40, 9, 60, 4, 20, 10],
  type: 'scatter'
};
let data = [traceA]



Plotly.newPlot(GraphDiv, data);