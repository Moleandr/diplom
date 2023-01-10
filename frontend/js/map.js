function generateEmptyMap() {
    let data = [{type:'scattergeo'}];
    let layout = {
        geo:{
            scope: 'world',
            projection: {
                type: 'equirectangular'
            },
            showland: true,
            landcolor: 'rgb(243,243,243)',
            countrycolor: 'rgb(204,204,204)',
        },
        width: 900,
        height: 400,
        margin: {r: 0, t: 0, b: 0, l: 0},
    };
    Plotly.newPlot("map_graph", data, layout);
}


function generateMap(data) {
    let graphData = []
    // generate point on Earth
    graphData = graphData.concat(data['objects'].map(function (el) {
        return {
            type:'scattergeo',
            mode: 'markers',
            lon: [el[2]['value']],
            lat: [el[1]['value']],
            name: el[0]['value'],
            line: {
                width: 2,
            }
        }
    }))
    // generate starting point for satellites
    graphData = graphData.concat(data['satellites'].map(function (el) {
        return {
            type:'scattergeo',
            mode: 'markers',
            lon: [0],
            lat: [0],
            name: el[0]['value'],
            line: {
                width: 2,
            }
        }
    }))
    // generate circle for view area
    graphData = graphData.concat(data['satellites'].map(function (el) {
        return {
            type:'scattergeo',
            mode: 'lines',
            lon: [0],
            lat: [0],
            name: `${el[0]['value']}-view-area`,
            line: {
                width: 2,
            }
        }
    }))
    // generate circle for illuminated area
    graphData.push(
        {
            type:'scattergeo',
            mode: 'lines',
            lon: [0],
            lat: [0],
            name: `illuminated-area`,
            line: {
                width: 2,
            }
        }
    )
    console.log(data.length)

    let layout = {
        geo:{
            scope: 'world',
            projection: {
                type: 'equirectangular'
            },
            showland: true,
            landcolor: 'rgb(243,243,243)',
            countrycolor: 'rgb(204,204,204)',
        },
        width: 900,
        height: 400,
        margin: {r: 0, t: 0, b: 0, l: 0},
    };
    Plotly.newPlot("map_graph", graphData, layout);
}

async function updateMap (data, t) {
    Plotly.animate('map_graph', {
            data: await eel.map_simulation(data, t)()
        },
        {
            transition: {
                duration: 0
            },
            frame: {
                duration: 0,
                redraw: true
            }
      });
}