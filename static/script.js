document.addEventListener('DOMContentLoaded', () => {
    const animalRadios = document.querySelectorAll('input[name="animal"]');
    const animalDisplay = document.getElementById('animal-display');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');

    animalRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            const selectedAnimal = e.target.value;
            if (selectedAnimal) {
                animalDisplay.innerHTML = `<img src="/static/images/${selectedAnimal}.jpg" alt="${selectedAnimal}">`;
            } else {
                animalDisplay.innerHTML = '';
            }
        });
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
