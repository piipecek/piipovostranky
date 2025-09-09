import http_get from "../http_get.js"

let id = document.getElementById("id").value
let data = JSON.parse(http_get("/acga_api/detail_krouzku/" + parseInt(id)))

document.getElementById("title_name").innerText = data.name
document.getElementById("nazev_krouzku").value = data.name
document.getElementById("popis_krouzku").value = data.description

for (let student of data.students) {
    let row = document.createElement("tr");
    row.innerHTML = `
        <td>${student.cislo}</td>
        <td>${student.full_name}</td>
        <td>${student.class}</td>
        <td>${student.email}</td>
        <td>${student.timestamp}</td>
        <td><button class="btn btn-danger" name="delete" value="${student.email}">Smazat</button></td>
    `;
    document.querySelector("tbody").appendChild(row);
}

let delete_all_button = document.getElementById("delete_all");
delete_all_button.addEventListener("click", function(event) {
    if (confirm("Opravdu chcete smazat všechny studenty?")) {
        event.preventDefault();
        document.getElementById("delete_identifier").value = "all";
        document.getElementById("delete_all_form").submit();
    }
});

let delete_krouzek_button = document.getElementById("delete_krouzek");
delete_krouzek_button.addEventListener("click", function(event) {
    if (confirm("Opravdu chcete smazat tento kroužek?")) {
        event.preventDefault();
        document.getElementById("delete_identifier").value = "krouzek";
        document.getElementById("delete_all_form").submit();
    }
});

let zkopirovat_button = document.getElementById("export_button");
zkopirovat_button.addEventListener("click", function() {
    navigator.clipboard.writeText(data.table_data)
    zkopirovat_button.innerText = "Zkopírováno!";
});