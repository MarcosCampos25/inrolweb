const frases = [
  "Descubre el secreto de una belleza sin esfuerzo, todos los días",
  "Tu compañero esencial para brillar en cada momento.",
  "Belleza, organización y estilo, todo en uno.",
  "Transforma tu rutina de belleza en una experiencia de lujo.",
  "Donde la belleza y la practicidad se encuentran.",
  "Haz que cada día sea una oportunidad para resplandecer.",
  "El arte de la belleza organizada.",
  "Innovación y estilo para tu rutina de belleza.",
  "Porque cada detalle cuenta en tu camino hacia la belleza.",
  "Eleva tu experiencia de belleza al siguiente nivel."
  ];
  
  let indiceActual = 0;
  
  function mostrarFrase(frase, indice) {
    if (indice < frase.length) {
      document.getElementById('carrusel__frases').textContent += frase.charAt(indice);
      setTimeout(() => mostrarFrase(frase, indice + 1), 100); // Ajusta el tiempo para controlar la velocidad de "escritura"
    } else {
      setTimeout(cambiarFrase, 2000); // Espera 2 segundos antes de cambiar la frase
    }
  }
  
  function cambiarFrase() {
    const carousel = document.getElementById('carrusel__frases');
    carousel.style.opacity = 1; // Asegura que la opacidad esté al máximo para la nueva frase
    carousel.textContent = ''; // Limpia la frase actual
    mostrarFrase(frases[indiceActual], 0);
    indiceActual = (indiceActual + 1) % frases.length;
  }
  
  // Inicia el efecto de máquina de escribir inmediatamente al cargar
  cambiarFrase();
  // Si deseas tener un intervalo fijo que incluya la escritura y pausa, ajusta este método y su implementación.
  