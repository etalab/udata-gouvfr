const recoUrl = 'https://raw.githubusercontent.com/etalab/datasets_reco/master/reco_json/';
const maxRecos = 2;

function getDatasetId() {
    const selector = '#json_ld';
    const dataset = JSON.parse(document.querySelector(selector).text);
    return dataset && dataset['@id'];
}

function addRecos(recos) {
    const recoContainer = document.getElementById('dataset-recommendations-container');
    let recoChildContainer, recoChildEmbed;
    recos.splice(0, maxRecos).forEach((reco) => {
        recoChildContainer = document.createElement('div');
        recoChildContainer.classList.add('recommendation');
    
        recoChildEmbed = document.createElement('div');
        recoChildEmbed.setAttribute('data-udata-dataset-id', reco[0]);
    
        recoChildContainer.appendChild(recoChildEmbed);
        recoContainer.appendChild(recoChildContainer);
    });
}

function addWidgetScript() {
    const scriptElm = document.createElement('script');
    scriptElm.type = 'application/javascript';
    scriptElm.src = '/static/widgets.js';
    scriptElm.id = 'udata';
    scriptElm.onload = loadDatasets;
    document.body.appendChild(scriptElm);
}

function loadDatasets() {
    udataScript.loadDatasets();
}

function fetchRecos(datasetId) {
    // XXX we can count on fetch polyfill from udata/front/js/mixin.js, right?
    fetch(recoUrl + datasetId + '.json').then((response) => {
        if(response.ok) {
            return response.json();
        }
    }).then((recos) => {
        recos = recos && recos[datasetId];
        if (recos) {
            addRecos(recos);
            addWidgetScript();
            const recoParent = document.getElementById('dataset-recommendations');
            recoParent.style.display = 'block';
        }
    });
}

global.udataDatasetRecos = {
    load () {
        var datasetId = getDatasetId();
        if (datasetId) {
            // TODO remove me
            // * 1 dataset
            // datasetId = '53698e90a3a729239d2034d3';
            // * 2 datasets
            // datasetId = '536991b0a3a729239d203d13'
            fetchRecos(datasetId);
        }
    }
}
