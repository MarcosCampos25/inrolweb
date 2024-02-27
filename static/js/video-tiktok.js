const videos = [
    "../static/video-tiktok-1.mp4",
    "../static/video-tiktok-2.mp4",
    "../static/video-tiktok-3.mp4"
];
let videoActual = 0;
const cacheVideos = {}; // Objeto para almacenar las URLs precargadas
 
const videoElement = document.getElementById('tiktok-video');
const svgMute = document.getElementById('svgMute');
const svgUnmute = document.getElementById('svgUnmute');
 
function precargarYReproducir(videoIndex) {
    if (videoIndex >= videos.length) {
      return;
    }
 
    if (cacheVideos[videos[videoIndex]]) {
        // Si el video ya está precargado, usarlo directamente
        videoElement.src = cacheVideos[videos[videoIndex]];
        videoElement.play();
    } else {
        // Si no está precargado, cargar y reproducir
        fetch(videos[videoIndex])
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                cacheVideos[videos[videoIndex]] = url; // Almacenar en caché
                videoElement.src = url;
                videoElement.play();
            })
            .catch(console.error);
    }
 
    // Preparar el próximo video para una transición suave
    let siguienteIndex = videoIndex + 1 < videos.length ? videoIndex + 1 : 0;
    precargarVideo(siguienteIndex); // Precargar el siguiente sin reproducir
}
 
function precargarVideo(videoIndex) {
    if (videoIndex >= videos.length || cacheVideos[videos[videoIndex]]) {
      return;
    }
 
    fetch(videos[videoIndex])
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            cacheVideos[videos[videoIndex]] = url; // Almacenar en caché
        })
        .catch(console.error);
}
 
videoElement.addEventListener('ended', () => {
    videoActual++;
    if (videoActual >= videos.length) {
        videoActual = 0;
    }
    precargarYReproducir(videoActual);
});
 
// Iniciar con el primer video
precargarYReproducir(videoActual);


function unMute() {
 // Toggle del estado mute

    // Cambiar la visibilidad de los SVGs basado en si el video está muteado
    if (videoElement.muted) {
        svgMute.style.display = "none";
        svgUnmute.style.display = "block";
    } else {
        svgMute.style.display = "block";
        svgUnmute.style.display = "none";
    }
    videoElement.muted = !videoElement.muted;
}



