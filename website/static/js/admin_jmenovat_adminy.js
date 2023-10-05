import httpGet from "./http_get.js"

let uzivatele_pro_udeleni_roli = JSON.parse(httpGet("/admin_api/uzivatele_pro_udeleni_roli"))

function generator_from_db(target, u) {
    let tr = document.createElement("tr")
    document.getElementById(target).append(tr)

    let th = document.createElement("th")
    th.scope = "row"
    th.innerText = u.id
    tr.appendChild(th)

    let td1 = document.createElement("td")
    td1.innerText = u.email
    tr.appendChild(td1)

    let td2 = document.createElement("td")
    tr.appendChild(td2)

    let button = document.createElement("button")
    button.classList.add("btn", "btn-success")
    button.type = "submit"
    button.innerHTML = "vybrat..."
    button.name="result"
    button.value = u.id
    td2.appendChild(button)
}

for (let u of uzivatele_pro_udeleni_roli.users) {   
    generator_from_db("users", u)   
}
for (let u of uzivatele_pro_udeleni_roli.admins) {   
    generator_from_db("admins", u)   
}