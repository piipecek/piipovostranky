import TableCreator from "../table_creator.js"

let budiz_button = document.getElementById("budiz")
let file_input = document.getElementById("file")
let parametry_nacteni_button = document.getElementById("parametry_nacteni_button")
let download_button = document.getElementById("download_button")

parametry_nacteni_button.addEventListener("click", function() {
    document.getElementById("parametry_nacteni").hidden = false
})

let edit_znamky_active = false
let recent_znamka = null
let vahy = null
let hranice_12_input = document.getElementById("hranice_12")
let hranice_23_input = document.getElementById("hranice_23")
let hranice_34_input = document.getElementById("hranice_34")
let hranice_45_input = document.getElementById("hranice_45")
let styl_vypoctu_select = document.getElementById("styl")

styl_vypoctu_select.addEventListener("change", function() {
    if (styl_vypoctu_select.value == "3") {
        hranice_12_input.value = "1.5"
        hranice_23_input.value = "2.5"
        hranice_34_input.value = "3.5"
        hranice_45_input.value = "4.5"
    } else {
        hranice_12_input.value = "80"
        hranice_23_input.value = "65"
        hranice_34_input.value = "50"
        hranice_45_input.value = "35"
    }   
})


let barvy = [
    {
        "znamka": 1,
        "barva": "#2cba00"
    },
    {
        "znamka": 2,
        "barva": "#a3ff00"
    },
    {
        "znamka": 3,
        "barva": "#fff400"
    },
    {
        "znamka": 4,
        "barva": "#ffa700"
    },
    {
        "znamka": 5,
        "barva": "#ff0000"
    },
    {
        "znamka": "Ano",
        "barva": "#2cba00"
    },
    {
        "znamka": "Ne",
        "barva": "#ff0000"
    },
    {
        "znamka": "-",
        "barva": "#ffffff"
    }
    
]


budiz_button.addEventListener("click", function() {
    if (file_input.files[0]) {
        let form_data = new FormData()    
        form_data.append("names_col", document.getElementById("names_col").value)
        form_data.append("results_col", document.getElementById("results_col").value)
        form_data.append("name_row", document.getElementById("name_row").value)
        form_data.append("hranice_12", hranice_12_input.value)
        form_data.append("hranice_23", hranice_23_input.value)
        form_data.append("hranice_34", hranice_34_input.value)
        form_data.append("hranice_45", hranice_45_input.value)
        form_data.append("file", file_input.files[0])
        form_data.append("styl", styl_vypoctu_select.value)

        $.ajax({
            type: "POST",
            url: "/acga_api/vazeny_prumer",
            data : form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                data = JSON.parse(data)
                generate(data)
                vahy = data["vahy"]
                download_button.hidden = false
            }
        })
    } else {
        alert("Nebyl nahrán žádný soubor.")
    }

})


function generate(data) {
    document.getElementById("title").innerText = data.title + " | ACGA"
    let vahy = data["vahy"]
    let studenti = data["studenti"]
    
    let header = ["Jméno"]
    vahy.forEach(element => {
        header.push("Váha " + String(element))
    });
    header.push("Průměr pct.")
    header.push("Kolik chybí")
    header.push("Rezerva")
    header.push("Známka")
    header.push("Klasifikace")
    
    let tc = new TableCreator(document.getElementById("parent_div"), "znamky")
    tc.make_header(header)

    studenti.forEach(s => {
        let row = []
        let colors = [null]
        let tooltips = [null]
        row.push(s["jmeno"])
        vahy.forEach(v => {
            let znamky = s["znamky_dict"].find(x => x["vaha"] == v)["znamky"]
            let znamky_string = znamky.join(", ")
            let znamky_span = document.createElement("span") // proto, abych mu mohl dat event listener
            znamky_span.innerText = znamky_string
            if (znamky_string == "") {
                znamky_span.innerText = "-"
            }
            znamky_span.addEventListener("click", inputize)
            row.push(znamky_span)
            colors.push(null)
            tooltips.push(null)
        })

        row.push(s["prumer_pct"])
        colors.push(null) // průměr
        tooltips.push(s["vypocet"])

        row.push(s["chybi"])
        colors.push(null)
        tooltips.push(null)

        row.push(s["rezerva"])
        colors.push(null)
        tooltips.push(null)
        
        row.push(s["znamka"])
        colors.push(barvy.find(x => x["znamka"] == s["znamka"])["barva"])
        tooltips.push(null)
        
        row.push(s["klasifikovan"])
        colors.push(barvy.find(x => x["znamka"] == s["klasifikovan"])["barva"])
        tooltips.push(null)


        tc.make_row(row, [], colors, tooltips)
    });
    

    let footer_array = ["Průměr"]
    data.prumery_ve_vahach.forEach(element => {footer_array.push(element)})
    footer_array.push(data.prumer_prumeru)
    footer_array.push("-")
    footer_array.push("-")
    footer_array.push(data.prumer_znamka)
    footer_array.push("-")
    tc.make_header(footer_array)


    download_button.addEventListener("click", function() {
        let a = document.createElement("a")
        let file = new Blob([JSON.stringify(data, null, 4)], {type: "text/plain"})
        a.href = URL.createObjectURL(file)
        a.download = "trida.json"
        a.click()
    }) 
}

