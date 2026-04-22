 document.addEventListener("DOMContentLoaded", function(){

/* =====================================================
MENÚ HAMBURGUESA
===================================================== */

const menuToggle = document.getElementById("menu-toggle");
const navMenu = document.getElementById("nav");

if(menuToggle && navMenu){

  menuToggle.addEventListener("click", function(){
    navMenu.classList.toggle("active");
    menuToggle.classList.toggle("active");
    document.body.classList.toggle("menu-open");
  });

  const navLinks = document.querySelectorAll(".nav a");

  navLinks.forEach(function(link){
    link.addEventListener("click", function(){
      navMenu.classList.remove("active");
      menuToggle.classList.remove("active");
      document.body.classList.remove("menu-open");
    });
  });

  window.addEventListener("resize", () => {
    if(window.innerWidth > 768){
      navMenu.classList.remove("active");
      menuToggle.classList.remove("active");
      document.body.classList.remove("menu-open");
    }
  });

}


/* =====================================================
ANIMACIÓN SCROLL
===================================================== */

const elements = document.querySelectorAll(".fade-up");

if(elements.length > 0){

  function showOnScroll(){
    const trigger = window.innerHeight * 0.85;

    elements.forEach(el => {
      const top = el.getBoundingClientRect().top;

      if(top < trigger){
        el.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", showOnScroll);
  showOnScroll();
}


/* =====================================================
CONTADOR ANIMADO
===================================================== */

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

  const target = +counter.dataset.target;
  let count = 0;

  const update = () => {
    const increment = target / 60;

    if(count < target){
      count += increment;
      counter.innerText = Math.floor(count);
      requestAnimationFrame(update);
    } else {
      counter.innerText = target;
    }
  };

  update();
});


/* =====================================================
FILTRO PROYECTOS
===================================================== */

const botones = document.querySelectorAll(".filtro-btn");
const proyectos = document.querySelectorAll(".proyecto-card");

botones.forEach(boton => {
  boton.addEventListener("click", () => {

    const filtro = boton.getAttribute("data-filter");

    botones.forEach(b => b.classList.remove("active"));
    boton.classList.add("active");

    if(filtro === "all"){
      proyectos.forEach(p => p.style.display = "block");
    } else {
      proyectos.forEach(p => {
        p.style.display = p.classList.contains(filtro) ? "block" : "none";
      });
    }

  });
});


/* =====================================================
CARRUSEL PROYECTOS
===================================================== */

const slider = document.querySelector(".proyectos-grid");
const btnPrev = document.querySelector(".slider-btn.prev");
const btnNext = document.querySelector(".slider-btn.next");

if(slider && btnPrev && btnNext){

  const scrollAmount = 300;

  btnNext.addEventListener("click", () => {
    slider.scrollBy({ left: scrollAmount, behavior: "smooth" });
  });

  btnPrev.addEventListener("click", () => {
    slider.scrollBy({ left: -scrollAmount, behavior: "smooth" });
  });

}


/* =====================================================
CARD ACTIVA
===================================================== */

const cards = document.querySelectorAll(".proyecto-card");

function updateActiveCard(){
  const center = window.innerWidth / 2;

  cards.forEach(card => {
    const rect = card.getBoundingClientRect();
    const cardCenter = rect.left + rect.width / 2;

    if(Math.abs(center - cardCenter) < 150){
      card.classList.add("active");
    } else {
      card.classList.remove("active");
    }
  });
}

if(slider){
  slider.addEventListener("scroll", updateActiveCard);
  window.addEventListener("load", updateActiveCard);
}









const form = document.getElementById("form-contacto");
const btn = document.getElementById("btn-enviar");

if (form && btn) {

  const loader = btn.querySelector(".loader");
  const text = btn.querySelector("span");
  const message = document.getElementById("form-message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (loader) loader.style.display = "block";
    if (text) text.style.opacity = "0.5";

    if (message) {
      message.style.color = "#00ff88";
      message.textContent = "Enviando solicitud...";
    }

    const data = {
      nombre: form.nombre.value,
      email: form.email.value,
      telefono: form.telefono.value,
      mensaje: form.mensaje.value
    };

    try {
      const res = await fetch("https://komp.onrender.com/contacto", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (result.success) {
        message.style.color = "#00ff88";
        message.textContent = "Solicitud enviada correctamente ✔";
        form.reset();
      } else {
        message.style.color = "red";
        message.textContent = "Error al enviar";
      }

    } catch (error) {
      console.error(error);
      message.style.color = "red";
      message.textContent = "No se pudo conectar con el servidor";
    }

    if (loader) loader.style.display = "none";
    if (text) text.style.opacity = "1";

  });

}