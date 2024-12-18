let categories_input = document.getElementById("categories");
let difficulties_input = document.getElementById("difficulties");

let create_game_button_2 = document.getElementById("create_game_button_2");
let edit_game_button_2 = document.getElementById("edit_game_button_2");
let save_game_button = document.getElementById("save_game_button");
let back_home_button = document.getElementById("back_home_button");

let game_creator_div = document.getElementById("game_creator");
let rozcestnik_div = document.getElementById("rozcestnik");
let questions_div = document.getElementById("questions");

create_game_button_2.addEventListener("click", () => {
    if (categories_input.value === "" || difficulties_input.value === "") {
        alert("Vyplňte všechny pole");
        return;
    }
    let categories = categories_input.value.replace(" ", "").split(",");
    let difficulties = difficulties_input.value.replace(" ", "").split(",");
    let numbers_ok = true;
    difficulties = difficulties.map((difficulty) => {
        let parsed = parseInt(difficulty);
        if (isNaN(parsed)) {
            alert("Zadejte pouze čísla do obtížností");
            numbers_ok = false;
            return;
        }
        return parsed;
    });
    if (numbers_ok) {
        game_creator_div.hidden = false;
        rozcestnik_div.hidden = true;
        create_form(categories, difficulties);
    }
})

edit_game_button_2.addEventListener("click", () => {
    let file_input = document.getElementById("file_edit");
    let file = file_input.files[0];
    let reader = new FileReader();
    reader.readAsText(file);
    reader.onload = () => {
        let json = reader.result;
        let questions = JSON.parse(json);
        game_creator_div.hidden = false;
        rozcestnik_div.hidden = true;
        for (let question of questions) {
            let question_div = create_question(question.category, question.difficulty, question.question, question.answer);
            questions_div.appendChild(question_div)
        }
    }
})

function create_question(category, difficulty, question, answer) {
    let question_div = document.createElement("div");
    question_div.classList.add("question");
    question_div.innerHTML = `
        <h3>${category} - ${difficulty}</h3>
        <input hidden type="text" value="${category}">
        <input hidden type="text" value="${difficulty}">
        <input class="form-control my-1" type="text" value="${question}" placeholder="Otázka">
        <input class="form-control my-1" type="text" value="${answer}" placeholder="Odpověď">
    `;
    return question_div;
}

function create_form(categories, difficulties) {
    for (let category of categories) {
        for (let difficulty of difficulties) {
            let question = create_question(category, difficulty, "", "");
            questions_div.appendChild(question);
        }
    }
}

save_game_button.addEventListener("click", () => {
    // read each question div, add them all up to an array and download it as a json
    let questions = [];
    let question_divs = document.getElementsByClassName("question");
    for (let question_div of question_divs) {
        let category = question_div.children[1].value;
        let difficulty = question_div.children[2].value;
        let question = question_div.children[3].value;
        let answer = question_div.children[4].value;
        questions.push({
            category: category,
            difficulty: difficulty,
            question: question,
            answer: answer
        });
    }
    let json = JSON.stringify(questions);
    let blob = new Blob([json], {type: "application/json"});
    let url = URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.href = url;
    a.download = "game.json";
    a.click();
    URL.revokeObjectURL(url);
})

back_home_button.addEventListener("click", () => {
    location.reload();
})