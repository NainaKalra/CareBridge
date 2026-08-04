const API_URL = "http://127.0.0.1:8000";

function timeAgo(dateStr) {
    const diffMs = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diffMs / 60000);
    if (mins < 1) return "just now";
    if (mins < 60) return `${mins} min ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs} hr${hrs > 1 ? "s" : ""} ago`;
    const days = Math.floor(hrs / 24);
    return `${days} day${days > 1 ? "s" : ""} ago`;
}

function calculateStreak(checkins) {
    // Counts consecutive days (from most recent) with at least one check-in
    const days = new Set(
        checkins.map(c => new Date(c.timestamp).toDateString())
    );
    let streak = 0;
    let cursor = new Date();
    while (days.has(cursor.toDateString())) {
        streak++;
        cursor.setDate(cursor.getDate() - 1);
    }
    return streak;
}

async function loadCheckins() {
    const heroEyebrow = document.getElementById("hero-eyebrow");
    const heroTitle = document.getElementById("hero-title");
    const heroSub = document.getElementById("hero-sub");
    const pulseRing = document.getElementById("pulse-ring");
    const pulseDot = document.getElementById("pulse-dot");
    const timeline = document.getElementById("timeline");

    try {
        const response = await fetch(`${API_URL}/checkins`);
        const data = await response.json();
        const checkins = data.checkins || [];

        if (checkins.length === 0) {
            heroEyebrow.textContent = "No data yet";
            heroTitle.textContent = "No check-ins so far";
            heroSub.textContent = "Once the first daily call happens, it'll show up here.";
            document.getElementById("stat-total").textContent = "0";
            document.getElementById("stat-streak").textContent = "0";
            document.getElementById("stat-attention").textContent = "0";
            timeline.innerHTML = `
        <div class="empty-state">
          <p class="empty-title">Nothing checked in yet</p>
          <p>Check-ins will appear here as soon as the first call happens.</p>
        </div>`;
            return;
        }

        // Hero — based on latest check-in
        const latest = checkins[0];
        const isAttention = latest.ai_result === "needs attention";

        heroEyebrow.textContent = isAttention ? "Needs attention" : "All good";
        heroEyebrow.className = "hero-eyebrow" + (isAttention ? " attention" : "");
        pulseRing.className = "pulse-ring" + (isAttention ? " attention" : "");
        pulseDot.className = "pulse-dot" + (isAttention ? " attention" : "");

        heroTitle.textContent = isAttention
            ? "Today's check-in needs a look"
            : "Everything looks normal";
        heroSub.textContent = `Last checked in ${timeAgo(latest.timestamp)}`;

        // Stats
        const attentionCount = checkins.filter(c => c.ai_result === "needs attention").length;
        document.getElementById("stat-total").textContent = checkins.length;
        document.getElementById("stat-streak").textContent = calculateStreak(checkins);
        document.getElementById("stat-attention").textContent = attentionCount;

        // Timeline
        timeline.innerHTML = "";
        checkins.forEach((checkin) => {
            const isAtt = checkin.ai_result === "needs attention";
            const item = document.createElement("div");
            item.className = "timeline-item";
            item.innerHTML = `
        <div class="timeline-dot ${isAtt ? "attention" : ""}"></div>
        <div class="checkin-card">
          <span class="badge ${isAtt ? "attention" : "normal"}">${isAtt ? "Needs Attention" : "Normal"}</span>
          <div class="transcript">"${checkin.transcript}"</div>
          <div class="timestamp">${new Date(checkin.timestamp).toLocaleString()}</div>
        </div>
      `;
            timeline.appendChild(item);
        });

    } catch (error) {
        console.error("Error loading check-ins:", error);
        heroTitle.textContent = "Couldn't load data";
        heroSub.textContent = "Make sure the backend server is running.";
        timeline.innerHTML = `<p class="empty-text">Failed to load check-ins.</p>`;
    }
}

loadCheckins();