let input_button = document.getElementById("input_button");
let input = document.getElementById("input");
let napoveda_buttons = document.getElementsByClassName("napoveda_button");

let dostupne_kody = ["okurka", "mrkev", "pravidla", "cuketa", "jahoda"]


input_button.addEventListener("click", function() {
    for (let kod of dostupne_kody) {
        document.getElementById(kod).hidden = true;
    }
    let input_value = input.value;
    if (dostupne_kody.includes(input_value)) {
        document.getElementById(input_value).hidden = false;
    } else {
        input.value = "";
        alert("Takový kód stanoviště neexistuje.");
    }
})

for (let button of napoveda_buttons) {
    button.addEventListener("click", function() {
        document.getElementById(button.id + "_div").hidden = false;
    })
}