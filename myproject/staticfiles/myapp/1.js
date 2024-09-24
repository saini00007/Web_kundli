// Show loading overlay
document.getElementById("loadingOverlay").style.visibility = "visible";

// Hide loading overlay when the page has fully loaded
window.addEventListener("load", function() {
    document.getElementById("loadingOverlay").style.visibility = "hidden";
});
