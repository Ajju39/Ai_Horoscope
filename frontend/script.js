const form = document.getElementById("horoscopeForm");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const result = document.getElementById("result");

function showLoading() {
  if (loading) loading.classList.remove("hidden");
}

function hideLoading() {
  if (loading) loading.classList.add("hidden");
}

function showError(message) {
  if (!errorBox) return;
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function hideError() {
  if (!errorBox) return;
  errorBox.textContent = "";
  errorBox.classList.add("hidden");
}

function showResult() {
  if (result) result.classList.remove("hidden");
}

function hideResult() {
  if (result) result.classList.add("hidden");
}

if (form) {
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    hideError();
    hideResult();
    showLoading();

    const payload = {
      name: document.getElementById("name").value.trim(),
      birth_date: document.getElementById("birth_date").value,
      birth_time: document.getElementById("birth_time").value,
      birth_place: document.getElementById("birth_place").value.trim(),
      user_id: window.currentUser ? window.currentUser.id : null
    };

    try {
      const response = await fetch("https://ai-horoscope-zosx.onrender.com/generate-horoscope", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong while generating horoscope.");
      }

      document.getElementById("r_name").textContent = data.name || "";
      document.getElementById("r_location").textContent = data.formatted_address || "";
      document.getElementById("r_latitude").textContent = data.latitude ?? "";
      document.getElementById("r_longitude").textContent = data.longitude ?? "";
      document.getElementById("r_sun_sign").textContent = data.sun_sign || "";
      document.getElementById("r_moon_sign").textContent = data.moon_sign || "";
      document.getElementById("r_ascendant").textContent = data.ascendant || "";
      document.getElementById("r_finance").textContent = data.finance || "";
      document.getElementById("r_career").textContent = data.career || "";
      document.getElementById("r_health").textContent = data.health || "";
      document.getElementById("r_relationship").textContent = data.relationship || "";
      document.getElementById("r_ai_horoscope").textContent =
        data.ai_horoscope || "AI horoscope not available.";

      hideLoading();
      showResult();
    } catch (error) {
      hideLoading();
      showError(error.message);
    }
  });
}