import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let terms = JSON.parse(httpGet("/slovnik_api/decks"))

let table = new TableCreator(document.getElementById("decks"), null, true)
table.make_header(["Název", "Vytvořeno", "Počet slovíček"])

for (let term of terms) {
    table.make_row([term["name"], term["datetime"], term["term_count"]], [], [], [], "/slovnik/deck/" + term["id"])
}
