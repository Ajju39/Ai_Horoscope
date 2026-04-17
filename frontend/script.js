const SUPABASE_URL = "https://jubjcswqdpuoebharyyk.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1Ympjc3dxZHB1b2ViaGFyeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjM1MjcxMSwiZXhwIjoyMDkxOTI4NzExfQ._2X9KrKcXXKY7lEPOzZXm4A7b2aFyaEutsIRce7KZs8";

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let latestHoroscope = null;
let currentUser = null;

const form = document.getElementById("horoscopeForm");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const result = document.getElementById("result");

async function refreshUser() {
  const statusBox = document.getElementById("authStatus");
  const { data, error } = await supabaseClient.auth.getUser();

  if (error) {
    statusBox.textContent = error.message;
    return;
  }

  currentUser = data.user || null;
  statusBox.textContent = currentUser
    ? `Logged in as ${currentUser.email}`
    : "Not logged in";
}

document.getElementById("signupBtn").addEventListener("click", async function () {
  const email = document.getElementById("authEmail").value.trim();
  const password = document.getElementById("authPassword").value.trim();
  const statusBox = document.getElementById("authStatus");

  if (!email || !password) {
    statusBox.textContent = "Please enter email and password.";
    return;
  }

  const { error } = await supabaseClient.auth.signUp({ email, password });

  statusBox.textContent = error ? error.message : "Signup successful!";
  await refreshUser();
});

document.getElementById("loginBtn").addEventListener("click", async function () {
  const email = document.getElementById("authEmail").value.trim();
  const password = document.getElementById("authPassword").value.trim();
  const statusBox = document.getElementById("authStatus");

  if (!email || !password) {
    statusBox.textContent = "Please enter email and password.";
    return;
  }

  const { data, error } = await supabaseClient.auth.signInWithPassword({
    email,
    password
  });

  if (error) {
    statusBox.textContent = error.message;
    return;
  }

  currentUser = data.user;
  statusBox.textContent = `Logged in as ${data.user.email}`;
});

document.getElementById("logoutBtn").addEventListener("click", async function () {
  const statusBox = document.getElementById("authStatus");
  const { error } = await supabaseClient.auth.signOut();

  if (error) {
    statusBox.textContent = error.message;
    return;
  }

  currentUser = null;
  statusBox.textContent = "Logged out";
});

refreshUser();
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
      user_id: currentUser ? currentUser.id : null
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

      latestHoroscope = data;

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

const loadHistoryBtn = document.getElementById("loadHistoryBtn");
if (loadHistoryBtn) {
  loadHistoryBtn.addEventListener("click", async function () {
    const historyBox = document.getElementById("historyBox");

    if (!currentUser) {
      historyBox.innerHTML = <div class="history-empty">Please login first.</div>;
      return;
    }

    historyBox.innerHTML = <div class="history-empty">Loading history...</div>;

    try {
      const response = await fetch(
        `https://ai-horoscope-zosx.onrender.com/history/${encodeURIComponent(currentUser.id)}`
      );
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load history.");
      }

      const history = data.history || [];

      if (history.length === 0) {
        historyBox.innerHTML = <div class="history-empty">No saved readings found.</div>;
        return;
      }

      historyBox.innerHTML = history.map(item => `
        <div class="history-item">
          <h3>${formatDate(item.created_at)}</h3>
          <div><strong>Name:</strong> ${item.name || ""}</div>
          <div><strong>Birth Place:</strong> ${item.birth_place || ""}</div>
          <div><strong>Sun:</strong> ${item.sun_sign || ""}</div>
          <div><strong>Moon:</strong> ${item.moon_sign || ""}</div>
          <div><strong>Ascendant:</strong> ${item.ascendant || ""}</div>
        </div>
      `).join("");
    } catch (error) {
      historyBox.innerHTML = <div class="history-empty">${error.message}</div>;
    }
  });
}

const chatBtn = document.getElementById("chatBtn");
if (chatBtn) {
  chatBtn.addEventListener("click", async function () {
    const question = document.getElementById("chatQuestion").value.trim();
    const replyBox = document.getElementById("chatReply");

    if (!latestHoroscope) {
      replyBox.textContent = "Please generate a horoscope first.";
      return;
    }

    if (!question) {
      replyBox.textContent = "Please enter a question.";
      return;
    }

    replyBox.textContent = "Thinking...";

    try {
      const response = await fetch("https://ai-horoscope-zosx.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: latestHoroscope.name,
          sun_sign: latestHoroscope.sun_sign,
          moon_sign: latestHoroscope.moon_sign,
          ascendant: latestHoroscope.ascendant,
          question: question
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat failed.");
      }

      replyBox.textContent = data.reply || "";
    } catch (error) {
      replyBox.textContent = error.message;
    }
  });
}

function formatDate(dateString) {
  if (!dateString) return "";
  return new Date(dateString).toLocaleString();
}

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

refreshUser();
