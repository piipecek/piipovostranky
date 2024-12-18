let start_game_button_1 = document.getElementById("start_game_button_1");
let start_game_button_2 = document.getElementById("start_game_button_2");
let create_game_button_1 = document.getElementById("create_game_button_1");
let rules_button = document.getElementById("rules_button");
let edit_game_button_1 = document.getElementById("edid_game_button_1");

let start_game_div = document.getElementById("start_game");
let rules_div = document.getElementById("rules");
let create_game_div = document.getElementById("create_game");
let edit_game_div = document.getElementById("edit_game");

// VIDITELNOST ROZCESTNÍKU

let start_game_visible = false;
let create_game_visible = false;
let edit_game_visible = false;
let rules_visible = false;

function update_visibility() {
    if (start_game_visible) {
        start_game_div.hidden = false;
        create_game_div.hidden = true;
        rules_div.hidden = true;
        edit_game_div.hidden = true;
    } else if (create_game_visible) {
        start_game_div.hidden = true;
        create_game_div.hidden = false;
        rules_div.hidden = true;
        edit_game_div.hidden = true;
    }
    else if (rules_visible) {
        start_game_div.hidden = true;
        create_game_div.hidden = true;
        rules_div.hidden = false;
        edit_game_div.hidden = true;
    } else if (edit_game_visible) {
        start_game_div.hidden = true;
        create_game_div.hidden = true;
        rules_div.hidden = true;
        edit_game_div.hidden = false;
    }
    else {
        start_game_div.hidden = true;
        create_game_div.hidden = true;
        rules_div.hidden = true;
        edit_game_div.hidden = true;
    }
}

start_game_button_1.addEventListener("click", () => {
    start_game_visible = !start_game_visible;
    create_game_visible = false;
    rules_visible = false;
    edit_game_visible = false;
    update_visibility();
})

create_game_button_1.addEventListener("click", () => {
    start_game_visible = false;
    create_game_visible = !create_game_visible;
    rules_visible = false;
    edit_game_visible = false;
    update_visibility();
})

rules_button.addEventListener("click", () => {
    start_game_visible = false;
    create_game_visible = false;
    rules_visible = !rules_visible;
    edit_game_visible = false;
    update_visibility();
})

edit_game_button_1.addEventListener("click", () => {
    start_game_visible = false;
    create_game_visible = false;
    rules_visible = false;
    edit_game_visible = !edit_game_visible;
    update_visibility();
})

// VYTVÁŘENÍ HRY