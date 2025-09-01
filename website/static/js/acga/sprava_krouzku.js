import http_get from "../http_get.js"

let data = JSON.parse(http_get("/acga_api/seznam_krouzku"));

for (let krouzek of data.krouzky) {
    let row = document.createElement("tr");
    row.innerHTML = `
        <td>${krouzek.name}</td>
        <td>${krouzek.pocet_lidi}</td>
        <td><a class="link" href="/acga/detail_krouzku/${krouzek.id}">Detail</a></td>
    `;
    document.querySelector("table tbody").appendChild(row);
}


let delete_button = document.getElementById("delete_krouzky");
delete_button.addEventListener("click", function(event) {
    if (confirm("Opravdu chcete smazat všechny kroužky?")) {
        event.preventDefault();
        document.getElementById("delete_all_form").submit();
    }
});


let zkopirovat_button = document.getElementById("export_button");
zkopirovat_button.addEventListener("click", function() {
    navigator.clipboard.writeText(data.table_data)
    zkopirovat_button.innerText = "Zkopírováno!";
});
