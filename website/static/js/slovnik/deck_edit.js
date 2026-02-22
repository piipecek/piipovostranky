import httpGet from "../http_get.js"

let deck_id = document.getElementById("deck_id").value
let term_div =  document.getElementById("term_div")
let new_term_button = document.getElementById("new_term")
let save_button = document.getElementById("save_button")
let form = document.getElementById("form")
let result_input = document.getElementById("result")

let deck = JSON.parse(httpGet("/slovnik_api/deck/" + deck_id))
let new_term_id = 0

new_term_button.addEventListener("click", function() {
    make_empty_term_row()
})

save_button.addEventListener("click", function() {
    save()
})


function make_term_row(term) {
    let definition_input = document.createElement("input")
    definition_input.type = "text"
    definition_input.value = term.definition
    definition_input.classList.add("form-control")
    definition_input.placeholder = "definice"
    let translation_input = document.createElement("input")
    translation_input.type = "text"
    translation_input.value = term.translation
    translation_input.classList.add("form-control")
    translation_input.placeholder = "překlad"
    let delete_button = document.createElement("button")
    delete_button.classList.add("red-button")
    delete_button.innerText = "X"
    delete_button.addEventListener("click", function() {
        remove_term(term.id)
    })
    let row = document.createElement("div")
    row.id = "term_row_" + term.id
    row.classList.add("row", "align-items-center", "g-2", "mb-2")
    let definition_col = document.createElement("div")
    definition_col.classList.add("col")
    definition_col.appendChild(definition_input)
    let translation_col = document.createElement("div")
    translation_col.classList.add("col")
    translation_col.appendChild(translation_input)
    let delete_col = document.createElement("div")
    delete_col.classList.add("col-auto")
    delete_col.appendChild(delete_button)
    row.appendChild(definition_col)
    row.appendChild(translation_col)
    row.appendChild(delete_col)

    translation_input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault()
            make_empty_term_row()
        }
    })

    
    term_div.appendChild(row)
    definition_input.focus()
}


function make_empty_term_row() {
    let empty_term = {
        definition: "",
        translation: "",
        id: "new_" + new_term_id
    }
    new_term_id++
    make_term_row(empty_term)
}


function remove_term(term_id) {
    let row = document.getElementById("term_row_" + term_id)
    row.remove()
}


function save() {
    let terms = []
    let deck_name = document.getElementById("deck_name").value
    for (let child of term_div.children) {
        let definition = child.children[0].children[0].value
        let translation = child.children[1].children[0].value
        let id = child.id.replace("term_row_", "")
        let is_new = id.startsWith("new_")
        if (!is_new) {
            id = parseInt(id)
        } else {
            id = null
        }
        
        if (definition.trim() == "" && translation.trim() == "") {
            continue
        }
        terms.push({
            id: id,
            is_new: is_new,
            definition: definition,
            translation: translation
        })
    }

    result_input.value = JSON.stringify({
        deck_name: deck_name,
        terms: terms
    })
    form.submit()
}


for (let term of deck.terms) {
    make_term_row(term)
}