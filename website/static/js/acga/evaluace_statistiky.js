let ukazat_button = document.getElementById("ukazat")

ukazat_button.addEventListener("click", function() {
    document.getElementById("form").hidden = true
    let form_data = new FormData()
    form_data.append("date", document.getElementById("date").value)
    $.ajax({
        type: "POST",
        url: "/acga_api/evaluace_statistiky_data",
        data: form_data,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log(data, "yayyyyy")
        }
    })
})

let today = new Date()
let ago = new Date()
ago.setMonth(today.getMonth() - 2)
let formattedDate = ago.toISOString().split('T')[0];
document.getElementById("date").value = formattedDate


