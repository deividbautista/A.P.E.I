// Definimos las constantes para obtener los objetos con lo que interactuaremos.
const boton = document.getElementById("boton");
const inputOculto = document.getElementById('inputOculto');
// --------------------------------------------------------------------------------


// --------------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
    // Obtiene todos los botones de clase "btnEliminarAsignacion".
    var buttons = document.querySelectorAll(".btnEliminarAsignacion");
  
    // Agrega un controlador de eventos a cada botón.
    buttons.forEach(function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault(); // Previene la acción por defecto del botón.
        // Obtiene los atributos "data".
        var idProceso = button.getAttribute("data-id");
        var idAsignado = button.getAttribute("data-id-asignado");
        // Crea un objeto de datos a enviar en la solicitud.
        var data = {
          id_proceso: idProceso,
          id_asignado: idAsignado
        };
        // Urilizamos la variable "Swal", la cual nos determinara los valores o caracteristicas 
        // del alert que estamos exponiendo al usuario.
        Swal.fire({
          title: '¿Estás seguro?',
          text: 'Esta acción eliminará la asignación de forma permanente.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar',
          // Lista con las caracteristicas de estilos personalizados.
          customClass: {
            // Apartado de customización de estilos en la alerta.
            confirmButton: 'custom-button-confirmation-1',
            cancelButton: 'custom-button-cancel-1',
            icon: 'custom-icon-class-1'
          }

        // Condicional para determinar si se confirma la eliminación o si se cancela el proceso.
        }).then((result) => {
          // En caso de ser afirmativo se realizaria el siguiente proceso.
          if (result.isConfirmed) {
            // Realizamos la petición al servidor para realizar la eliminación del usuario asignado.
          fetch("/deleteAsignacion", {
            method: "POST",
            headers: {
              "Content-Type": "application/json", // Establece el tipo de medio como JSON.
            },
            body: JSON.stringify(data)
          })
            .then(response => response.json())
            .then(data => {
              // Maneja la respuesta del servidor aquí.
              console.log(data);
              // Recarga la página o realiza otras acciones según sea necesario.
            })
            .catch(error => {
              // Maneja los errores aquí.
              console.error(error);
            });
            Swal.fire(
              'Eliminada',
              'La asignación ha sido eliminada.',
              'success'
            ).then(() => {
              // Refresca la ventana después de la confirmación.
              location.reload();

            });
          
          // En caso de ser negativo el proceso se dara por cancelado y se ilustrara el siguiente SweetAlert.
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
  
  
// --------------------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    var eliminarButtons = document.querySelectorAll('.eliminarProceso');
  
    eliminarButtons.forEach(function (eliminarButton) {
      eliminarButton.addEventListener('click', function (e) {
        e.preventDefault(); // Evita que el enlace se abra inmediatamente.
        
        // Variable con la información sobre la dirección para hacer peticiones a la api.
        var deleteUrl = this.getAttribute('data-url');
  
        // Muestra el SweetAlert al usuario.
        Swal.fire({
          title: '¿Estás seguro?',
          text: 'Esta acción eliminara el proceso de manera permanente.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar',
          // Lista con las caracteristicas de estilos personalizados.
          customClass: {
            confirmButton: 'custom-button-confirmation-1',
            cancelButton: 'custom-button-cancel-1',
            icon: 'custom-icon-class-1'
          }
        
        // Condicional para determinar si se confirma la eliminación o si se cancela el proceso.
        }).then(function (result) {
          // Si el usuario confirma, redirige a la dirección de la api para borrar el proceso.
          if (result.isConfirmed) {
            window.location.href = deleteUrl;
          // En caso de ser negativo el proceso se dara por cancelado y se ilustrara el siguiente SweetAlert.
          } else {
            Swal.fire({
              title: 'Cancelado',
              text: 'La eliminación de la asignación ha sido cancelada.',
              icon: 'info',
              // Lista con las caracteristicas de estilos personalizados.
              customClass: {
                // Apartado de customización de estilos en la alerta.
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

// --------------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
  var eliminarButtons = document.querySelectorAll('.eliminarReporte');

  eliminarButtons.forEach(function (eliminarButton) {
    eliminarButton.addEventListener('click', function (e) {
      e.preventDefault(); // Evita que el enlace se abra inmediatamente.
      
      // Variable con la información sobre la dirección para hacer peticiones a la api.
      var deleteUrl = this.getAttribute('data-url');

      // Muestra el SweetAlert al usuario.
      Swal.fire({
        title: '¿Estás seguro?',
        text: 'Esta acción eliminara el reporte del proceso de manera permanente.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        // Lista con las caracteristicas de estilos personalizados.
        customClass: {
          confirmButton: 'custom-button-confirmation-1',
          cancelButton: 'custom-button-cancel-1',
          icon: 'custom-icon-class-1'
        }
      
      // Condicional para determinar si se confirma la eliminación o si se cancela el proceso.
      }).then(function (result) {
        // Si el usuario confirma, redirige a la dirección de la api para borrar el proceso.
        if (result.isConfirmed) {
          window.location.href = deleteUrl;
        // En caso de ser negativo el proceso se dara por cancelado y se ilustrara el siguiente SweetAlert.
        } else {
          Swal.fire({
            title: 'Cancelado',
            text: 'La eliminación de la asignación ha sido cancelada.',
            icon: 'info',
            // Lista con las caracteristicas de estilos personalizados.
            customClass: {
              // Apartado de customización de estilos en la alerta.
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