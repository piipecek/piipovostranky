import http_get from "../http_get.js"

let jazyky_table = document.getElementById("jazyky")
let jazyky = JSON.parse(http_get("/admin_api/uprava_jazyku"))

for (let j of jazyky) {
    let tr = document.createElement("tr")
    jazyky_table.appendChild(tr)
    
    let td1 = document.createElement("td")
    td1.innerText = j["system_name"]
    tr.appendChild(td1)
    
    let td2 = document.createElement("th")
    td2.innerText = j["display_name"]
    tr.appendChild(td2)

    let td3 = document.createElement("td")
    td3.innerText = j["number_of_translations"]
    tr.appendChild(td3)

    let button = document.createElement("button")
    button.classList.add("btn", "custom-button")
    button.innerText = "Detail"
    button.type="submit"
    button.name="detail"
    button.value = j["id"]
    
    let td4 = document.createElement("td")
    tr.appendChild(td4)
    td4.appendChild(button)
}