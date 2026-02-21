import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"


let generovat_button = document.getElementById('generovat_button');

generovat_button.addEventListener('click', function() {
    let prijmeni = document.getElementById('prijmeni').value;
    let adress = "/acga_api/astrofyzika/" + prijmeni;
    let response = JSON.parse(httpGet(adress));
    createTable(response)
})

// Tady byla funkce pro výpočet výsledku. První tento fakt exploitnula Eliška Rokosová (JU3A) za pomoci jejích známých 29. 5. 2024. Od té doby probíhá výpočet na serveru a výsledek se pouze zobrazuje v tabulce.

function createTable(data) {

    let table = new TableCreator(document.getElementById("zadani"));
    table.make_header(["veličina", "hodnota"])
    table.make_row(["\\(x_1\\)", "\\(" + String(data[0]) + "\\)"])
    table.make_row(["\\(y_1\\)", "\\(" + String(data[1]) + "\\)"])
    table.make_row(["\\(x_2\\)", "\\(" + String(data[2]) + "\\)"])
    table.make_row(["\\(y_2\\)", "\\(" + String(data[3]) + "\\)"])
    table.make_row(["\\(v_{1x}\\)", "\\(" + String(data[4]) + "\\)"])
    table.make_row(["\\(v_{1y}\\)", "\\(" + String(data[5]) + "\\)"])
    table.make_row(["\\(m\\)", "\\(" + String(data[6]) + "\\)"])
    table.make_header(["výsledek", String(data[7])])
    MathJax.typeset()
}