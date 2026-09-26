let button = document.getElementById("get_location");
let accurate_button = document.getElementById("get_accurate_location");

button.addEventListener("click", () => {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            const acc = pos.coords.accuracy;
            alert("Pošu na server: " + lat + ", " + lon +". Přesnost: " + acc + " metrů.");
        },
        (err) => {
            console.error("Error getting location:", err);
        }
    );
});

accurate_button.addEventListener("click", () => {
    let bestPosition = null;
    let finished = false;

    accurate_button.classList.add("loading");

    const finish = (pos) => {
        if (finished) return;
        finished = true;

        navigator.geolocation.clearWatch(watchId);
        clearTimeout(timeoutId);

        accurate_button.classList.remove("loading");

        const { latitude, longitude, accuracy } = pos.coords;

        alert(
            `Pošlu na server: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}. ` +
            `Přesnost: ${accuracy.toFixed(1)} m.`
        );
    };

    const watchId = navigator.geolocation.watchPosition(
        (pos) => {
            if (
                bestPosition === null ||
                pos.coords.accuracy < bestPosition.coords.accuracy
            ) {
                bestPosition = pos;
            }

            console.log(`Přesnost: ${pos.coords.accuracy.toFixed(1)} m`);
        },
        (err) => {
            console.error("Chyba při získávání polohy:", err);
        },
        {
            enableHighAccuracy: true,
            maximumAge: 0
        }
    );

    const timeoutId = setTimeout(() => {
        if (bestPosition) {
            finish(bestPosition);
        } else {
            navigator.geolocation.clearWatch(watchId);
            alert("Nepodařilo se zjistit polohu.");
        }
    }, 5000);
});