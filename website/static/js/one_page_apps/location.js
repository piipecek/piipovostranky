let button = document.getElementById("get_location");

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