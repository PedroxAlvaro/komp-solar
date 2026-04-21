document.addEventListener("DOMContentLoaded", function(){

const form = document.getElementById("form-contacto");

if(!form) return;

form.addEventListener("submit", function(e){
e.preventDefault();

const data = {
nombre: form.querySelector("input[type='text']").value,
email: form.querySelector("input[type='email']").value,
telefono: form.querySelector("input[type='tel']").value,
mensaje: form.querySelector("textarea").value
};

fetch("enviar.php", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify(data)
})
.then(res => res.text())
.then(respuesta => {
alert("Solicitud enviada correctamente ✅");
form.reset();
})
.catch(error => {
alert("Error al enviar ❌");
});

});

});