function inputize() {
    let value = this.innerText
    let width = this.offsetWidth + 5
    edit_znamky_active = true
    recent_znamka = value
    let input = document.createElement("input")
    input.type = "text"
    input.value = value
    input.classList.add("znamka-input")
    input.style.width = width + "px"
    this.replaceWith(input)
    input.focus()
    input.addEventListener("blur", () => {
        save_input_edit(input)
    })
    input.addEventListener("keydown", function(event) {
        if (edit_znamky_active) {
            if (event.key == "Enter") {
                save_input_edit(this)
            }
        }
    })
}

function save_input_edit(input_element) {
    let value = input_element.value
    if (value == "") {
        value = "-"
    }
    edit_znamky_active = false
    let span = document.createElement("span")
    span.innerText = value
    if (value != recent_znamka) {
        span.classList.add("znamka-edited")
    }
    recent_znamka = null
    input_element.replaceWith(span)
    span.addEventListener("click", inputize)
    prepocitat_radek(span)
}

function prepocitat_radek(edited_span_element) {
    function smart_int_float_to_str(x) {
        if (parseInt(x) == x) {
            return String(parseInt(x))
        } else {
            // to 2 decimals
            return String(parseFloat(x.toFixed(2))).replace(".", ",")
        }
    }


    let row = edited_span_element.parentElement.parentElement
    let znamky = []
    let citatel = 0
    let jmenovatel = 0
    let citatel_tooltip_list = []
    let jmenovatel_tooltip_list = []
    for (let i = 0; i < vahy.length; i++) { // priprava znamek jako [[1, 2], [3], [4, 5]]
        let znamky_str = row.children[i + 1].innerText
        if (znamky_str == "-") {
            znamky.push([])
        } else {
            znamky.push(znamky_str.replace(" ", "").split(","))
        }
    }
    for (let i = 0; i < vahy.length; i++) { // vytvorit prumer a jeho vypocet
        for (let znamka of znamky[i]) {
            citatel += parseFloat(znamka) * vahy[i]
            citatel_tooltip_list.push(smart_int_float_to_str(parseFloat(znamka)) + " \\cdot " + vahy[i])
            jmenovatel += vahy[i]
            jmenovatel_tooltip_list.push(vahy[i])
        }
    }

    // prumer
    let prumer = citatel / jmenovatel
    let prumer_str = smart_int_float_to_str(prumer)
    row.children[1 + vahy.length].innerText = prumer_str

    // tooltip
    let citatel_tooltip = citatel_tooltip_list.join(" + ")
    let jmenovatel_tooltip = jmenovatel_tooltip_list.join(" + ") 
    let tooltip = "\\( \\frac{" + citatel_tooltip + "}{" + jmenovatel_tooltip + "} = " + prumer_str + "\\)"
    let tooltip_span = document.createElement("span")
    tooltip_span.classList.add("tooltiptext1", "px-2")
    tooltip_span.innerHTML = tooltip
    row.children[1 + vahy.length].appendChild(tooltip_span)
    MathJax.typeset([tooltip_span])

    // chybi, rezerva a znamka
    let chybi = null
    let rezerva = null
    let znamka = null
    if (styl_vypoctu_select.value == "1" || styl_vypoctu_select.value == "2") {
        if (prumer >= hranice_12_input.value) {
            chybi = 0
            rezerva = prumer - hranice_12_input.value
            znamka = 1
        } else if (prumer >= hranice_23_input.value) {
            chybi = hranice_12_input.value - prumer
            rezerva = prumer - hranice_23_input.value
            znamka = 2
        } else if (prumer >= hranice_34_input.value) {
            chybi = hranice_23_input.value - prumer
            rezerva = prumer - hranice_34_input.value
            znamka = 3
        } else if (prumer >= hranice_45_input.value) {
            chybi = hranice_34_input.value - prumer
            rezerva = prumer - hranice_45_input.value
            znamka = 4
        } else {
            chybi = hranice_45_input.value - prumer
            rezerva = 0
            znamka = 5
        }
    } else if (styl_vypoctu_select.value == "3") {
        if (prumer <= hranice_12_input.value) {
            chybi = 0
            rezerva = hranice_12_input.value - prumer
            znamka = 1
        } else if (prumer <= hranice_23_input.value) {
            chybi = prumer - hranice_12_input.value
            rezerva = hranice_23_input.value - prumer
            znamka = 2
        } else if (prumer <= hranice_34_input.value) {
            chybi = prumer - hranice_23_input.value
            rezerva = hranice_34_input.value - prumer
            znamka = 3
        } else if (prumer <= hranice_45_input.value) {
            chybi = prumer - hranice_34_input.value
            rezerva = hranice_45_input.value - prumer
            znamka = 4
        } else {
            chybi = prumer - hranice_45_input.value
            rezerva = 0
            znamka = 5
        }
    }

    if (chybi == 0) {
        chybi = "-"
    } else {
        chybi = smart_int_float_to_str(chybi)
    }
    if (rezerva == 0) {
        rezerva = "-"
    } else {
        rezerva = smart_int_float_to_str(rezerva)
    }
    row.children[1 + vahy.length + 1].innerText = chybi
    row.children[1 + vahy.length + 2].innerText = rezerva
    row.children[1 + vahy.length + 3].innerText = znamka
    row.children[1 + vahy.length + 3].style.backgroundColor = barvy.find(x => x["znamka"] == znamka)["barva"]
    row.children[1 + vahy.length + 4].innerText = "ručně upraveno" // klasifikace
    row.children[1 + vahy.length + 4].style.backgroundColor = "white"

    
}