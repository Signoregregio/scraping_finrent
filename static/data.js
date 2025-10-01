const carsToShow = [1, 2, 3, 4, 5, -2, -1];
let allCars = [];
let currentIndex = 0;
let autoSlide = true;
let slideInterval;
const slideIntervalTimer = 500000;

retrieveData();

function retrieveData() {
  fetch("/data")
    .then((response) => {
      if (!response.ok) throw new Error("Errore nella risposta del server");
      return response.json();
    })
    .then((data) => {
      allCars = filterCars(data, carsToShow);
      initCarousel();
    })
    .catch((error) => {
      console.error("Errore nel recupero dei dati:", error);
    });
}

function filterCars(autoArray, indexCarsToShowRaw) {
  function realIndex(i, length) {
    return i >= 0 ? i : length + i;
  }

  const indexCarToShow = indexCarsToShowRaw.map((indexShow) =>
    realIndex(indexShow, autoArray.length)
  );

  return indexCarToShow.map(index => autoArray[index]);
}

function initCarousel() {
  if (allCars.length === 0) return;
  
  createDots();
  showCurrentCar();
  setupControls();
  startAutoSlide();
}

function showCurrentCar() {
  const container = document.getElementById("container-auto");
  const counter = document.getElementById("counter");
  
  container.innerHTML = "";
  
  const auto = allCars[currentIndex];
  const card = document.createElement("div");
  card.className = "card-auto";
  card.innerHTML = `
    <div class="car-image-container">
      <img class="immagine-auto" src="${auto.imageUrls?.[0] || ""}" alt="Foto macchina">
      <div class="etichetta-label">${auto.etichetta?.label || ""}</div>
    </div>
    <div class="car-info">
      <h1 class="nome-macchina">${auto.nomeMacchina}</h1>
      <div class="car-details">
        <div class="detail-item">
          <span class="detail-label">Motore:</span>
          <span class="detail-value">${auto.motore}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Prezzo:</span>
          <span class="detail-value">${auto.prezzo || "N.D."}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">KM inclusi:</span>
          <span class="detail-value">${auto.kmTotali || "N.D."}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Durata:</span>
          <span class="detail-value">${auto.mesi} mesi</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Anticipo:</span>
          <span class="detail-value">${auto.anticipo || "Nessuno"}</span>
        </div>
      </div>
    </div>
  `;
  
  container.appendChild(card);
  counter.textContent = `${currentIndex + 1} / ${allCars.length}`;
  updateDots();
}

function createDots() {
  const dotsContainer = document.getElementById("dots-container");
  dotsContainer.innerHTML = "";
  
  allCars.forEach((_, index) => {
    const dot = document.createElement("span");
    dot.className = "dot";
    dot.addEventListener("click", () => goToSlide(index));
    dotsContainer.appendChild(dot);
  });
}

function updateDots() {
  const dots = document.querySelectorAll(".dot");
  dots.forEach((dot, index) => {
    dot.classList.toggle("active", index === currentIndex);
  });
}

function goToSlide(index) {
  currentIndex = index;
  showCurrentCar();
  resetAutoSlide();
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % allCars.length;
  showCurrentCar();
}

function prevSlide() {
  currentIndex = (currentIndex - 1 + allCars.length) % allCars.length;
  showCurrentCar();
}

function setupControls() {
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  
  prevBtn.addEventListener("click", () => {
    prevSlide();
    resetAutoSlide();
  });
  
  nextBtn.addEventListener("click", () => {
    nextSlide();
    resetAutoSlide();
  });
  
  // Controlli da tastiera
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") {
      prevSlide();
      resetAutoSlide();
    } else if (e.key === "ArrowRight") {
      nextSlide();
      resetAutoSlide();
    } else if (e.key === " ") {
      e.preventDefault();
      toggleAutoSlide();
    }
  });
}

function startAutoSlide() {
  if (!autoSlide) return;
  slideInterval = setInterval(nextSlide, slideIntervalTimer); // Cambia ogni 5 secondi
}

function stopAutoSlide() {
  clearInterval(slideInterval);
}

function resetAutoSlide() {
  stopAutoSlide();
  if (autoSlide) startAutoSlide();
}

function toggleAutoSlide() {
  autoSlide = !autoSlide;
  if (autoSlide) {
    startAutoSlide();
  } else {
    stopAutoSlide();
  }
}