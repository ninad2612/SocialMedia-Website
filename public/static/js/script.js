document.addEventListener('DOMContentLoaded', function () {
    // Follow Button Functionality
    const followBtn = document.getElementById('follow-btn');

    if (followBtn) {
        followBtn.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');
            const isFollowing = this.textContent.trim() === 'Following';

            fetch(`/follow/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'  // Django CSRF token for security
                },
                body: JSON.stringify({ 'action': isFollowing ? 'unfollow' : 'follow' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    followBtn.textContent = isFollowing ? 'Follow' : 'Following';
                } else {
                    alert(data.error || 'An error occurred.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Image and Video Preview Functionality
    const imageInput = document.getElementById('content_image');
    const videoInput = document.getElementById('content_video');
    const imagePreview = document.getElementById('image-preview');
    const videoPreview = document.getElementById('video-preview');

    // Image Preview
    if (imageInput) {
        imageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                    videoPreview.style.display = 'none'; // Hide video preview
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Video Preview
    if (videoInput) {
        videoInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file && file.type.startsWith('video/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    videoPreview.src = e.target.result;
                    videoPreview.style.display = 'block';
                    imagePreview.style.display = 'none'; // Hide image preview
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
