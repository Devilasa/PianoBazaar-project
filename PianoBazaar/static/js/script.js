document.addEventListener("DOMContentLoaded", function() {
        const footer = document.querySelector("footer"); // Seleziona il footer

        window.addEventListener("scroll", function () {
            const windowHeight = window.innerHeight; // Altezza visibile del viewport
            const documentHeight = document.documentElement.scrollHeight; // Altezza totale del documento
            const scrollTop = window.scrollY; // Posizione attuale dello scroll dall'alto

            // Calcolo: utente è alla fine della pagina
            const hasReachedBottom = (scrollTop + windowHeight) >= documentHeight;

            if (hasReachedBottom) {
                footer.classList.add("visible"); // Mostra il footer
            } else {
                footer.classList.remove("visible"); // Nascondi il footer
            }
    });
});