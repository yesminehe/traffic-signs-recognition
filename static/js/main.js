// Import styles
import "../css/style.css";

// Theme switching functionality
document.addEventListener("DOMContentLoaded", () => {
  const themeSwitch = document.querySelector(".theme-switch");
  const themeIcon = themeSwitch.querySelector("i");

  // Check for saved theme preference
  const currentTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", currentTheme);
  updateThemeIcon(currentTheme);

  themeSwitch.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";

    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeIcon(newTheme);
  });

  function updateThemeIcon(theme) {
    themeIcon.className = theme === "light" ? "fas fa-moon" : "fas fa-sun";
  }

  // Drag and drop functionality
  const dropZone = document.querySelector(".drop-zone");
  const fileInput = document.querySelector("#fileInput");
  const previewImage = document.querySelector("#previewImage");
  const resultSection = document.querySelector("#resultSection");
  const loadingSpinner = document.querySelector("#loadingSpinner");
  const predictionResult = document.querySelector("#predictionResult");
  const confidenceBar = document.querySelector("#confidenceBar");
  const descriptionText = document.querySelector("#descriptionText");

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, highlight, false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, unhighlight, false);
  });

  function highlight() {
    dropZone.classList.add("highlight");
  }

  function unhighlight() {
    dropZone.classList.remove("highlight");
  }

  dropZone.addEventListener("drop", handleDrop, false);
  fileInput.addEventListener("change", handleFileSelect, false);

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = function (e) {
          previewImage.src = e.target.result;
          previewImage.style.display = "block";
          analyzeImage(file);
        };
        reader.readAsDataURL(file);
      } else {
        showError("Veuillez sélectionner une image valide.");
      }
    }
  }

  function analyzeImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    loadingSpinner.style.display = "block";
    resultSection.style.display = "none";

    fetch("/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          showError(data.error);
        } else {
          displayResults(data);
        }
      })
      .catch((error) => {
        showError("Une erreur est survenue lors de l'analyse de l'image.");
        console.error("Error:", error);
      })
      .finally(() => {
        loadingSpinner.style.display = "none";
      });
  }

  function displayResults(data) {
    predictionResult.textContent = data.prediction;
    confidenceBar.style.width = `${data.confidence}%`;
    descriptionText.textContent = data.description;
    resultSection.style.display = "block";
  }

  function showError(message) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-danger";
    alertDiv.textContent = message;
    resultSection.innerHTML = "";
    resultSection.appendChild(alertDiv);
    resultSection.style.display = "block";
  }
});
