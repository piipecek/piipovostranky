let textarea = document.getElementById("textarea")
let button = document.getElementById("button")
let download_button = document.getElementById("download")
let canvas_div = document.getElementById('ctverec')

button.addEventListener("click", main)
download_button.addEventListener("click", download)

let chart = null

function parse() {
    let text = textarea.value
    let lines = text.split("\n")
    let lines_parsed = []
    for (let line of lines) {
        if (line == "") {
            continue
        } else {
            line.replace(", ", ",")
            let new_line = line.split(",")
            if (new_line.length == 2) {
                for (let i = 0; i < new_line.length; i++) {
                    if (new_line[i] == "-") {
                        new_line[i] = null
                    } else {
                        new_line[i] = parseInt(new_line[i]);
                    }
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
    document.getElementById("wrapper").hidden = false
    download_button.hidden = false
    let parsed_input = parse()
    if (parsed_input) {
        ocekavana_vs_obdrzena_plot(parsed_input)
        prumerne_hodnoty(parsed_input)
    } else {
        alert("V zadaných známkách je chyba někde, zkuste jí najít a opravit.")
    }
}

function ocekavana_vs_obdrzena_plot(parsed_input) {
    let data = []
    for (let line of parsed_input){
        if (line.includes(null)) {

        } else {
            data.push({
                "x": line[0],
                "y": line[1]
            })
        }
    }

    // vytvoreni canvasu
    canvas_div.innerHTML = null
    let canvas = document.createElement("canvas")
    canvas_div.appendChild(canvas)

    // vyska a sirka canvasu
    let vyska = window.outerHeight
    let sirka = window.outerWidth
    if (vyska > sirka) {
        canvas_div.style.width = sirka*0.9
    } else {
        canvas_div.style.height = vyska*0.9
    }

    let  ctx = canvas.getContext('2d');

    chart = new Chart(ctx, {
        data: {
            datasets: [{
                type: 'scatter',
                label: "Studenti",
                data: data,
                borderColor: "rgb(0,151,10)",
                backgroundColor: "rgb(148,256,148)",
                pointStyle: "cross",
                pointRadius: 5,
                pointHoverRadius: 10,
                borderWidth: 2
              }, {
                type: 'line',
                label: 'y=x',
                data: [{x: 0, y: 0}, {x:100, y:100}],
                pointStyle: false,
                borderColor: "rgb(256,0,0)",
                backgroundColor: "rgb(256,148,148)",
                borderWidth: 1
            }],
        },
        options: {
            aspectRatio: 1.3,
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "Obdržená známka",
                        font: {
                            size: 20
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Očekávaná známka",
                        font: {
                            size: 20
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: "Srovnání očekávaných a obdržených známek",
                    font: {
                        size: 25
                    }
                }
            },
            animation: false
        }
    });
}

function prumerne_hodnoty(parsed_input) {
    let ocekavane_znamky = []
    let obdrzene_znamky = []
    for (let line of parsed_input) {
        ocekavane_znamky.push(line[0])
        obdrzene_znamky.push(line[1])
    }
    ocekavane_znamky = ocekavane_znamky.filter(num => num !== null);
   obdrzene_znamky =obdrzene_znamky.filter(num => num !== null);

    let avg_exp_total = 0
    for (let n of ocekavane_znamky) {
        avg_exp_total += n
    }
    let avg_total = 0
    for (let n of obdrzene_znamky) {
        avg_total += n
    }
    document.getElementById("avg_exp").innerText = String(Math.round(avg_exp_total/ocekavane_znamky.length*100)/100).replace(".",",")
    document.getElementById("avg").innerText = String(Math.round(avg_total/obdrzene_znamky.length*100)/100).replace(".",",")
}

function download() {
    let a = document.createElement('a');
    a.href = chart.toBase64Image("image/png", 1);
    a.download = 'plot.png';
    
    // Trigger the download
    a.click();
}