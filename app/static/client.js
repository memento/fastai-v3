var el = x => document.getElementById(x);

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}

function analyze() {
    var uploadFiles = el('file-input').files;
    if (uploadFiles.length != 1){
        alert('Veuillez sélectionner une image à analyser');
        return;
    }

    el('analyze-button').innerHTML = 'Analyse en cours...';
    var xhr = new XMLHttpRequest();
    var loc = window.location
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            var response = JSON.parse(e.target.responseText);
            var responseTable = response['result'].split("/");
            var result = responseTable[1]
            el('result-label').innerHTML = `Resultat = ${result}`;
            el('details-label').innerHTML = `Voici de détail de mon analyse : <br /> ${responseTable[2]} <br /> ${responseTable[3]} <br /> ${responseTable[4]}`;
        }
        el('analyze-button').innerHTML = 'Analyser';
    }

    var fileData = new FormData();
    fileData.append('file', uploadFiles[0]);
    xhr.send(fileData);
}

