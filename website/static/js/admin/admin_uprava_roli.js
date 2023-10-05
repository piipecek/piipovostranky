import http_get from "../http_get.js"

let roles = JSON.parse(http_get("/admin_api/info_pro_upravu_roli"))
let stavajici_role_div = document.getElementById("stavajici_role")

for (let role of roles) {
    let tr = document.createElement("tr")
    stavajici_role_div.appendChild(tr)

    let th = document.createElement("th")
    th.innerText = role["system_name"]
    tr.appendChild(th)

    let td1 = document.createElement("td")
    td1.innerText = role["display_name"]
    tr.appendChild(td1)

    let td2 = document.createElement("td")
    td2.innerText = role["number_of_users"]
    tr.appendChild(td2)
    
    let td3 = document.createElement("td")
    tr.appendChild(td3)
    let button = document.createElement("button")
    button.classList.add("btn", "btn-danger")
    button.innerHTML = "Smazat"
    button.name="smazat"
    button.value = role["system_name"]
    
    td3.appendChild(button)

}

