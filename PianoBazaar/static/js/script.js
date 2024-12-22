document.addEventListener("DOMContentLoaded", function() {
  const footer = document.querySelector("footer"); // Seleziona il footer
  let timeout = null;

  const checkScroll = () => {
    const windowHeight = window.innerHeight; // Altezza visibile del viewport
    const documentHeight = document.documentElement.scrollHeight; // Altezza totale del documento
    const scrollTop = window.scrollY; // Posizione attuale dello scroll dall'alto

    const hasReachedBottom = (scrollTop + windowHeight) >= documentHeight;

    if (hasReachedBottom) {
      footer.classList.add("visible");
    } else {
      footer.classList.remove("visible");
    }
  };

  window.addEventListener("scroll", function () {
    clearTimeout(timeout); // Cancella il timeout precedente
    timeout = setTimeout(checkScroll, 100); // Debouncing
  });
});

function adjustCardSizes() {
  const container = document.getElementById('card-container');
    if(!container) return;
  const containerWidth = container.clientWidth; // Larghezza orizzontale disponibile (in pixel)
  const cardMargin = 16; // Margine laterale (0.5rem = 16px, 8px su ogni lato)

  //minCardWidth = 325; (In pixel)
  //maxCardWidth = 435; (optimal range)
  //problema di PLI: f.obj.minimizzazione del resto in pixel; poi prova a risolverlo graficamente

  let actCardWidth = 325;

  let best_pixel_rest = 325;
  let best_card_width = 350;

  for (let i = 0; i < 23; i++) {
      let cardNumber = Math.floor(containerWidth / (actCardWidth+cardMargin));
      let pixel_rest = Math.floor(containerWidth - cardNumber * (actCardWidth+cardMargin));

      if (pixel_rest < best_pixel_rest) {
          best_pixel_rest = pixel_rest;
          best_card_width = actCardWidth;
      }
      actCardWidth += 5;
  }
  console.log(containerWidth);
  console.log("rest", best_pixel_rest);
  console.log(best_card_width);

  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.style.width = `${best_card_width}px`;
  });
}

window.addEventListener('load', adjustCardSizes);
window.addEventListener('resize', adjustCardSizes);
