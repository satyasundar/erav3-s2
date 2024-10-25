document.addEventListener('DOMContentLoaded', () => {
    const animalCheckboxes = document.querySelectorAll('input[name="animal"]');
    const generateImageBtn = document.getElementById('generate-image-btn');
    const animalDisplay = document.getElementById('animal-display');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');

    generateImageBtn.addEventListener('click', async () => {
        const selectedAnimals = Array.from(animalCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

        if (selectedAnimals.length > 0) {
            animalDisplay.innerHTML = '<p>Generating image...</p>';
            try {
                const response = await fetch('/generate-image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ animals: selectedAnimals }),
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const imageUrl = URL.createObjectURL(blob);
                    animalDisplay.innerHTML = `<img src="${imageUrl}" alt="${selectedAnimals.join(' and ')}">`;
                } else {
                    const errorData = await response.json();
                    console.error('Error details:', errorData);
                    animalDisplay.innerHTML = `<p>Error generating image: ${errorData.detail}</p>`;
                    if (errorData.api_response) {
                        animalDisplay.innerHTML += `<p>API Response: ${errorData.api_response}</p>`;
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                animalDisplay.innerHTML = `<p>Error generating image: ${error.message}</p>`;
            }
        } else {
            animalDisplay.innerHTML = '<p>Please select at least one animal.</p>';
        }
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    fileInfo.innerHTML = `
                        <p>File Name: ${data.filename}</p>
                        <p>File Size: ${data.size} bytes</p>
                        <p>File Type: ${data.content_type}</p>
                    `;
                } else {
                    fileInfo.innerHTML = '<p>Error uploading file</p>';
                }
            } catch (error) {
                console.error('Error:', error);
                fileInfo.innerHTML = '<p>Error uploading file</p>';
            }
        }
    });
});
