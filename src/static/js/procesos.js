// --------------------------------------------------------------------------------
// Definimos las constantes para obtener los objetos con lo que interactuaremos.
const userLabels = document.querySelectorAll(".NombreUsuario");
const labels = document.querySelectorAll('.NombreUsuario_2');
const toggleButtons = document.querySelectorAll('.desplegable-toggle');
const main_container = document.querySelector('.container4');
const mensajeEr = document.querySelector('.MensajeError')
var dropdowns = document.querySelectorAll('.dropdown');
var select = document.getElementById("SelectLevel");


// --------------------------------------------------------------------------------
// Agrega un evento click a cada label.
userLabels.forEach(label => {
  label.addEventListener('click', (event) => {
    // Prevenir que se cierre la lista.
    event.stopPropagation();
  });
});
// --------------------------------------------------------------------------------


// --------------------------------------------------------------------------------
// Función para obtener la fecha del dia de hoy y asignarla automaticamente en el campo de periodo.
window.onload = function () {
  var dateFields = document.querySelectorAll("#fecha");
  var today = new Date().toISOString().split("T")[0];

  dateFields.forEach(function (dateField) {
    dateField.value = today;
  });
};
// --------------------------------------------------------------------------------


// --------------------------------------------------------------------------------
// Agrega un evento de clic a cada botón
toggleButtons.forEach(function(button) {
  button.addEventListener('click', function(event) {
      event.preventDefault(); // Prevenir la acción predeterminada (puede evitar que la lista se abra/cierre)
      var dropdown = button.closest('.dropdown'); // Encuentra el elemento .dropdown más cercano
      dropdown.classList.toggle('active');
      event.stopPropagation(); // Evita que el clic llegue al documento
  });
});

// Agrega un controlador de eventos clic al documento
document.addEventListener('click', function(event) {
  dropdowns.forEach(function(dropdown) {
      if (!dropdown.contains(event.target)) {
          // Si el clic ocurrió fuera del menú desplegable, ciérralo
          dropdown.classList.remove('active');
      }
  });
});
// --------------------------------------------------------------------------------

// --------------------------------------------------------------------------------
// Evita que el formulario se envie si no se escoje un una opción del valida del input select.
document.getElementById("formularioActualizarP").addEventListener("submit", function(event) {
  if (select.value === "") {
    event.preventDefault(); // Evitar el envío del formulario
    alert("Por favor, elija una opción válida antes de enviar el formulario.");
  }
});




document.addEventListener("keyup", e => {
  if (e.target.matches("#buscador")) {
    if (e.key === "Escape") e.target.value = "";

    // Obtén el valor del campo de búsqueda
    const valorInput = e.target.value.toLowerCase();

    // Obtén todos los elementos con la clase "main-container"
    const elementos = document.querySelectorAll(".main-container");

    // Variable para rastrear si al menos un elemento coincide
    let coincidencia = false;

    elementos.forEach(palabra => {
      const tituloP = palabra.querySelector(".titleP");
      if (palabra.textContent.toLowerCase().includes(valorInput)) {
        // Si hay al menos una coincidencia, establecemos la variable coincidencia en true.
        palabra.classList.remove("filtro");
        coincidencia = true;
      } else {
        palabra.classList.add("filtro");
      }
    });

    if (!coincidencia && valorInput) {
      main_container.classList.add('filtro2');
      mensajeEr.classList.add('filtro3');

    } else {
      main_container.classList.remove('filtro2');
      mensajeEr.classList.remove('filtro3');
    }
  }
});















