// Definimos las constantes para obtener los objetos con lo que interactuaremos.
const idlabel = document.querySelectorAll(".usuariosSeleccionados");
const boton = document.getElementById("boton");
const checkboxes = document.querySelectorAll(".usuariosSelect");
const inputOculto = document.getElementById('inputOculto');


// --------------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
    // Obtiene todos los botones de clase "btnEliminarAsignacion"
    var buttons = document.querySelectorAll(".btnEliminarAsignacion");
  
    // Agrega un controlador de eventos a cada botón
    buttons.forEach(function (button) {
      button.addEventListener("click", function (event) {
  
        event.preventDefault(); // Previene la acción por defecto del botón
        // Obtiene los atributos "data"
        var idProceso = button.getAttribute("data-id");
        var idAsignado = button.getAttribute("data-id-asignado");
  
        // Crea un objeto de datos a enviar en la solicitud
        var data = {
          id_proceso: idProceso,
          id_asignado: idAsignado
        };
  
        // Urilizamos la variable swal, la cual nos determinara los valores o caracteristicas 
        // del alert que estamos exponiendo al usuario
        Swal.fire({
          title: '¿Estás seguro?',
          text: 'Esta acción eliminará la asignación de forma permanente.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar',
          customClass: {
            // confirmButtonColor: '#900C3F',
            // cancelButtonColor: '#33415c',
            // confirmButtonText: 'Sí, eliminar',
            // cancelButtonText: 'Cancelar'
            confirmButton: 'custom-button-confirmation-1',
            cancelButton: 'custom-button-cancel-1',
            icon: 'custom-icon-class-1'
          }
        }).then((result) => {
          if (result.isConfirmed) {
            /// Aquí puedes agregar la lógica para eliminar al usuario
          fetch("/deleteAsignacion", {
            method: "POST",
            headers: {
              "Content-Type": "application/json" // Establece el tipo de medio como JSON
            },
            body: JSON.stringify(data)
          })
            .then(response => response.json())
            .then(data => {
              // Maneja la respuesta del servidor aquí
              console.log(data);
              // Recarga la página o realiza otras acciones según sea necesario
            })
            .catch(error => {
              // Maneja los errores aquí
              console.error(error);
            });
            Swal.fire(
              'Eliminada',
              'La asignación ha sido eliminada.',
              'success'
            ).then(() => {
              // Refresca la ventana después de la confirmación
              location.reload();
            });
            
          } else {
            Swal.fire({
              title: 'Cancelado',
              text: 'La eliminación de la asignación ha sido cancelada.',
              icon: 'info',
              customClass: {
                confirmButton: 'custom-button-confirmation-2',
                icon: 'custom-icon-class-2',
              }
            });
          }
        });
      });
    });
  });
  // --------------------------------------------------------------------------------
  
  
  // -----------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    var eliminarButtons = document.querySelectorAll('.eliminar');
  
    eliminarButtons.forEach(function (eliminarButton) {
      eliminarButton.addEventListener('click', function (e) {
        e.preventDefault(); // Evita que el enlace se abra inmediatamente
  
        var deleteUrl = this.getAttribute('data-url');
  
        // Muestra la alerta SweetAlert
        Swal.fire({
          // title: '¿Estás seguro?',
          // text: 'Esta acción no se puede deshacer',
          // icon: 'warning',
          // showCancelButton: true,
          // confirmButtonColor: '#3085d6',
          // cancelButtonColor: '#d33',
          // cancelButtonText: 'Cancelar',
          // confirmButtonText: 'Sí, borrarlo'
  
          title: '¿Estás seguro?',
          text: 'Esta acción eliminara el proceso de manera permanente.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar',
          customClass: {
            confirmButton: 'custom-button-confirmation-1',
            cancelButton: 'custom-button-cancel-1',
            icon: 'custom-icon-class-1'
          }
  
        }).then(function (result) {
          if (result.isConfirmed) {
            // Si el usuario confirma, redirige a la página de borrado
            window.location.href = deleteUrl;
          } else {
            Swal.fire({
              title: 'Cancelado',
              text: 'La eliminación de la asignación ha sido cancelada.',
              icon: 'info',
              customClass: {
                confirmButton: 'custom-button-confirmation-2',
                icon: 'custom-icon-class-2',
              }
            });
          }
        });
      });
    });
  });
  // --------------------------------------------------------------------------------