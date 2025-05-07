// toggle nav bar
const menu = document.querySelector(".navbar .nav-container");
const menuToggle = document.querySelector(".navbar i");
menuToggle.addEventListener("click", () => {
  menu.classList.toggle("visible");
  menuToggle.classList.toggle("fa-bars");
  menuToggle.classList.toggle("fa-xmark");
});