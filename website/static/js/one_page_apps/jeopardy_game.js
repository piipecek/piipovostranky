let start_game_button_2 = document.getElementById("start_game_button_2");
let game_input = document.getElementById("file_start");
let teams_input = document.getElementById("teams_input");

let rozcestnik_div = document.getElementById("rozcestnik");
let game_div = document.getElementById("game");
let categories_tr = document.getElementById("categories_tr")
let tbody = document.getElementById("game_table")
let recent_field = document.getElementById("posledni_pole")
let teams_row = document.getElementById("teams_row")
let click_space_hint = document.getElementById("click_space_hint")

let modal = document.getElementById("mymodal");
let modal_content = document.getElementById("mymodal_content");
let odpoved = document.getElementById("odpoved");

let teams = []
let questions = []
let modal_visible = false;
let modal_state = 1;
let recent_id = null;
let recent_difficulty = 0;
let recent_category = "";

start_game_button_2.addEventListener("click", () => {
    let teams_value = teams_input.value
    let file = game_input.files[0];
    if (!file || teams_value === "") {
        alert("Vyplňte všechny údaje")
        return
    } else {
        let team_names = teams_value.replace(" ", "").split(",");
        for (let team_name of team_names) {
            teams.push({
                name: team_name,
                score: 0
            })
        }
        let reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => {
            let json = reader.result;
            questions = JSON.parse(json);
            for (let i=0; i<questions.length; i++) {
                questions[i].id = i
            }
            create_game();
        }
    }
})


function create_game() {
    rozcestnik_div.hidden = true;
    game_div.hidden = false;

    let categories = []
    let difficulties = []
    for (let question of questions) {
        if (!categories.includes(question.category)) {
            categories.push(question.category)
        }
        if (!difficulties.includes(question.difficulty)) {
            difficulties.push(question.difficulty)
        }
    }
    // tymy
    for (let team of teams) {
        let colDiv = document.createElement("div");
        colDiv.classList.add("col", "text-center", "d-flex", "flex-column");

        let teamP = document.createElement("p");
        teamP.classList.add("team");
        teamP.innerText = team.name;
        colDiv.appendChild(teamP);

        let scoreP = document.createElement("p");
        scoreP.classList.add("score");
        scoreP.innerText = team.score;
        colDiv.appendChild(scoreP);

        let buttonDiv = document.createElement("div");

        let plusButton = document.createElement("button");
        plusButton.classList.add("btn", "custom-button", "plus-button", "mx-1");
        plusButton.innerText = "+";
        plusButton.addEventListener("click", () => {
            team.score += recent_difficulty;
            scoreP.innerText = team.score;
        });
        buttonDiv.appendChild(plusButton);

        let minusButton = document.createElement("button");
        minusButton.classList.add("btn", "custom-button", "minus-button", "mx-1");
        minusButton.innerText = "-";
        minusButton.addEventListener("click", () => {
            team.score -= recent_difficulty;
            scoreP.innerText = team.score;
        });
        buttonDiv.appendChild(minusButton);

        colDiv.appendChild(buttonDiv);
        teams_row.appendChild(colDiv);
    }

    // kategorie
    for (let category of categories) {
        let th = document.createElement("th")
        th.innerText = category
        categories_tr.appendChild(th)
    }
    // otázky
    for (let difficulty of difficulties) {
        let tr = document.createElement("tr")
        tbody.appendChild(tr)
        for (let category of categories) {
            let question = questions.find((question) => question.category === category && question.difficulty === difficulty)
            let td = document.createElement("td")
            td.innerHTML = difficulty
            td.classList.add("clickable")
            td.id = "question_" + question.id
            tr.appendChild(td)
            td.addEventListener("click", () => {
                show_modal(question.category, question.difficulty, question.question, question.answer, question.id);
            })
        }
    }
}

function show_modal(category, difficulty, question, answer, id) {
    document.getElementById("modal_cat").innerText = category
    document.getElementById("modal_diff").innerText = difficulty
    document.getElementById("otazka").innerText = question
    odpoved.innerText = answer
    modal_visible = true
    modal_state = 1
    modal.hidden = false
    recent_id = id
}

function hide_modal() {
    modal.hidden = true
    modal_visible = false
    odpoved.hidden = true
    click_space_hint.innerText = "odpověď zobrazte mezerníkem nebo kliknutím"
}

function hide_answered_modal() {
    let td = document.getElementById("question_" + recent_id)
    td.classList.remove("clickable")
    td.classList.add("answered")
    let qustion = questions.find((question) => question.id === recent_id)
    recent_difficulty = qustion.difficulty
    recent_category = qustion.category
    recent_field.innerText = recent_category + " - " + recent_difficulty
    hide_modal()

}

modal.addEventListener("click", (event) => {
    if (event.target === modal) {
        hide_modal();
    }
});

modal_content.addEventListener("click", () => {
    if (modal_state === 1) {
        ukazat_odpoved();
    } else {
        hide_answered_modal();
    }
});

function ukazat_odpoved() {
    odpoved.hidden = false;
    click_space_hint.innerText = "otázku zavřete mezerníkem nebo kliknutím"
    modal_state = 2;
}

document.addEventListener("keydown", (event) => {
    if (modal_visible) {
        event.preventDefault();
        if (event.key === "Escape") {
            hide_modal();
        } else if (event.key === " " && modal_state === 1) {
            ukazat_odpoved();
        } else if (event.key === " " && modal_state === 2) {
            hide_answered_modal();
        }
    }
});