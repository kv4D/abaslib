document.addEventListener('DOMContentLoaded', function() {
    const coverInput = document.querySelector('input[type="file"]');
    const previewContainer = document.getElementById('cover_preview');
    const previewImage = document.getElementById('cover');
    
    coverInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
            }
            
            reader.readAsDataURL(file);
        } else {
            previewImage.src = '{% get_media_prefix %}default_cover.jpg';
            previewContainer.style.display = 'none';
        }
    });
});