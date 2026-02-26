import httpGet from "../http_get.js"
let deck_id = document.getElementById("deck_id").value
let data = JSON.parse(httpGet("/slovnik_api/quiz/" + deck_id))
import TableCreator from "../table_creator.js"

// 1: front -> back, 2: back -> front
let quiz_type = document.getElementById("quiz_type").value
let number_of_terms = document.getElementById("number_of_terms").value

let start_button = document.getElementById("start_quiz")
let confirm_button = document.getElementById("confirm_button")
let skip_button = document.getElementById("skip_button")
let end_button = document.getElementById("end_button")
let key_div = document.getElementById("key")
let value_input = document.getElementById("value")
let result_div = document.getElementById("result")
let color_row = document.getElementById("color_row")
let progress_col = document.getElementById("progress")

let quiz_section = document.getElementById("quiz_section")
let summary_section = document.getElementById("summary_section")
let overview_section = document.getElementById("overview_section")
let form = document.getElementById("form")
let save_quiz_button = document.getElementById("save_quiz")
let result_input = document.getElementById("result_input")

confirm_button.addEventListener("click", handle_confirm)
skip_button.addEventListener("click", handle_skip)
end_button.addEventListener("click", handle_end)
start_button.addEventListener("click", handle_start)
value_input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault()
        handle_confirm()
    }
})
save_quiz_button.addEventListener("click", function() {
    form.submit()
})

let quiz_queue = []
let index = 0
let quiz_answers = []


function initialize_queue() {
    // randomly sample number_of_terms from data
    if (number_of_terms != "0") { // 0 means all
        data = data.sort(() => Math.random() - 0.5).slice(0, number_of_terms)
    }

    for (let term of data) {
        quiz_queue.push({
            id: term["id"],
            front: term["front"],
            back: term["back"],
        })
    }
}


function handle_confirm() {
    // ignore empty input
    if (value_input.value.trim() === "") {
        return
    }
    
    let input = value_input.value.trim()
    let back = quiz_queue[index]["back"].trim()
    let front = quiz_queue[index]["front"].trim()

    // in case of other correctness settings, here would be the evaluator
    let correct = false
    if (quiz_type == 1) {
        correct = input == back
    } else if (quiz_type == 2) {
        correct = input == front
    }

    // take the value, create a quiz_answer and push it
    let answer_element = {
        id: quiz_queue[index]["id"],
        front: quiz_queue[index]["front"],
        back: quiz_queue[index]["back"],
        answer: input,
        correct: correct,
    }
    quiz_answers.push(answer_element)

    // clear input value
    value_input.value = ""

    // if correct, write "správně" to result_div, if not, write the answer
    // color the color_row green or red with two different classes and timeouts
    if (correct) {
        result_div.innerText = "Správně!"
        color_row.classList.add("correct")
    } else {
        result_div.innerText = quiz_type == 1 ? back : front
        color_row.classList.add("wrong")
    }
    // if wrong, add a new entry to queue to practice the wrong term again
    if (!correct) {
        quiz_queue.push({
            id: quiz_queue[index]["id"],
            front: quiz_queue[index]["front"],
            back: quiz_queue[index]["back"],
        })
    }
    // increment the index
    index++
    // draw current or end suummary if the queue is done
    if (!correct) {
        setTimeout(draw_current, 2000)
    } else {
        setTimeout(() => {
            if (index < quiz_queue.length) {
                draw_current()
            } else {
                end_summary()
            }
        }, 500)
    }
}

function handle_skip() {
    // add the current term to the end of the queue
    quiz_queue.push({
        id: quiz_queue[index]["id"],
        front: quiz_queue[index]["front"],
        back: quiz_queue[index]["back"],
    })
    // draw the current answer as wrong and show the correct answer in result_div
    // do not create a new answer element, just show the correct answer
    let back = quiz_queue[index]["back"].trim()
    let front = quiz_queue[index]["front"].trim()
    result_div.innerText = quiz_type == 1 ? back : front
    color_row.classList.add("skip")

    // increment the index and draw current
    index++
    setTimeout(draw_current, 2000)
}

function handle_end() {
    // end the quiz immediately and show the summary
    end_summary()
}

function draw_current() {
    // write index / len(queue) to progress_col
    progress_col.innerText = `${index + 1} / ${quiz_queue.length}`
    // clear the color classes by removing them
    color_row.classList.remove("correct", "wrong", "skip")
    // clear the result_div
    result_div.innerText = ""
    // write the current front to key_div
    if (quiz_type == 1) {
        key_div.innerText = quiz_queue[index]["front"]
    } else if (quiz_type == 2) {
        key_div.innerText = quiz_queue[index]["back"]
    }
}

function end_summary() {
    quiz_section.hidden = true
    summary_section.hidden = false

    let table = new TableCreator(document.getElementById("summary"), null, true)
    table.make_header(["#", "Pojem", "Vysvětlení", "Tvoje odpověď"])
    for (let i = 0; i < quiz_answers.length; i++) {
        let answer = quiz_answers[i]
        table.make_row([i + 1, answer["front"], answer["back"], answer["answer"]])
    }

    // write the quiz_answers to result_input as json
    result_input.value = JSON.stringify(quiz_answers)
}

function draw_overview() {
    quiz_section.hidden = true
    summary_section.hidden = true

    let table = new TableCreator(document.getElementById("overview"), null, true)
    table.make_header(["#", "Pojem", "Vysvětlení"])
    for (let i = 0; i < quiz_queue.length; i++) {
        let term = quiz_queue[i]
        table.make_row([i + 1, term["front"], term["back"]])
    }
}

function handle_start() {
    overview_section.hidden = true
    quiz_section.hidden = false
    // shuffle the quiz_queue
    quiz_queue = quiz_queue.sort(() => Math.random() - 0.5)
    draw_current()
}

initialize_queue()
draw_overview()