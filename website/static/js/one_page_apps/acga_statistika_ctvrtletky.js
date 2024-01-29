let textarea = document.getElementById("textarea")
let button = document.getElementById("button")
let ocekavana_vs_obdrzena_plot_div = document.getElementById("ocekavana_vs_obdrzena_plot")


button.addEventListener("click", main)


function parse() {
    let text = textarea.value
    let lines = text.split("\n")
    let lines_parsed = []
    for (let line of lines) {
        if (line == "") {
            continue
        }
        if (line.includes("-")){
            continue
        } else {
            let new_line = line.split(", ")
            if (new_line.length == 2) {
                for (let i = 0; i < new_line.length; i++) {
                    new_line[i] = parseInt(new_line[i]);
                }
                lines_parsed.push(new_line)
            } else {
                return null
            }
        }
    }
    return lines_parsed
}


function main() {
    let parsed_input = parse()
    if (parsed_input) {
        ocekavana_vs_obdrzena_plot(parsed_input)
        console.log(parsed_input)
    } else {
        alert("V zadaných známkách je chyba někde, zkuste jí najít a opravit.")
    }
}

function ocekavana_vs_obdrzena_plot(parsed_input) {
    let x = []
    let y = []
    for (let line of parsed_input){
        x.push(line[0])
        y.push(line[1])
    }
    let data = [
        {
            x: x,
            y: y,
            marker: {
                color: "blue"
            }
        }]
    
    let layout = {
        yaxis: {
            title: 'Výdaje [Kč]',
            rangemode: "tozero",
            autosize: true
        }
    }
    
    let config = {
        responsive: true
    }

    Plotly.new_plot(ocekavana_vs_obdrzena_plot_div, data, layout, config)
}