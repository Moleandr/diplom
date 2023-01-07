function generateTab(name){
    return`<a class="item" data-tab="${name}">${name}</a>`
}

function generateTabContent(name, fields) {
    fields.unshift(
        {'text': 'Наименование', 'name': 'name', 'value': name, 'disabled': true},
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
            <input type="text" name=${elem.name} value="${elem.value ? elem.value: ""}">
        </div>
    `)
    form += '</form>'
    return form
}

function simulate () {
    console.log("simulate run")
}