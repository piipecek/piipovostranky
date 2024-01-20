import httpGet from "../http_get.js"
let acga_jmeno = httpGet("/user_api/get_acga_jmeno")


let generovat_button = document.getElementById("generovat")
let pocet_kodu_input = document.getElementById("pocet_kodu")
document.getElementById("acga_jmeno").value = acga_jmeno


generovat_button.addEventListener("click", function() {
    let value = pocet_kodu_input.value
    if (!value) {
        alert("Nebylo zadáno platné číslo.")
    } else if (!acga_jmeno) {
        alert("Nemáte vyplněné jméno učitele.")
    } else {
        $.ajax({
        type: "POST",
        url: "/user_api/vytvorit_evaluace/" + String(value),
        contentType: false,
        processData: false,
        success: function(data) {
            console.log(data)
            }
        })
    }
})