const fileInput = document.getElementById('fileInput');
const passwordInput = document.getElementById('passwordInput');
const uploadArea = document.getElementById('uploadArea');
const convertButton = document.getElementById('convertButton');
const loadingDiv = document.getElementById('loading');
const uploadedFileActions = document.getElementById('uploadedFileActions');
const fileNameElement = document.getElementById('fileName');
const fileSizeElement = document.getElementById('fileSize');
const fileDownloadLink = document.getElementById('fileDownloadLink');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    fileInput.files = files;
    updateFileName();
});

fileInput.addEventListener('change', updateFileName);

function updateFileName() {
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        uploadArea.querySelector('.upload-text').textContent = fileName;
        convertButton.disabled = false;
    } else {
        resetUploadArea();
    }
}

convertButton.addEventListener('click', async () => {
    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('password', passwordInput.value);

    loadingDiv.style.display = 'block';
    convertButton.disabled = true;

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showFileMetadata(data.metadata);
        } else {
            alert(data.error || 'An error occurred');
        }
    } catch {
        alert('An error occurred while uploading the file.');
    } finally {
        loadingDiv.style.display = 'none';
        convertButton.disabled = false;
    }
});

function showFileMetadata(metadata) {
    fileNameElement.textContent = metadata.filename;
    fileSizeElement.textContent = metadata.size;
    fileDownloadLink.href = metadata.download_url;

    uploadedFileActions.style.display = 'block';
}

function resetUploadArea() {
    uploadArea.querySelector('.upload-text').textContent = 'Drag and drop your DOCX file here';
    convertButton.disabled = true;
    uploadedFileActions.style.display = 'none';
}