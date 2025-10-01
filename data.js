let carsToShow = [1, 2, 3, 4, 5, -2, -1];
retrieveData();

function retrieveData() {
  fetch("http://127.0.0.1:5000/data")
    .then((response) => {
      if (!response.ok) throw new Error("Errore nella risposta del server");
      return response.json();
    })
    .then((data) => {
      showCars(data, carsToShow);
    })
    .catch((error) => {
      console.error("Errore nel recupero dei dati:", error);
    });
}

function showCars(autoArray, indexCarsToShowRaw) {
  const container = document.getElementById("container-auto");
  container.innerHTML = "";

  // Funzione per convertire indice negativo in reale
  function realIndex(i, length) {
    return i >= 0 ? i : length + i;
  }

  // Calcola gli indici reali corretti da carsToShow
  const indexCarToShow = indexCarsToShowRaw.map((indexShow) =>
    realIndex(indexShow, autoArray.length)
  );

  autoArray.forEach((auto, index) => {
    // Mostra solo le auto il cui indice è presente in indicesToShow
    if (indexCarToShow.includes(index)) {
      const card = document.createElement("div");
      card.className = "card-auto";
      card.innerHTML = `
        <img src="${
          auto.imageUrls?.[0] || "placeholder.jpg"
        }" alt="Foto macchina">
        <h3 class="nome-macchina">${auto.nomeMacchina}</h3>
        <p class="motore">Motore: ${auto.motore}</p>
        <p class="prezzo">Prezzo: ${auto.prezzo || "N.D."}</p>
        <p class="km-totali">KM inclusi: ${auto.kmTotali || "N.D."}</p>
        <p class="mesi">Durata: ${auto.mesi} mesi</p>
        <p class="anticipo">Anticipo: ${auto.anticipo || "Nessuno"}</p>
      `;
      container.appendChild(card);
    }
  });
}
