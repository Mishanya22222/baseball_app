document.addEventListener("DOMContentLoaded", async () => {
    const yearSelect = document.getElementById("year-select");
    const teamSelect = document.getElementById("team-select");
    const playersSection = document.getElementById("players-section");
    const playersGrid = document.getElementById("players-grid");
    const emptyState = document.getElementById("empty-state");
    const teamTitle = document.getElementById("team-title");
    const teamInfo = document.getElementById("team-info");

    let currentTeamName = "";

    // Load years on page load
    try {
        const response = await fetch("/years");
        const years = await response.json();

        yearSelect.innerHTML = '<option value="">📅 Select a year...</option>';
        years.forEach(year => {
            const option = document.createElement("option");
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        });
        yearSelect.disabled = false;
    } catch (error) {
        console.error("Failed to load years:", error);
        yearSelect.innerHTML = '<option value="">⚠️ Failed to load years</option>';
    }

    // Handle year selection
    yearSelect.addEventListener("change", async () => {
        const year = yearSelect.value;
        
        // Reset team dropdown
        teamSelect.innerHTML = '<option value="">🏟️ Select a team...</option>';
        teamSelect.disabled = true;
        playersSection.hidden = true;
        emptyState.hidden = false;

        if (!year) {
            return;
        }

        // Load teams for selected year
        try {
            const response = await fetch(`/teams?year=${year}`);
            const teams = await response.json();

            teamSelect.innerHTML = '<option value="">🏟️ Select a team...</option>';
            teams.forEach(team => {
                const option = document.createElement("option");
                option.value = team.teamID;
                option.textContent = team.name;
                option.dataset.name = team.name;
                teamSelect.appendChild(option);
            });
            teamSelect.disabled = false;
        } catch (error) {
            console.error("Failed to load teams:", error);
            teamSelect.innerHTML = '<option value="">⚠️ Failed to load teams</option>';
        }
    });

    // Handle team selection
    teamSelect.addEventListener("change", async () => {
        const year = yearSelect.value;
        const teamID = teamSelect.value;

        if (!year || !teamID) {
            playersSection.hidden = true;
            emptyState.hidden = false;
            return;
        }

        // Get team name from selected option
        currentTeamName = teamSelect.options[teamSelect.selectedIndex].text;
        teamTitle.textContent = `${currentTeamName} Roster`;
        teamInfo.textContent = `Season: ${year}`;

        playersGrid.innerHTML = '<div class="loading">Loading players...</div>';
        playersSection.hidden = false;
        emptyState.hidden = true;

        // Load players
        try {
            const response = await fetch(`/players?year=${year}&teamID=${teamID}`);
            const players = await response.json();

            playersGrid.innerHTML = "";

            if (players.length === 0) {
                playersGrid.innerHTML = '<div class="no-data">No players found for this team</div>';
                return;
            }

            players.forEach((player, index) => {
                const card = document.createElement("div");
                card.className = "player-card";
                card.innerHTML = `
                    <div class="player-number">${String(index + 1).padStart(2, '0')}</div>
                    <div class="player-info">
                        <div class="player-name">${player.first} ${player.last}</div>
                        <div class="player-position">Player</div>
                    </div>
                `;
                playersGrid.appendChild(card);
            });
        } catch (error) {
            console.error("Failed to load players:", error);
            playersGrid.innerHTML = '<div class="error">⚠️ Failed to load players</div>';
        }
    });
});