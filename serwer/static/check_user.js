function posiadana() {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'cechy', false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function checker(e) {
    let v = e.target.value;
    let posiadane = posiadana();
    e.target.setCustomValidity("");
    for (let index = 0; index < posiadane.length; index++) {
        const element = posiadane[index];
        if (element.localeCompare(v.toLowerCase()) == 0) {
            e.target.setCustomValidity('Taka cecha już została zaproponowana')
            e.target.reportValidity();
            break
        }
    }
}

document.getElementById('cechaID').addEventListener('input', checker)