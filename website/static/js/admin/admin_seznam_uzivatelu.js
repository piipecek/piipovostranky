import httpGet from "../http_get.js"
let users_from_db = JSON.parse(httpGet("/admin_api/non_admin_users_from_db"))


function generator_from_db(u, target) {
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
    td2.innerText = u.last_login_datetime

    let td3 = document.createElement("td")
    td3.innerText = u.confirmed
    tr.appendChild(td3)

    let td4 = document.createElement("td")
    tr.appendChild(td4)

    let button = document.createElement("button")
    button.classList.add("btn", "btn-success")
    button.type = "submit"
    button.innerHTML = "Detail usera"
    button.name="result"
    button.value = u.id
    td4.appendChild(button)
}

for (let u of users_from_db) {
    generator_from_db(u, "users")
}
