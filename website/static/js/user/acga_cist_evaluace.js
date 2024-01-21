import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let acga_jmeno = httpGet("/user_api/get_acga_jmeno")
let evaluace = JSON.parse(httpGet("/user_api/get_evaluace_pro_seznam"))

let generovat_button = document.getElementById("generovat")
let pocet_kodu_input = document.getElementById("pocet_kodu")
let vyplnene_div = document.getElementById("vyplnene")
let nevyplnene_div = document.getElementById("nevyplnene")
let vysledek_div = document.getElementById("vysledek")
let vysledek_button = document.getElementById("vysledek_button")
let vysledek_textarea = document.getElementById("vysledek_textarea")
document.getElementById("acga_jmeno").value = acga_jmeno


generovat_button.addEventListener("click", function() {
    let value = pocet_kodu_input.value
    if (!value) {
        alert("Nebylo zadáno platné číslo.")
    } else if (!acga_jmeno) {
        alert("Nemáte vyplněné jméno učitele.")
    } else {
        $.ajax({
        type: "POST",
        url: "/user_api/vytvorit_evaluace/" + String(value),
        contentType: false,
        processData: false,
        success: function(data) {
            console.log(data)
            vysledek_div.hidden = false
            vysledek_textarea.value = data
            vysledek_button.addEventListener("click", function() {
                let a = document.createElement("a")
                let file = new Blob([data], {type: "text/plain"})
                a.href = URL.createObjectURL(file)
                a.download = "kody.txt"
                a.click()
            })
            }
        })
    }
})

// nejdriv je roztridim, pak udelam tabulky
let vyplnene = []
let nevyplnene = []
for (let e of evaluace) {
    if (e.je_vyplnena) {
        vyplnene.push(e)
    } else {
        nevyplnene.push(e)
    }
}

if (vyplnene.length == 0) {
    vyplnene_div.innerText = "Nejsou tu žádné vyplněné evaluace."
} else {
    for (let e of vyplnene) {
        console.log(e)
    }
}

// tlacitko na mazani
function create_delete_button(id) {
    let b = document.createElement("button")
    b.classList.add("btn", "btn-danger")
    b.innerText = "Smazat"
    b.type = "submit"
    b.name = "smazat_evaluaci"
    b.value = id
    return b
}

// delani tabulek
if (nevyplnene.length == 0) {
    nevyplnene_div.innerText = "Nejsou tu žádné prázdné evaluace. Nově vytvořené se tu zobrazí po obnovení stránky."
} else {
    let tc = new TableCreator(nevyplnene_div)
    tc.make_header(["Datum vytvoření", "Kód", "Smazat"])
    for (let e of nevyplnene) {
        tc.make_row([e.datetime_vytvoreni, e.kod, create_delete_button(e.id)])
    }
}
