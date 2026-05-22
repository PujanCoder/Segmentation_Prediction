/* main.js — Customer Segmentation Frontend */

const formCard   = document.getElementById("form-card");
const resultCard = document.getElementById("result-card");
const predictBtn = document.getElementById("predictBtn");
const resetBtn   = document.getElementById("resetBtn");
const errorMsg   = document.getElementById("error-msg");

// Result DOM targets
const resEmoji   = document.getElementById("res-emoji");
const resCluster = document.getElementById("res-cluster");
const resName    = document.getElementById("res-name");
const resDesc    = document.getElementById("res-desc");
const resTags    = document.getElementById("res-tags");

// ── Collect & validate inputs ────────────────────────────────────
function getInputs() {
  const fields = ["income", "age", "recency", "spending", "purchases", "webvisits"];
  const data   = {};
  for (const id of fields) {
    const val = document.getElementById(id).value.trim();
    if (val === "") return { error: `Please fill in all fields (missing: ${id}).` };
    const num = parseFloat(val);
    if (isNaN(num) || num < 0) return { error: `"${id}" must be a non-negative number.` };
    data[id] = num;
  }
  return { data };
}

// ── Show error ───────────────────────────────────────────────────
function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.hidden = false;
}
function clearError() { errorMsg.hidden = true; errorMsg.textContent = ""; }

// ── Render result ─────────────────────────────────────────────────
function renderResult(res) {
  resEmoji.textContent            = res.emoji;
  resCluster.textContent          = `CLUSTER ${res.cluster}`;
  resName.textContent             = res.name;
  resName.style.color             = res.color;
  resDesc.textContent             = res.description;

  // Tags
  resTags.innerHTML = "";
  res.tags.forEach(tag => {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = tag;
    span.style.color       = res.color;
    span.style.borderColor = res.color + "55"; // 33 % opacity border
    span.style.background  = res.color + "11";
    resTags.appendChild(span);
  });

  formCard.hidden   = true;
  resultCard.hidden = false;
}

// ── Predict ───────────────────────────────────────────────────────
predictBtn.addEventListener("click", async () => {
  clearError();
  const { data, error } = getInputs();
  if (error) { showError(error); return; }

  // Loading state
  predictBtn.classList.add("loading");
  predictBtn.disabled = true;
  predictBtn.querySelector(".btn-text").textContent = "Classifying";

  try {
    const response = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(data),
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || `Server error ${response.status}`);
    }

    const result = await response.json();
    renderResult(result);

  } catch (err) {
    showError("Prediction failed: " + err.message);
  } finally {
    predictBtn.classList.remove("loading");
    predictBtn.disabled = false;
    predictBtn.querySelector(".btn-text").textContent = "Classify Customer";
  }
});

// ── Reset ─────────────────────────────────────────────────────────
resetBtn.addEventListener("click", () => {
  resultCard.hidden = true;
  formCard.hidden   = false;
  clearError();
  // Optionally clear inputs
  ["income","age","recency","spending","purchases","webvisits"]
    .forEach(id => { document.getElementById(id).value = ""; });
});
