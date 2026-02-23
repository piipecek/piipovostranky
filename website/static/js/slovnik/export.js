import httpGet from "../http_get.js"

let decks = JSON.parse(httpGet("/slovnik_api/decks_select"));
let export_deck_select = document.getElementById("export_deck_select");
let pdf_deck_select = document.getElementById("pdf_deck_select");

decks.forEach(deck => {
    let option = document.createElement("option");
    option.value = deck.id;
    option.textContent = deck.name;
    export_deck_select.appendChild(option);
    pdf_deck_select.appendChild(option.cloneNode(true));
});

document.getElementById("export_all").addEventListener("click", async () => {
    const res = await fetch("/slovnik_api/export_all", { method: "GET" });
    if (!res.ok) throw new Error("Export failed: " + res.status);

    const blob = await res.blob(); // IMPORTANT: keep it binary
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "slovnik_export.xlsx";
    document.body.appendChild(a);
    a.click();
    a.remove();

    URL.revokeObjectURL(url);
});

document.getElementById("export_deck").addEventListener("click", () => {
    const deckId = export_deck_select.value;
    if (!deckId) {
        alert("Please select a deck to export.");
        return;
    }

    window.location.href = `/slovnik_api/export_deck/${deckId}`;
});