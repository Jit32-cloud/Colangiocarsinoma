function showSpinnerOnSubmit() {
    const form = document.getElementById("predictionForm");
    if (!form) return;

    form.addEventListener("submit", function (event) {
        const errorBox = document.getElementById("clientValidationError");
        const spinner = document.getElementById("loadingSpinner");
        const requiredFields = form.querySelectorAll("input, select");
        let valid = true;

        requiredFields.forEach((field) => {
            if (
                (field.type === "radio" && !form.querySelector(`input[name="${field.name}"]:checked`)) ||
                ((field.type === "text" || field.type === "number" || field.tagName === "SELECT") && !field.value)
            ) {
                valid = false;
            }
        });

        if (!valid) {
            event.preventDefault();
            errorBox.classList.remove("hidden");
            return;
        }

        errorBox.classList.add("hidden");
        spinner.classList.remove("hidden");
    });
}

function styleResultDynamically() {
    const percentElement = document.getElementById("riskPercent");
    const progress = document.getElementById("riskProgress");
    if (!percentElement || !progress) return;

    const value = parseFloat(percentElement.textContent);
    progress.style.width = `${Math.min(Math.max(value, 0), 100)}%`;
}

showSpinnerOnSubmit();
styleResultDynamically();

function syncDarkModeButton(isDark) {
    const modeButton = document.getElementById("darkModeToggle");
    if (!modeButton) return;
    modeButton.textContent = isDark ? "Light Mode" : "Dark Mode";
}

function applySavedTheme() {
    const savedTheme = localStorage.getItem("themePreference");
    const isDark = savedTheme === "dark";
    document.body.classList.toggle("dark-mode", isDark);
    syncDarkModeButton(isDark);
}

function initDarkModeToggle() {
    const modeButton = document.getElementById("darkModeToggle");
    if (!modeButton) return;

    modeButton.addEventListener("click", () => {
        const darkEnabled = document.body.classList.toggle("dark-mode");
        localStorage.setItem("themePreference", darkEnabled ? "dark" : "light");
        syncDarkModeButton(darkEnabled);
    });
}

applySavedTheme();
initDarkModeToggle();
