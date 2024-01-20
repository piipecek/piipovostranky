import http_get from "../http_get.js"

let ucitele = JSON.parse(http_get("/guest_api/ucitele_na_evaluaci"))
console.log(ucitele)
