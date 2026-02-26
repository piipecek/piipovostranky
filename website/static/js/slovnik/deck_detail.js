import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let deck_id = document.getElementById("deck_id").value
let data = JSON.parse(httpGet("/slovnik_api/deck/" + deck_id))
let terms = data["terms"]
let number_of_terms_select = document.getElementById("number_of_terms_select")

let table = new TableCreator(document.getElementById("terms"), null, true)
table.make_header(["Pojem", "Vysvětlení", "Zkoušeno", "Správně", "%"])

for (let term of terms) {
    let percent = 0
    if (term["times_tested"] > 0) {
        percent = Math.round(term["times_correct"] / term["times_tested"] * 100)
    }
    table.make_row([term["front"], term["back"], term["times_tested"], term["times_correct"], percent], [], [], [], "/slovnik/term/" + term["id"])
}

// create options 10, 20, 30 etc. until the number of terms. the first option already in html has value 0 and represents "all"
for (let i = 10; i < data["term_count"]; i += 10) {
    let option = document.createElement("option")
    option.value = i
    option.text = i
    number_of_terms_select.appendChild(option)
}