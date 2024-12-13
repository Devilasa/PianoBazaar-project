document.addEventListener("DOMContentLoaded", function() {
        const footer = document.querySelector("footer"); // Seleziona il footer
        let lastScrollY = window.scrollY; // Posizione iniziale dello scroll

        window.addEventListener("scroll", function() {
            const currentScrollY = window.scrollY;

            if (currentScrollY > lastScrollY) {
                footer.classList.add("visible");
            } else {
                footer.classList.remove("visible");
            }

            lastScrollY = currentScrollY;
        });
});