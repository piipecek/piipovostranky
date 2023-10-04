import httpGet from "./httpGet.js"

document.getElementById("logs").innerHTML = JSON.parse(httpGet("/admin_api/app_logs"))
