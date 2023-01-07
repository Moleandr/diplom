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
      geo: {
          projection: {
              type: 'orthographic',
              rotation: {
                  lon: -100,
                  lat: 40
              },
          },
          showocean: true,
          oceancolor: 'rgb(0, 255, 255)',
          showland: true,
          landcolor: 'rgb(230, 145, 56)',
          showlakes: true,
          lakecolor: 'rgb(0, 255, 255)',
          showcountries: true,
          lonaxis: {
              showgrid: true,
              gridcolor: 'rgb(102, 102, 102)'
          },
          lataxis: {
              showgrid: true,
              gridcolor: 'rgb(102, 102, 102)'
          }
      }
  };

  Plotly.newPlot(GraphDiv, data, layout);
