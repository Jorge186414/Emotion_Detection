async function uploadImage() {
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];

    if (!file) {
        alert('Por favor, selecciona una imagen antes de subirla.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.error}`);
            return;
        }

        const responseData = await response.json();
        if (result.images) {
            document.getElementById('originalImage').src = result.images[0] + '?t=' + new Date().getTime(); // Cache busting

            const processedImagesDiv = document.getElementById('processedImages');
            processedImagesDiv.innerHTML = ''

            result.images.slice(1).forEach(img => {
                const imgElement = document.createElement('img');
                imgElement.src = img + '?t=' + new Date().getTime(); 
                imgElement.style.maxWidth = '50%';
                processedImagesDiv.appendChild(imgElement);
            });
        }
        alert(`Imagen subida exitosamente: ${responseData.filepath}`);
    } catch (error) {
        console.error('Error al subir la imagen:', error);
        alert('Ocurrió un error al subir la imagen.');
    }
}
