// --------------------------------------------------------------------------------
// Definimos las constantes para obtener los objetos con lo que interactuaremos.
const userLabels = document.querySelectorAll(".NombreUsuario");
const labels = document.querySelectorAll('.NombreUsuario_2');
const toggleButtons = document.querySelectorAll('.desplegable-toggle');


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
// Función para obtener la fecha del dia de hoy y asignarla automaticament en el campo de periodo.
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
// toggleButtons.forEach(function(button) {
//     button.addEventListener('click', function(event) {
//         event.preventDefault(); // Prevenir la acción predeterminada (puede evitar que la lista se abra/cierre)
//         var dropdown = button.closest('.dropdown'); // Encuentra el elemento .dropdown más cercano
//         dropdown.classList.toggle('active');
//     });
// });

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
  var dropdowns = document.querySelectorAll('.dropdown');
  dropdowns.forEach(function(dropdown) {
      if (!dropdown.contains(event.target)) {
          // Si el clic ocurrió fuera del menú desplegable, ciérralo
          dropdown.classList.remove('active');
      }
  });
});

// --------------------------------------------------------------------------------
















