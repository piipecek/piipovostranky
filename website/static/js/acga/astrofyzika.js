import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"


let generovat_button = document.getElementById('generovat_button');

generovat_button.addEventListener('click', function() {
    let prijmeni = document.getElementById('prijmeni').value;
    let adress = "/acga_api/astrofyzika/" + prijmeni;
    let response = JSON.parse(httpGet(adress));
    createTable(response)
})

function calculate_result(data) {
    let r1 = [data[0], data[1]];
    let r2 = [data[2], data[3]];
    let v1 = [data[4], data[5]];
    let v2 = [-v1[0], -v1[1]];
    const m = data[6];

    const time_step = 0.05;
    const n_steps = 500;

    const positions_1 = [r1];
    const positions_2 = [r2];
    const velocities_1 = [v1];
    const velocities_2 = [v2];

    for (let n = 0; n < n_steps; n++) {
        const last_position_1 = positions_1[positions_1.length - 1];
        const last_position_2 = positions_2[positions_2.length - 1];
        const last_velocity_1 = velocities_1[velocities_1.length - 1];
        const last_velocity_2 = velocities_2[velocities_2.length - 1];
        const vector_12 = [
            last_position_2[0] - last_position_1[0],
            last_position_2[1] - last_position_1[1]
        ];
        const vector_21 = [-vector_12[0], -vector_12[1]];
        const dst = Math.sqrt(vector_12[0] ** 2 + vector_12[1] ** 2);
        const a = m / (dst ** 2);
        const a_1 = [a * vector_12[0] / dst, a * vector_12[1] / dst];
        const a_2 = [a * vector_21[0] / dst, a * vector_21[1] / dst];
        v1 = [
            last_velocity_1[0] + a_1[0] * time_step,
            last_velocity_1[1] + a_1[1] * time_step
        ];
        v2 = [
            last_velocity_2[0] + a_2[0] * time_step,
            last_velocity_2[1] + a_2[1] * time_step
        ];
        r1 = [
            last_position_1[0] + v1[0] * time_step,
            last_position_1[1] + v1[1] * time_step
        ];
        r2 = [
            last_position_2[0] + v2[0] * time_step,
            last_position_2[1] + v2[1] * time_step
        ];
        positions_1.push(r1);
        positions_2.push(r2);
        velocities_1.push(v1);
        velocities_2.push(v2);
    }

    const result = Math.round(
        positions_1.concat(positions_2).reduce((sum, r) => sum + r[0], 0)
    );

    return result;
}

function createTable(data) {

    let table = new TableCreator(document.getElementById("zadani"));
    table.make_header(["veličina", "hodnota"])
    table.make_row(["\\(x_1\\)", "\\(" + String(data[0]) + "\\)"])
    table.make_row(["\\(y_1\\)", "\\(" + String(data[1]) + "\\)"])
    table.make_row(["\\(x_2\\)", "\\(" + String(data[2]) + "\\)"])
    table.make_row(["\\(y_2\\)", "\\(" + String(data[3]) + "\\)"])
    table.make_row(["\\(v_{1x}\\)", "\\(" + String(data[4]) + "\\)"])
    table.make_row(["\\(v_{1y}\\)", "\\(" + String(data[5]) + "\\)"])
    table.make_row(["\\(m\\)", "\\(" + String(data[6]) + "\\)"])
    table.make_header(["výsledek", calculate_result(data)])
    MathJax.typeset()
}