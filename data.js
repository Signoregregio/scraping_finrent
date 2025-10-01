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

  function realIndex(i, length) {
    return i >= 0 ? i : length + i;
  }

  const indexCarToShow = indexCarsToShowRaw.map((indexShow) =>
    realIndex(indexShow, autoArray.length)
  );

  indexCarToShow.forEach((index) => {
    const auto = autoArray[index];
    const card = document.createElement("div");
    card.className = "card-auto";
    card.innerHTML = `
        <img class="immagine-auto" src="${
          auto.imageUrls?.[0] || ""
        }" alt="Foto macchina">
        <div class="etichetta-label">${auto.etichetta?.label || ""}</div>
        <img class="etichetta-icon" src="${auto.etichetta?.icon || ""}" alt="">
        <img class="timbro-icon" src="${auto.timbroUrl || ""}" alt="">
        <h3 class="nome-macchina">${auto.nomeMacchina}</h3>
        <p class="motore">Motore: ${auto.motore}</p>
        <p class="prezzo">Prezzo: ${auto.prezzo || "N.D."}</p>
        <p class="km-totali">KM inclusi: ${auto.kmTotali || "N.D."}</p>
        <p class="mesi">Durata: ${auto.mesi} mesi</p>
        <p class="anticipo">Anticipo: ${auto.anticipo || "Nessuno"}</p>
      `;
    container.appendChild(card);
  });
}
