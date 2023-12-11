let slides = document.getElementsByClassName('slide');
let slideIndex = 0;

showSlides();

function showSlides() {
 for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = 'none';
 }
 slideIndex++;
 if (slideIndex > slides.length) {
    slideIndex = 1;
  }
 slides[slideIndex - 1].style.display = 'block';
 setTimeout(showSlides, 2000); // Cambiar la imagen cada 2 segundos
}