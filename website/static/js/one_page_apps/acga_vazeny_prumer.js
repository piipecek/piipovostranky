import TableCreator from "../table_creator.js"

let budiz_button = document.getElementById("budiz")
let file_input = document.getElementById("file")

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
    }
    
]


budiz_button.addEventListener("click", function() {
    if (file_input.files[0]) {
        let form_data = new FormData()    
        form_data.append("names_col", document.getElementById("names_col").value)
        form_data.append("results_col", document.getElementById("results_col").value)
        form_data.append("name_row", document.getElementById("name_row").value)
        form_data.append("hranice_12", document.getElementById("hranice_12").value)
        form_data.append("hranice_23", document.getElementById("hranice_23").value)
        form_data.append("hranice_34", document.getElementById("hranice_34").value)
        form_data.append("hranice_45", document.getElementById("hranice_45").value)
        form_data.append("file", file_input.files[0])

        $.ajax({
            type: "POST",
            url: "/acga_vazeny_prumer",
            data : form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                generate(data)
            }
        })
    } else {
        alert("Nebyl nahrán žádný soubor.")
    }

})

function generate(data) {
    data = JSON.parse(data)
    let vahy = data["vahy"]
    let studenti = data["studenti"]
    
    let header = ["Jméno"]
    vahy.forEach(element => {
        header.push("Váha " + String(element))
    });
    header.push("Průměr pct.")
    header.push("Známka")
    header.push("Klasifikace")
    
    let tc = new TableCreator(document.getElementById("parent_div"))
    tc.make_header(header)

    studenti.forEach(s => {
        let row = []
        let colors = [null]
        let tooltips = [null]
        row.push(s["jmeno"])
        vahy.forEach(v => {
            row.push(s["znamky_dict"].find(x => x["vaha"] == v)["znamky"])
            colors.push(null)
            tooltips.push(null)
        })

        row.push(s["prumer_pct"])
        colors.push(null) // průměr
        tooltips.push(s["vypocet"])
        
        row.push(s["znamka"])
        colors.push(barvy.find(x => x["znamka"] == s["znamka"])["barva"])
        tooltips.push(null)
        
        row.push(s["klasifikovan"])
        colors.push(barvy.find(x => x["znamka"] == s["klasifikovan"])["barva"])
        tooltips.push(null)


        tc.make_row(row, [], colors, tooltips)
    });



}