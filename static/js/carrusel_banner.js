document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll('.carousel__image');
    const indicatorsContainer = document.querySelector('.carousel__indicators');
    let currentIndex = 0; 

    // Crear indicadores
    images.forEach((image, index) => {
      const indicator = document.createElement('div');
      indicator.classList.add('carousel__indicator');
      if (index === 0) indicator.classList.add('carousel__indicator--active');
      indicator.addEventListener('click', () => {
        moveToIndex(index);
      });
      indicatorsContainer.appendChild(indicator);
    });
  
    const indicators = document.querySelectorAll('.carousel__indicator');
  
    function updateIndicators(newIndex) {
      indicators.forEach((indicator, index) => {
        if (index === newIndex) {
          indicator.classList.add('carousel__indicator--active');
        } else {
          indicator.classList.remove('carousel__indicator--active');
        }
      });
    }
  
    function moveToIndex(index) {
      const width = images[0].getBoundingClientRect().width;
      const offset = width * index;
      document.querySelector('.carousel__images').style.transform = `translateX(-${offset}px)`;
      currentIndex = index;
      updateIndicators(index);
    }
  
    document.querySelector('.carousel__button--left').addEventListener('click', () => {
      const newIndex = (currentIndex - 1 + images.length) % images.length;
      moveToIndex(newIndex);
    });
  
    document.querySelector('.carousel__button--right').addEventListener('click', () => {
      const newIndex = (currentIndex + 1) % images.length;
      moveToIndex(newIndex);
    });
  
    // Autoplay
    setInterval(() => {
      const newIndex = (currentIndex + 1) % images.length;
      moveToIndex(newIndex);
    }, 5000); // Cambia las imágenes cada 3 segundos
  
    carousel.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      currentX = startX;
    }, { passive: true });
  
    carousel.addEventListener('touchmove', (e) => {
      currentX = e.touches[0].clientX;
    }, { passive: true });
  
    carousel.addEventListener('touchend', () => {
      const deltaX = startX - currentX;
      const threshold = 50; // Define qué tan lejos debe deslizarse para activar el cambio de imagen
      if (deltaX > threshold) {
        // Deslizar a la derecha
        const newIndex = (currentIndex + 1) % images.length;
        moveToIndex(newIndex);
      } else if (deltaX < -threshold) {
        // Deslizar a la izquierda
        const newIndex = (currentIndex - 1 + images.length) % images.length;
        moveToIndex(newIndex);
      }
    });


   
});
  