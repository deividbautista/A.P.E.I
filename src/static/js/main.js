
const bell = document.querySelector(".button-bell")
const notifications = document.querySelector(".notifications")

bell.addEventListener('click', () => {
    if (notifications.classList.contains("Nfiltro")) {
        notifications.classList.remove("Nfiltro");
    } else {
        notifications.classList.add("Nfiltro");
    }
});

document.addEventListener('click', (event) => {
    if (!notifications.contains(event.target) && !bell.contains(event.target)) {
        notifications.classList.add("Nfiltro");
    }
});

const socket = io();

        socket.on('notificacion', function(data) {
            const notificacionDiv = document.getElementById('notificacion');
            notificacionDiv.innerHTML = data.mensaje;
        });