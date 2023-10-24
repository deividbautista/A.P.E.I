
const bell = document.querySelector(".button-bell")
const notifications = document.querySelector(".notifications")

bell.addEventListener('click', () => {
    console.log("wenas")

    if (notifications.classList.contains("Nfiltro")) {
        notifications.classList.remove("Nfiltro");
    } else {
        notifications.classList.add("Nfiltro");
    }
});

document.addEventListener('click', (event) => {
    console.log("wenas")
    if (!notifications.contains(event.target) && !bell.contains(event.target)) {
        notifications.classList.add("Nfiltro");
    }
});

const socket = io();

        socket.on('notificacion', function(data) {
            const notificacionDiv = document.getElementById('notificacion');
            notificacionDiv.innerHTML = data.mensaje;
        });