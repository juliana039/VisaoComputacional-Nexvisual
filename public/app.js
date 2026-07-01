                  
                 
                   
                 
                      
                
                                                          
                                                                  
                 
  

const presetImages = [
  { label: "Gato 1", path: "/gatos/1.jpeg" },
  { label: "Gato 2", path: "/gatos/2.jpg" },
  { label: "Gato 3", path: "/gatos/3.png" },
  { label: "Gato 4", path: "/gatos/4.jpg" },
  { label: "Gato 5", path: "/gatos/5.png" },
  { label: "Gato 6", path: "/gatos/6.png" },
];

const uploadInput = document.querySelector("#uploadInput")                    ;
const presetButtons = document.querySelector("#presetButtons")               ;
const previewImage = document.querySelector("#previewImage")                    ;
const imageFrame = document.querySelector(".image-frame")               ;
const selectedName = document.querySelector("#selectedName")               ;
const analyzeButton = document.querySelector("#analyzeButton")                     ;
const resultContent = document.querySelector("#resultContent")               ;
const statusText = document.querySelector("#statusText")               ;

let selectedFile              = null;
let selectedObjectUrl                = null;

function setStatus(text        )       {
  statusText.textContent = text;
}

function setPreview(file      , previewUrl        , displayName        )       {
  if (selectedObjectUrl) {
    URL.revokeObjectURL(selectedObjectUrl);
    selectedObjectUrl = null;
  }

  selectedFile = file;
  previewImage.src = previewUrl;
  selectedName.textContent = displayName;
  imageFrame.classList.add("has-image");
  analyzeButton.disabled = false;
  setStatus("Pronto para analisar");
  resultContent.className = "result-content idle";
  resultContent.innerHTML = "<p>Clique em analisar para descobrir o tipo do gato.</p>";
}

async function choosePresetImage(path        , label        )                {
  const response = await fetch(path);
  const blob = await response.blob();
  const fileName = path.split("/").pop() || "gato.jpg";
  const file = new File([blob], fileName, { type: blob.type || "image/jpeg" });
  setPreview(file, path, label);
}

function chooseUploadedImage(file      )       {
  const objectUrl = URL.createObjectURL(file);
  setPreview(file, objectUrl, file.name);
  selectedObjectUrl = objectUrl;
}

function formatPercent(value        )         {
  return `${Math.round(value * 100)}%`;
}

function renderRanking(result           )         {
  if (!result.ranking?.length) {
    return "";
  }

  const rows = result.ranking
    .map(
      (item) => `
        <div class="ranking-row">
          <span>${item.label}</span>
          <strong>${formatPercent(item.probability)}</strong>
        </div>
      `,
    )
    .join("");

  return `<div class="ranking">${rows}</div>`;
}

function renderResult(result           )       {
  resultContent.className = "result-content";

  if (result.error) {
    setStatus("Erro");
    resultContent.innerHTML = `
      <div class="oops">
        <div>
          <h2>Erro</h2>
          <p>${result.error}</p>
        </div>
      </div>
    `;
    return;
  }

  if (!result.isCat) {
    setStatus("Não é gato");
    resultContent.innerHTML = `
      <div class="oops">
        <div>
          <h2>Oops!</h2>
          <p>${result.message || "Isso não é gato!"}</p>
        </div>
      </div>
    `;
    return;
  }

  setStatus("Gato encontrado");
  resultContent.innerHTML = `
    <h2 class="result-title">${result.label}</h2>
    <p class="confidence">Confiança: ${formatPercent(result.confidence || 0)}</p>
    ${result.meme ? `<img class="meme-image" src="${result.meme}" alt="Meme do resultado ${result.label}" />` : ""}
    ${renderRanking(result)}
  `;
}

async function analyzeSelectedImage()                {
  if (!selectedFile) {
    return;
  }

  analyzeButton.disabled = true;
  setStatus("Analisando...");
  resultContent.className = "result-content idle";
  resultContent.innerHTML = "<p>Analisando imagem com CLIP...</p>";

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      body: formData,
    });
    const result = (await response.json())             ;
    renderResult(result);
  } catch (error) {
    renderResult({ isCat: false, error: error instanceof Error ? error.message : "Erro inesperado." });
  } finally {
    analyzeButton.disabled = false;
  }
}

function renderPresetButtons()       {
  presetButtons.innerHTML = "";
  presetImages.forEach((preset, index) => {
    const button = document.createElement("button");
    button.className = "preset-button";
    button.type = "button";
    button.textContent = preset.label;
    button.addEventListener("click", async () => {
      document.querySelectorAll(".preset-button").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      await choosePresetImage(preset.path, preset.label);
    });
    presetButtons.appendChild(button);

    if (index === 0) {
      button.click();
    }
  });
}

uploadInput.addEventListener("change", () => {
  const file = uploadInput.files?.[0];
  if (file) {
    document.querySelectorAll(".preset-button").forEach((item) => item.classList.remove("active"));
    chooseUploadedImage(file);
  }
});

analyzeButton.addEventListener("click", analyzeSelectedImage);
renderPresetButtons();
