const API_URL = "http://127.0.0.1:8000";

async function loadCheckins() {
    try {
        const response = await fetch(`${API_URL}/checkins`);
        const data = await response.json();
        const checkins = data.checkins || [];

        const listDiv = document.getElementById("checkins-list");
        const statusBanner = document.getElementById("status-banner");

        if (checkins.length === 0) {
            listDiv.innerHTML = "<p>No check-ins yet.</p>";
            statusBanner.textContent = "No check-ins yet.";
            return;
        }

        // Update top banner based on most recent check-in
        const latest = checkins[0];
        if (latest.ai_result === "needs attention") {
            statusBanner.textContent = "⚠️ Latest check-in needs attention.";
            statusBanner.classList.add("attention");
        } else {
            statusBanner.textContent = "✅ All good — latest check-in was normal.";
        }

        // Render check-in list
        listDiv.innerHTML = "";
        checkins.forEach((checkin) => {
            const card = document.createElement("div");
            card.className = "checkin-card";

            const badgeClass = checkin.ai_result === "needs attention" ? "attention" : "normal";
            const badgeText = checkin.ai_result === "needs attention" ? "Needs Attention" : "Normal";

            card.innerHTML = `
        <span class="badge ${badgeClass}">${badgeText}</span>
        <div class="transcript">"${checkin.transcript}"</div>
        <div class="timestamp">${new Date(checkin.timestamp).toLocaleString()}</div>
      `;

            listDiv.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading check-ins:", error);
        document.getElementById("checkins-list").innerHTML = "<p>Failed to load check-ins.</p>";
    }
}

loadCheckins();