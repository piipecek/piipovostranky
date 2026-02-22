import httpGet from "../http_get.js"
let deck_id = document.getElementById("deck_id").value
let data = JSON.parse(httpGet("/slovnik_api/quiz/" + deck_id))
import TableCreator from "../table_creator.js"


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
let form = document.getElementById("form")
let save_quiz_button = document.getElementById("save_quiz")
let result_input = document.getElementById("result_input")

confirm_button.addEventListener("click", handle_confirm)
skip_button.addEventListener("click", handle_skip)
end_button.addEventListener("click", handle_end)
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
    for (let term of data) {
        quiz_queue.push({
            id: term["id"],
            definition: term["definition"],
            translation: term["translation"],
        })
    }
}


function handle_confirm() {
    // ignore empty input
    if (value_input.value.trim() === "") {
        return
    }
    
    let input = value_input.value.trim()
    let translation = quiz_queue[index]["translation"].trim()

    // in case of other correctness settings, here would be the evaluator
    let correct = input == translation

    // take the value, create a quiz_answer and push it
    let answer_element = {
        id: quiz_queue[index]["id"],
        definition: quiz_queue[index]["definition"],
        translation: quiz_queue[index]["translation"],
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
        result_div.innerText = quiz_queue[index]["translation"]
        color_row.classList.add("wrong")
    }
    // if wrong, add a new entry to queue to practice the wrong term again
    if (!correct) {
        quiz_queue.push({
            id: quiz_queue[index]["id"],
            definition: quiz_queue[index]["definition"],
            translation: quiz_queue[index]["translation"],
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
        definition: quiz_queue[index]["definition"],
        translation: quiz_queue[index]["translation"],
    })
    // increment the index and draw current
    index++
    setTimeout(draw_current, 200)
}

function handle_end() {
    // end the quiz immediately and show the summary
    end_summary()
}

function draw_current() {
    // write index / len(queue) to progress_col
    progress_col.innerText = `${index + 1} / ${quiz_queue.length}`
    // clear the color classes by removing them
    color_row.classList.remove("correct", "wrong")
    // clear the result_div
    result_div.innerText = ""
    // write the current definition to key_div
    key_div.innerText = quiz_queue[index]["definition"]
}

function end_summary() {
    quiz_section.hidden = true
    summary_section.hidden = false

    let table = new TableCreator(document.getElementById("summary"), null, true)
    table.make_header(["#", "Definice", "Překlad", "Tvoje odpověď"])
    for (let i = 0; i < quiz_answers.length; i++) {
        let answer = quiz_answers[i]
        table.make_row([i + 1, answer["definition"], answer["translation"], answer["answer"]])
    }

    // write the quiz_answers to result_input as json
    result_input.value = JSON.stringify(quiz_answers)
}

initialize_queue()
draw_current()