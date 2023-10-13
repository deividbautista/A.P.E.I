// Apartado para definir las constantes que vamos a utilizar en el proceso.
//------------------------------------------------------------------------

// Definimos la constante inp que aacoje al objeto tipo input con el id "formFileSm" alojado en nueestro documento html
// para poder cargar los archivos y subirlos al servidor.
const inp = document.querySelector("#formFileSm");
// Definimos la constante dropArea, para el div con la clase "modal-content", esto para poder detectar el area donde arratra el archivo.
const dropArea = document.querySelector(".modal-content");

//---------------------------------------
// Definimos el evento que se realizara cuando pasemos por encima del area con nuestro archivo.
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    // La siguiente linea añade la clase activate que contiene los estilos del evento dragover.
    dropArea.classList.add("activate");
});

//---------------------------------------
// Definimos el evento que se realizara cuando quitemos del area nuestro archivo.
dropArea.addEventListener("dragleave", (e) => {
    e.preventDefault();
    // La siguiente linea retira la clase activate que contiene los estilos del evento dragover.
    dropArea.classList.remove("activate");
});

//---------------------------------------
// Definimos el evento a realizar cuando soltamos el archivo en el area permitida o especificada.
dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    // Transferimos el archivo capturado por el area permitida o especificada, al input designado
    // para realizar el envio de archivos.
    inp.files = e.dataTransfer.files;
    // La siguiente linea retira la clase activate que contiene los estilos del evento dragover.
    dropArea.classList.remove("activate");
});
