import httpGet from "../http_get.js"

let deck_id = document.getElementById("deck_id").value
let term_div =  document.getElementById("term_div")
let new_term_button = document.getElementById("new_term")
let save_button = document.getElementById("save_button")
let form = document.getElementById("form")
let result_input = document.getElementById("result")
let swap_button = document.getElementById("swap")

swap_button.addEventListener("click", function() {
    for (let child of term_div.children) {
        let front_input = child.children[0].children[0]
        let back_input = child.children[1].children[0]
        let temp = front_input.value
        front_input.value = back_input.value
        back_input.value = temp
    }
})

let deck = JSON.parse(httpGet("/slovnik_api/deck/" + deck_id))
let new_term_id = 0

new_term_button.addEventListener("click", function() {
    make_empty_term_row()
})

save_button.addEventListener("click", function() {
    save()
})


function make_term_row(term) {
    let front_input = document.createElement("input")
    front_input.type = "text"
    front_input.value = term.front
    front_input.classList.add("form-control")
    front_input.placeholder = "pojem"
    let back_input = document.createElement("input")
    back_input.type = "text"
    back_input.value = term.back
    back_input.classList.add("form-control")
    back_input.placeholder = "vysvětlení"
    let delete_button = document.createElement("button")
    delete_button.classList.add("red-button")
    delete_button.innerText = "X"
    delete_button.addEventListener("click", function() {
        remove_term(term.id)
    })
    let row = document.createElement("div")
    row.id = "term_row_" + term.id
    row.classList.add("row", "align-items-center", "g-2", "mb-2")
    let front_col = document.createElement("div")
    front_col.classList.add("col")
    front_col.appendChild(front_input)
    let back_col = document.createElement("div")
    back_col.classList.add("col")
    back_col.appendChild(back_input)
    let delete_col = document.createElement("div")
    delete_col.classList.add("col-auto")
    delete_col.appendChild(delete_button)
    row.appendChild(front_col)
    row.appendChild(back_col)
    row.appendChild(delete_col)

    back_input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault()
            make_empty_term_row()
        }
    })

    
    term_div.appendChild(row)
    front_input.focus()
}


function make_empty_term_row() {
    let empty_term = {
        front: "",
        back: "",
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
        let front = child.children[0].children[0].value
        let back = child.children[1].children[0].value
        let id = child.id.replace("term_row_", "")
        let is_new = id.startsWith("new_")
        if (!is_new) {
            id = parseInt(id)
        } else {
            id = null
        }
        
        if (front.trim() == "" && back.trim() == "") {
            continue
        }
        terms.push({
            id: id,
            is_new: is_new,
            front: front,
            back: back
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