import httpGet from "./http_get.js"
let id_usera = document.getElementById("id_getter").value
let detail_usera = JSON.parse(httpGet("/admin_api/detail_usera/" + String(id_usera)))

for (let k of Object.keys(detail_usera)) {
    document.getElementById(k).innerText = detail_usera[k]
}
