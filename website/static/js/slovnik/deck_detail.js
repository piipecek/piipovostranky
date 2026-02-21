import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let deck_id = document.getElementById("deck_id").value
let data = JSON.parse(httpGet("/slovnik_api/deck/" + deck_id))
let terms = data["terms"]

let table = new TableCreator(document.getElementById("terms"), null, true)
table.make_header(["Definice", "Překlad", "Zkoušeno", "Správně"])

for (let term of terms) {
    table.make_row([term["definition"], term["translation"], term["times_tested"], term["times_correct"]], [], [], [], "/slovnik/term/" + term["id"])
}
