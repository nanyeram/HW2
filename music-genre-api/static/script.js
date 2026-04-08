document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    const resultSection = document.getElementById('result-section');
    const genreResult = document.getElementById('genre-result');
    const recommendationList = document.getElementById('recommendation-list');
    
    let selectedFile = null;

    // Drag and Drop Events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    // Click to upload
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            selectedFile = files[0];
            // Update UI to show selected file
            const h3 = dropZone.querySelector('h3');
            const p = dropZone.querySelector('p');
            h3.textContent = selectedFile.name;
            p.textContent = `${(selectedFile.size / (1024 * 1024)).toFixed(2)} MB`;
            
            // Enable button
            analyzeBtn.disabled = false;
            
            // Hide previous results
            resultSection.classList.add('hidden');
        }
    }

    // Analyze Button Click
    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI Loading State
        analyzeBtn.disabled = true;
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        resultSection.classList.add('hidden');

        // Prepare FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // Call FastAPI backend
            const response = await fetch('/api/v1/predict/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server returned ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            
            // Show result
            genreResult.textContent = data.predicted_genre.toUpperCase();
            
            // Render recommendations
            recommendationList.innerHTML = '';
            if (data.recommendations && data.recommendations.length > 0) {
                data.recommendations.forEach(song => {
                    const li = document.createElement('li');
                    li.textContent = song;
                    recommendationList.appendChild(li);
                });
            }

            resultSection.classList.remove('hidden');
            
        } catch (error) {
            alert(`분석 중 오류가 발생했습니다: ${error.message}`);
            console.error(error);
        } finally {
            // Restore UI
            analyzeBtn.disabled = false;
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
        }
    });
});
