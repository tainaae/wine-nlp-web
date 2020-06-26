var receivedData = ""
var geojson;
var postGeojson;
var num = 1;

/*inicia variáveis inicialmente como checked:false*/
var controlVars = {
    "red": false,
    "white": false,
    "rose": false,
    "sweet": false,
    "dry": false,
    "light": false,
    "medium": false,
    "high": false,
    "tannin": false,
    "acid": false,
    "fruit": false,
    "mineral":false,
    "dark": false,
    "yellow": false,
    "young": false,
    "old": false,
    "complex": false,
    "intermediary": false,
    "simple": false
};


function prepare() {
    /* vare cada uma das entradas dos checkboxes
    no array controlVars, com a posiçao dada mapeada pela entrada corrente 
    event.currentTarget.value e armazena o status do checkbox (checked ou 
    unchecked) na variável */
    defMap();
    $("input").on('input', (event) => {
        target = event.currentTarget;
        controlVars[target.value] = target.checked;
    }); 
    
    
    /*quando o botão receber ação de click:
    imprime no terminal os valores das variáveis e 
    chama a função */
    $( "#submit" ).on("click", () => {
        postGeojson = geojson;
        console.log(controlVars);
        getSuggestions(controlVars, postDataCallback);
        if(postGeojson){
            //mymap.removeLayer(postGeojson);
            mymap.remove();
            mymap = L.map('mapid').setView([30, 0], 16);
            defMap();
            num = 1;
            controlVars = {
                "red": false,
                "white": false,
                "rose": false,
                "sweet": false,
                "dry": false,
                "light": false,
                "medium": false,
                "high": false,
                "tannin": false,
                "acid": false,
                "fruit": false,
                "mineral":false,
                "dark": false,
                "yellow": false,
                "young": false,
                "old": false,
                "complex": false,
                "intermediary": false,
                "simple": false
            };

        }
        $('input[type=checkbox]').prop('checked',false); 
    });
    
    $('input[type=checkbox]').each(function() { 
            this.checked = false; 
        });
}

/* carrega função prepare ao carrehgar página html*/
$( document ).ready(() => prepare())

function postDataCallback(data, textStatus) {
    receivedData = data;
    console.log(receivedData);
    receivedData.forEach((i) => {
        name = i.country; 
        pointss = i.points;
        grapeVariety = i.variety;
        //points = i.points;
        geojson = L.geoJson(window[name], {style: style(pointss),
                                          onEachFeature: onEachFeature}).addTo(mymap).bindPopup(num+'º'+' - '+grapeVariety+', '+name);
        num++;
    });
}



/*recebe controlVars e retorna um json com o mesmo  */
function getSuggestions (postData, callback) {
	$.ajax({
    type: "POST",
    url: '/suggestion',
    // data 
    data: JSON.stringify(postData),
    success: callback,
    dataType: 'json',
    contentType: 'application/json;charset=utf-8'
})};

