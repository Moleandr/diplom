let GraphDiv = document.getElementById('map');

var data = [
    {
          type:'scattergeo',
          lon: 1,
          lat: 1,
          mode: 'lines',
          line: {
              width: 2,
          }
      }
];
var layout = {
    showlegend: false,
    geo:{
        projection: {
            type: 'equirectangular'
        },
        showland: true,
        landcolor: 'rgb(243,243,243)',
        countrycolor: 'rgb(204,204,204)'
    },
    margin: {l: 0, r: 0, b: 0, t: 0},
};

Plotly.newPlot(GraphDiv, data, layout);
