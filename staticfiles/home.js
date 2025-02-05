document.addEventListener("DOMContentLoaded", function () {
    const postModal = document.getElementById("postModal");
    const openPostModal = document.getElementById("openPostModal");
    const closePostModal = document.querySelector(".modal .close");

    // Open modal with smooth animation
    openPostModal.addEventListener("click", (e) => {
        e.preventDefault();
        postModal.style.display = "block";
    });

    // Close modal
    closePostModal.addEventListener("click", () => {
        postModal.style.display = "none";
    });

    // Close modal when clicking outside
    window.addEventListener("click", (event) => {
        if (event.target === postModal) {
            postModal.style.display = "none";
        }
    });

    // Handle form submission (AJAX)
    document.getElementById("postForm").addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(document.getElementById("postForm"));
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        try {
            const response = await fetch("/posts/new/", {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
                body: formData
            });

            if (response.ok) {
                alert("Post Created Successfully!");
                window.location.reload();
            } else {
                alert("Error creating post.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while creating the post.");
        }

        postModal.style.display = "none";
    });
});