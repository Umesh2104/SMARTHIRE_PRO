// ============================================================
// SmartHire AI — script.js
// ============================================================

// ── Dark Mode Toggle ─────────────────────────────────────────
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("darkModeToggle");
  if (!toggle) return;
  const icon = toggle.querySelector("i");

  function applyMode(dark) {
    if (dark) {
      document.body.classList.add("dark-mode");
      icon.classList.replace("fa-moon", "fa-sun");
      localStorage.setItem("darkMode", "enabled");
    } else {
      document.body.classList.remove("dark-mode");
      icon.classList.replace("fa-sun", "fa-moon");
      localStorage.setItem("darkMode", "disabled");
    }
  }

  // Restore preference
  const pref = localStorage.getItem("darkMode");
  if (pref === "enabled") applyMode(true);
  else if (pref === "disabled") applyMode(false);
  // else: body.dark-mode is the default set by base.html class

  toggle.addEventListener("click", () => {
    applyMode(!document.body.classList.contains("dark-mode"));
  });
});

// ── Interview Room (only on interview page) ──────────────────
if (document.getElementById("questionContainer")) {

  /* --- State --- */
  let currentIndex = 0;
  const questions    = interview.questions;
  const total        = questions.length;
  const TIME_PER_Q   = 3 * 60;           // 3 minutes per question
  let   timeLeft     = total * TIME_PER_Q;
  let   timerInterval = null;
  let   saveTimer     = null;
  let   recognition   = null;
  let   isRecording   = false;

  /* --- DOM refs --- */
  const progressBar      = document.getElementById("progressBar");
  const qContainer       = document.getElementById("questionContainer");
  const prevBtn          = document.getElementById("prevBtn");
  const nextBtn          = document.getElementById("nextBtn");
  const timerEl          = document.getElementById("timer");

  /* ---- Render a question ---- */
  function renderQuestion(idx) {
    const q = questions[idx];
    const isDark = document.body.classList.contains("dark-mode");
    const textareaStyle = isDark
      ? "background:#1f1f1f;color:#fff;border:1px solid #333;"
      : "background:#fff;color:#1e293b;border:1px solid #cbd5e1;";

    qContainer.innerHTML = `
      <div class="mb-3">
        <h5 class="mb-1" style="font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;opacity:0.6">
          Question ${idx + 1} of ${total}
        </h5>
        <p class="lead fw-semibold mb-3" style="font-size:1.05rem">${q.question}</p>
        <textarea
          class="form-control"
          id="answerArea"
          rows="6"
          placeholder="Type your answer here… Be specific and use examples."
          style="${textareaStyle}border-radius:12px!important;resize:vertical;line-height:1.6"
        >${q.answer || ""}</textarea>

        <div class="d-flex align-items-center gap-3 mt-2 flex-wrap">
          <button class="voice-btn btn" id="voiceBtn" onclick="toggleVoice()" type="button">
            <i class="fas fa-microphone" id="voiceIcon"></i>
            <span id="voiceBtnText">Speak Answer</span>
          </button>
          <span class="voice-not-supported" id="voiceNotSupported" style="display:none;font-size:0.8rem;opacity:0.6">
            Voice not supported in this browser
          </span>
          <span class="ms-auto save-indicator" id="saveIndicator">
            <i class="fas fa-check-circle me-1"></i>Saved
          </span>
          <span class="word-count-label" id="wordCount">0 words</span>
        </div>
      </div>
    `;

    // Progress
    progressBar.style.width = `${((idx + 1) / total) * 100}%`;

    // Nav buttons
    prevBtn.disabled = idx === 0;
    nextBtn.innerHTML = idx === total - 1
      ? '<i class="fas fa-paper-plane me-1"></i>Submit'
      : 'Next <i class="fas fa-chevron-right"></i>';
    nextBtn.className = idx === total - 1
      ? "btn btn-success"
      : "btn btn-outline-primary";

    // Word count listener
    document.getElementById("answerArea").addEventListener("input", function () {
      updateWordCount(this.value);
      clearTimeout(saveTimer);
      saveTimer = setTimeout(() => autoSave(idx, this.value), 1200);
    });

    updateWordCount(q.answer || "");
    stopVoice();
    initVoice();
  }

  /* ---- Word count ---- */
  function updateWordCount(text) {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const el = document.getElementById("wordCount");
    if (!el) return;
    el.textContent = `${words} word${words !== 1 ? "s" : ""}`;
    el.className = `word-count-label${words >= 30 ? " good" : ""}`;
  }

  /* ---- Auto-save ---- */
  async function autoSave(idx, answer) {
    try {
      const fd = new FormData();
      fd.append("q_index", idx);
      fd.append("answer", answer);
      await fetch("/save_answer", { method: "POST", body: fd });
      questions[idx].answer = answer;
      const ind = document.getElementById("saveIndicator");
      if (ind) { ind.classList.add("show"); setTimeout(() => ind.classList.remove("show"), 2000); }
    } catch (e) {}
  }

  function saveCurrentAnswer() {
    const ta = document.getElementById("answerArea");
    if (!ta) return;
    const val = ta.value.trim();
    questions[currentIndex].answer = val;
    autoSave(currentIndex, val);
  }

  /* ---- Navigation ---- */
  prevBtn.addEventListener("click", () => {
    if (currentIndex > 0) {
      saveCurrentAnswer();
      currentIndex--;
      renderQuestion(currentIndex);
    }
  });

  nextBtn.addEventListener("click", () => {
    saveCurrentAnswer();
    if (currentIndex < total - 1) {
      currentIndex++;
      renderQuestion(currentIndex);
    } else {
      showSubmitConfirm();
    }
  });

  /* ---- Timer ---- */
  function startTimer() {
    updateTimerDisplay();
    timerInterval = setInterval(() => {
      timeLeft--;
      updateTimerDisplay();
      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        saveCurrentAnswer();
        submitInterview();
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const mins = Math.floor(timeLeft / 60);
    const secs = timeLeft % 60;
    timerEl.textContent = `${String(mins).padStart(2,"0")}:${String(secs).padStart(2,"0")}`;
    timerEl.className = "badge bg-primary";
    if (timeLeft <= 60)  timerEl.className = "badge bg-danger timer-danger";
    else if (timeLeft <= 180) timerEl.className = "badge bg-warning timer-warning";
  }

  /* ---- Submit ---- */
  function showSubmitConfirm() {
    const unanswered = questions.filter(q => !(q.answer || "").trim()).length;
    const msg = unanswered > 0
      ? `You have ${unanswered} unanswered question(s). They will score 0. Submit anyway?`
      : "Submit your interview now? You cannot change answers after this.";
    if (confirm(msg)) submitInterview();
  }

  function submitInterview() {
    clearInterval(timerInterval);
    fetch("/submit_interview", { method: "POST" })
      .then(res => {
        if (res.redirected) window.location.href = res.url;
        else window.location.href = "/dashboard";
      })
      .catch(() => { window.location.href = "/dashboard"; });
  }

  /* ---- Voice Input ---- */
  function initVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      const nb = document.getElementById("voiceNotSupported");
      const vb = document.getElementById("voiceBtn");
      if (nb) nb.style.display = "inline";
      if (vb) vb.style.display = "none";
      return;
    }
    recognition = new SpeechRecognition();
    recognition.continuous    = true;
    recognition.interimResults = true;
    recognition.lang = "en-IN";

    recognition.onresult = (event) => {
      let finalText = "";
      let interimText = "";
      for (let i = 0; i < event.results.length; i++) {
        if (event.results[i].isFinal) finalText    += event.results[i][0].transcript + " ";
        else                           interimText  += event.results[i][0].transcript;
      }
      const ta = document.getElementById("answerArea");
      if (!ta) return;
      const base = questions[currentIndex].answer || "";
      const sep  = base && !base.endsWith(" ") ? " " : "";
      ta.value = base + sep + finalText + interimText;
      updateWordCount(ta.value);
    };

    recognition.onend = () => {
      const ta = document.getElementById("answerArea");
      if (ta) { questions[currentIndex].answer = ta.value; autoSave(currentIndex, ta.value); }
      setRecordingState(false);
    };

    recognition.onerror = () => setRecordingState(false);
  }

  window.toggleVoice = function () {
    if (isRecording) stopVoice();
    else startVoice();
  };

  function startVoice() {
    if (!recognition) return;
    // Snapshot current answer as base before voice appends
    const ta = document.getElementById("answerArea");
    if (ta) questions[currentIndex].answer = ta.value;
    recognition.start();
    setRecordingState(true);
  }

  function stopVoice() {
    if (recognition && isRecording) recognition.stop();
    setRecordingState(false);
  }

  function setRecordingState(state) {
    isRecording = state;
    const btn  = document.getElementById("voiceBtn");
    const txt  = document.getElementById("voiceBtnText");
    if (!btn || !txt) return;
    if (state) {
      btn.classList.add("recording");
      txt.textContent = "Stop Recording";
    } else {
      btn.classList.remove("recording");
      txt.textContent = "Speak Answer";
    }
  }

  /* ---- Boot ---- */
  renderQuestion(0);
  startTimer();
}