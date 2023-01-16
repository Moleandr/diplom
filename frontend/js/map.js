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

    // generate objects
    for (let i=0; i < data['objects'].length; i++){
        graphData.push({
            type:'scattergeo',
            mode: 'markers',
            lon: [data['objects'][i][2]['value']],
            lat: [data['objects'][i][1]['value']],
            name: data['objects'][i][0]['value'],
            line: {
                width: 2,
            }
        })
    }

    // generate satellites
    for (let i=0; i < data['satellites'].length; i++){
        // satellites point
        graphData.push({
            type:'scattergeo',
            mode: 'markers',
            lon: [0],
            lat: [0],
            name: data['satellites'][i][0]['value'],
            line: {
                width: 2,
            }
        })

        // satellites view area
        graphData.push({
            type:'scattergeo',
            mode: 'lines',
            lon: [0],
            lat: [0],
            name: `Зона обзора(${data['satellites'][i][0]['value']})`,
            line: {
                width: 2,
            }
        })

        // satellites illuminated area
        graphData.push({
            type:'scattergeo',
            mode: 'lines',
            lon: [0],
            lat: [0],
            name: `Световое пятно(${data['satellites'][i][0]['value']})`,
            line: {
                width: 2,
            }
        })

        for (let j=0; j < data['recipients'].length; j++){
            graphData.push({
            type:'scattergeo',
            mode: 'lines',
            lon: [0],
            lat: [0],
            name: `Зона радиовидимости(${data['satellites'][i][0]['value']}-${data['recipients'][j][0]['value']})`,
            line: {
                width: 2,
                }
            })
        }
    }


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
    await Plotly.animate('map_graph', {
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
    $('#current_time').val(t)
}

