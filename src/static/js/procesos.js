// --------------------------------------------------------------------------------
// Definimos las constantes para obtener los objetos con lo que interactuaremos.
const userLabels = document.querySelectorAll(".NombreUsuario");
var labels = document.querySelectorAll('.NombreUsuario_2');


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


// Obtén todos los elementos con la clase "dropdown-toggle"
var toggleButtons = document.querySelectorAll('.desplegable-toggle');

// Agrega un evento de clic a cada botón
toggleButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir la acción predeterminada (puede evitar que la lista se abra/cierre)
        var dropdown = button.closest('.dropdown'); // Encuentra el elemento .dropdown más cercano
        dropdown.classList.toggle('active');
    });
});

document.addEventListener("keyup", e=>{
  if (e.target.matches("#buscador")){
    if(e.key === "Escape")e.target.value = ""

    document.querySelectorAll(".section-main-container").forEach(palabra =>{

      const tituloP = palabra.querySelector(".titleP");

      palabra.textContent.toLocaleLowerCase().includes(e.target.value.toLowerCase())
      ?palabra.classList.remove("filtro")
      :palabra.classList.add("filtro")

    })
  }

})















