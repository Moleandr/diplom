from backend import export

data = {'end_time': '1000000',
     'objects': [[{'name': 'name', 'value': 'object-1'},
                  {'name': 'latitude', 'value': '0'},
                  {'name': 'longitude', 'value': '0'}],
                 [{'name': 'name', 'value': 'object-2'},
                  {'name': 'latitude', 'value': '60'},
                  {'name': 'longitude', 'value': '50'}]],
     'satellites': [[{'name': 'name', 'value': 'satellite-1'},
                     {'name': 'cluster', 'value': ''},
                     {'name': 'perigeeAltitude', 'value': '800'},
                     {'name': 'apogeeAltitude', 'value': '800'},
                     {'name': 'orbitalInclination', 'value': '30'},
                     {'name': 'ascendingNodeLongitude', 'value': '0'},
                     {'name': 'initialPerigeeArgument', 'value': '0'},
                     {'name': 'opticalRotationAngle', 'value': '60'}],
                    [{'name': 'name', 'value': 'satellite-2'},
                     {'name': 'cluster', 'value': ''},
                     {'name': 'perigeeAltitude', 'value': '800'},
                     {'name': 'apogeeAltitude', 'value': '800'},
                     {'name': 'orbitalInclination', 'value': '50'},
                     {'name': 'ascendingNodeLongitude', 'value': '0'},
                     {'name': 'initialPerigeeArgument', 'value': '0'},
                     {'name': 'opticalRotationAngle', 'value': '60'}]],
     'start_time': '0',
     'step': '100'}

export.simulate(data)
