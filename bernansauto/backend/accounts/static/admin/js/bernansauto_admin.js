(() => {
    const forceLightTheme = () => {
        const html = document.documentElement;
        html.dataset.theme = "light";
        html.style.colorScheme = "light";
        try {
            localStorage.setItem("theme", "light");
        } catch (error) {
            /* Ignore storage access errors */
        }
    };

    const hideThemeControls = () => {
        const selectors = [
            ".theme-toggle",
            ".theme-switch",
            "button[aria-label*='theme' i]",
            "button[title*='theme' i]",
            "button[aria-label*='тема' i]",
            "button[title*='тема' i]",
        ];

        selectors.forEach((selector) => {
            document.querySelectorAll(selector).forEach((element) => {
                element.style.display = "none";
            });
        });
    };

    forceLightTheme();
    hideThemeControls();
    window.addEventListener("load", () => {
        forceLightTheme();
        hideThemeControls();
    });
})();
