function generateTab(name){
    return`<a class="item" data-tab="${name}">${name}</a>`
}

function generateTabContent(name, fields) {
    fields.unshift(
        {'text': 'Наименование', 'name': 'name', 'value': name, 'disabled': true, 'type': 'text'},
    )
    return `
    <div class="ui tab segment" data-tab="${name}" id="${name}">
        ${generateForm(fields)}
    <div/>
    `
}

function generateForm(data) {
    let form = '<form class="ui form">'
    data.forEach(elem => form += `
        <div class="${elem.disabled ? "disabled ": ""}field">
            <label>${elem.text}</label>
            <input type=${elem.type} name=${elem.name} value="${elem.value ? elem.value: ""}">
        </div>
    `)
    form += '</form>'
    return form
}


function generateCheckboxForm(data) {
    return `
        <div class="ui segment">
            <form class="ui form">
                ${data.map((elem) => `
                    <div class="inline field">
                        <div class="ui toggle checkbox">
                            <input type="checkbox" tabindex="0" class="hidden" name="${elem.name}">
                            <label>${elem.name}</label>
                        </div>
                    </div>
                `).join("")}
            </form>
        </div>
    `
}


function getForms(selector) {
    return $(selector).toArray().map(function (form) {return $(form).serializeArray()})
}


eel.expose(setProgress);
function setProgress (percent) {
    $('.bar').css('width', `${percent}%`)
    $('.progress .label').text(`${percent}%`)
}

eel.expose(setPeriodicitySettings);
function setPeriodicitySettings (settings) {
    $('#periodicity_settings .segment').remove()
    $('#periodicity_settings').prepend(generateCheckboxForm(settings))
    $('.ui.checkbox').checkbox()
}

async function PeriodicityIndicatorGraph() {
    let keys = $('#periodicity_settings .checkbox.checked input').toArray()
        .map((el) => el.name.split("|"))
    let values = await eel.get_last_simulate()()
    let data = [{'x': [], 'y': [], 'type': 'bar'}]
    keys.forEach(function(key) {
        data[0]['x'].push(`${key[0]}|${key[1]}`)
        data[0]['y'].push(values[key[0]][key[1]]['periodicity_indicator'])
    });
    let GraphDiv = $('#periodicity_graph');
    Plotly.newPlot('periodicity_graph', data);
}

async function simulate () {
    let data = {}
    data['satellites'] = getForms('#satellite-tab-content form')
    data['objects'] = getForms('#object-tab-content form')
    data['start_time'] = $('#start_time').val()
    data['end_time'] = $('#end_time').val()
    data['step'] = $('#step').val()
    console.log(await eel.simulate(data)())
}