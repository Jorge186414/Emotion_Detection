document.getElementById('upload-form').addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('image');

    if (fileInput.files.length === 0) {
        alert('No se cargó una imagen');
        return; // Detener ejecución
    }

    formData.append('image', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {

            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }
            // Mostrar imagen original
            document.getElementById('originalImage').src = data.images[0] + '?t=' + new Date().getTime();

            // Mostart la emocion
            var emotion = document.getElementById('emotion-result');
            emotion.textContent = data.emotion
            
            // Mostrar imágenes procesadas
            const processedImagesDiv = document.getElementById('processedImages');
            processedImagesDiv.innerHTML = '';

            data.images.slice(1).forEach(img => {
                const imgElement = document.createElement('img');
                imgElement.src = img + '?t=' + new Date().getTime();
                imgElement.style.width = '50%';
                processedImagesDiv.appendChild(imgElement);
            });

            alert(`Imagen subida exitosamente: ${data.message}`);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
