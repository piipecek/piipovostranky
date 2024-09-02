// Function to convert CSV data to an array of objects
function csvToObjectArray(csv) {
    const lines = csv.split('\n');
    let start_index = 0
    if (lines[0].includes("Pohyby na účtu")) {
        start_index = 2
    }
    const headers = lines[start_index].split(';');
    const platby = []
    const popisky = []

    // pro zjisteni rozsahu mesicu, labelu na grafy a poradi
    let roky_mesice_kombinace = []
    let tokeny = []
    for (let i = start_index+1; i < lines.length; i++) {
        const currentLine = lines[i].split(';');
        if (currentLine[0] == "") {  // ochrana proti tomu poslednimu prazdnymu
            continue
        }
        let mesice = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen", "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
        let mesic = currentLine[1].split(".")[1]
        let rok = currentLine[1].split(".")[2]
        let label = mesice[parseInt(mesic)-1] + " " + rok
        let token = rok + mesic
        let novy_zaznam = {
            "token": token,
            "label": label
        }

        if (!tokeny.includes(token)) {
            tokeny.push(token)
            roky_mesice_kombinace.push(novy_zaznam)
        }
    }

    roky_mesice_kombinace.sort((a, b) => a.token.localeCompare(b.token))
    for (let i = 0; i < roky_mesice_kombinace.length; i++) {
        popisky.push({"token": roky_mesice_kombinace[i].token, "poradi_datum": i, "label": roky_mesice_kombinace[i].label})
    }

    // pairsovani csvcka
    for (let i = start_index+1; i < lines.length; i++) {
        const obj = {};
        const currentLine = lines[i].split(';');
        
        if (currentLine[0] == "") {  // ochrana proti tomu poslednimu prazdnymu
            continue
        }

        let misto = ""
        if (currentLine[14].includes("Místo:")) {
            misto = currentLine[14].split("Místo: ")[1]
        }

        obj["datum"] = currentLine[1];
        obj["castka"] = -parseFloat(currentLine[2].replace(",","."))
        obj["misto"] = misto
        obj["cislo_protiuctu"] = currentLine[5]
        obj["zprava"] = currentLine[14]
        obj["rok"] = currentLine[1].split(".")[2]
        obj["mesic"] = currentLine[1].split(".")[1]
        for (let popisek of popisky) {
            if (popisek.token == obj["rok"] + obj["mesic"]) {
                obj["poradi"] = popisek.poradi_datum
            }
        }
        platby.push(obj);
    }
    return {
        "platby": platby,
        "popisky": popisky
    };
}


export default csvToObjectArray