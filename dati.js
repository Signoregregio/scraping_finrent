retrieveData();



function retrieveData() {
  fetch("http://127.0.0.1:5000/data")
    .then((response) => {
      if (!response.ok) throw new Error("Errore nella risposta del server");
      return response.json();
    })
    .then((data) => {
      mostraAuto(data);
    })
    .catch((error) => {
      console.error("Errore nel recupero dei dati:", error);
    });
}

function mostraAuto(autoArray) {
  const container = document.getElementById("container-auto");
  container.innerHTML = "";

  autoArray.forEach((auto) => {
    const card = document.createElement("div");
    card.className = "card-auto";
    card.innerHTML = `
      <img src="${
        auto.imageUrls?.[0] || "placeholder.jpg"
      }" alt="Foto macchina">
      <h3 class="nome-macchina">${auto.nomeMacchina}</h3>
      <p class="motore" >Motore: ${auto.motore}</p>
      <p class="prezzo" >Prezzo: ${auto.prezzo || "N.D."}</p>
      <p class="km-totali" >KM inclusi: ${auto.kmTotali || "N.D."}</p>
      <p class="mesi">Durata: ${auto.mesi} mesi</p>
      <p class="anticipo">Anticipo: ${auto.anticipo || "Nessuno"}</p>
    `;
    container.appendChild(card);
  });
}
