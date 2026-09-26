let button = document.getElementById("get_location");
let accurate_button = document.getElementById("get_accurate_location");
let liveLocationSpan = document.getElementById("live_location");

let currentPosition = null;

// Proměnné pro přesné 5s měření
let measuring = false;
let bestPosition = null;


// JEDINÝ watcher polohy
navigator.geolocation.watchPosition(
    (pos) => {
        currentPosition = pos;

        liveLocationSpan.textContent =
            pos.coords.accuracy.toFixed(1) + " m";

        // Pokud právě probíhá 5s měření,
        // ukládej nejlepší polohu
        if (
            measuring &&
            (
                bestPosition === null ||
                pos.coords.accuracy < bestPosition.coords.accuracy
            )
        ) {
            bestPosition = pos;
        }
    },
    (err) => {
        console.error("Chyba při sledování polohy:", err);
        liveLocationSpan.textContent = "Chyba při získávání polohy";
        accurate_button.classList.remove("loading");
    },
    {
        enableHighAccuracy: true,
        maximumAge: 0
    }
);


// 1. tlačítko: okamžitě vezme aktuální polohu
button.addEventListener("click", () => {
    if (!currentPosition) {
        alert("Poloha ještě není k dispozici.");
        return;
    }

    const { latitude, longitude, accuracy } = currentPosition.coords;

    alert(
        `Pošlu na server: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}. ` +
        `Přesnost: ${accuracy.toFixed(1)} m.`
    );
});


// 2. tlačítko: 5 sekund hledá nejlepší polohu
accurate_button.addEventListener("click", () => {
    if (measuring) return;

    measuring = true;

    // Aktuální poloha je první kandidát
    bestPosition = currentPosition;

    accurate_button.classList.add("loading");

    setTimeout(() => {
        measuring = false;
        accurate_button.classList.remove("loading");

        if (!bestPosition) {
            alert("Nepodařilo se zjistit polohu.");
            return;
        }

        const { latitude, longitude, accuracy } = bestPosition.coords;

        alert(
            `Pošlu na server: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}. ` +
            `Přesnost: ${accuracy.toFixed(1)} m.`
        );

        bestPosition = null;

    }, 5000);
});