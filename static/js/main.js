function onSubmit(e) {
    e.preventDefault();
    document.querySelector('.msg').textContent = '';
    // document.querySelector('#file_download').style.display = "none";
    const file = document.querySelector('#video_file').files[0];
    let formData = new FormData();
    formData.append('video', file)

    generateSubtitleRequest(formData, file);
}

async function generateSubtitleRequest(formData, file) {
    try {
        showSpinner();
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            removeSpinner();
            throw new Error('That Video cannot be generated!')
        }
        const data = await response.json();
        const file_path = `static/output/${file['name']}`
        document.querySelector('#video_file').value = ""
        document.querySelector('#file_download').style.display = "block";
        
        document.querySelector('#video_play').innerHTML = `<source src=${file_path} type="video/mp4">`;
        document.querySelector('#video_play').style.display = "block";
        document.querySelector('#file_download').href = `/download/${file['name']}`
        // const imageUrl = data.data;
        // document.querySelector('#image').src = imageUrl;
        removeSpinner();
    } catch (error) {
        // removeSpinner();
        document.querySelector('.msg').textContent = error;
    }
}

function showSpinner() {
    document.querySelector('.spinner').classList.add('show');

}
function removeSpinner() {
    document.querySelector('.spinner').classList.remove('show');
    
}
document.querySelector('#file_download').style.display = 'none';
document.querySelector('#video_play').style.display = 'none';
document.querySelector('#video-form').addEventListener('submit', onSubmit);

