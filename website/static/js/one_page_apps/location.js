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
    if (!navigator.geolocation) {
        alert("Tento prohlížeč nepodporuje geolokaci.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const { latitude, longitude, accuracy } = pos.coords;
            alert(`Pošlu na server: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}. Přesnost: ${accuracy} m.`);
        },
        (err) => {
            console.error("Chyba při získávání polohy:", err);
            alert("Nepodařilo se zjistit přesnou polohu. Zkontroluj oprávnění nebo signál GPS.");
        },
        {
            enableHighAccuracy: true, // požaduj GPS (pokud je dostupné)
            timeout: 15000,           // čekej až 15 s na fix
            maximumAge: 0             // nepoužívej staré údaje
        }
    );
});