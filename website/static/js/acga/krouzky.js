import http_get from "../http_get.js"

let data = JSON.parse(http_get("/acga_api/student_krouzky"));

let krouzky_div = document.getElementById("krouzky");

for (let krouzek of data) {

    krouzky_div.appendChild(document.createElement("hr"));

    let div = document.createElement("div");
    div.classList.add("form-check", "d-flex", "align-items-center", "w-100");

    let input = document.createElement("input");
    input.classList.add("form-check-input", "me-4");
    input.type = "checkbox";
    input.name = "krouzky";
    input.value = krouzek.id;
    input.id = `krouzek_${krouzek.id}`;
    if (krouzek.enrolled) {
        input.checked = true;
    }

    let label = document.createElement("label");
    label.classList.add("form-check-label", "w-100");
    label.htmlFor = `krouzek_${krouzek.id}`;
    

    let name_p = document.createElement("p");
    name_p.classList.add("m-0", "fw-bold");
    name_p.innerText = krouzek.name;
    label.appendChild(name_p);

    let description_small = document.createElement("small");
    description_small.innerText = krouzek.description;
    label.appendChild(description_small);

    div.appendChild(input);
    div.appendChild(label);
    krouzky_div.appendChild(div);

}