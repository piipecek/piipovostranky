import httpGet from "../http_get.js"
let detail_usera = JSON.parse(httpGet("/user_api/detail_usera"))


for (let k of Object.keys(detail_usera)) {
    if (k == "acga_jmeno") {
        document.getElementById(k).value = detail_usera[k]
    } else {
        document.getElementById(k).innerText = detail_usera[k]
    }
}
