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
                card.style.cursor = "pointer";
                card.dataset.playerId = player.playerID;
                card.innerHTML = `
                    <div class="player-number">${String(index + 1).padStart(2, '0')}</div>
                    <div class="player-info">
                        <div class="player-name">${player.first} ${player.last}</div>
                        <div class="player-position">Player</div>
                    </div>
                `;
                card.addEventListener('click', () => showPlayerDetails(player.playerID));
                playersGrid.appendChild(card);
            });
        } catch (error) {
            console.error("Failed to load players:", error);
            playersGrid.innerHTML = '<div class="error">⚠️ Failed to load players</div>';
        }
    });
});

// Player modal functions
async function showPlayerDetails(playerID) {
    const modal = document.getElementById('player-modal');
    const loading = document.getElementById('player-details-loading');
    const content = document.getElementById('player-details-content');

    modal.style.display = 'flex';
    loading.style.display = 'block';
    content.style.display = 'none';

    try {
        const res = await fetch(`/player/${playerID}`);
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        if (data.error) {
            loading.textContent = data.error;
            return;
        }

        document.getElementById('player-details-name').textContent = data.name || '';
        document.getElementById('player-birth-year').textContent = data.birthYear || '';
        document.getElementById('player-birth-city').textContent = data.birthCity || '';
        document.getElementById('player-birth-country').textContent = data.birthCountry || '';
        document.getElementById('player-height').textContent = data.height || '';
        document.getElementById('player-weight').textContent = data.weight || '';
        document.getElementById('player-bats').textContent = data.bats || '';
        document.getElementById('player-throws').textContent = data.throws || '';
        document.getElementById('player-debut').textContent = data.debut || '';

        const tbody = document.getElementById('batting-records');
        tbody.innerHTML = '';
        if (data.battingRecords && data.battingRecords.length) {
            data.battingRecords.forEach(r => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${r.year}</td>
                    <td>${r.team}</td>
                    <td>${r.games ?? ''}</td>
                    <td>${r.atBats ?? ''}</td>
                    <td>${r.runs ?? ''}</td>
                    <td>${r.hits ?? ''}</td>
                    <td>${r.doubles ?? ''}</td>
                    <td>${r.triples ?? ''}</td>
                    <td>${r.homeRuns ?? ''}</td>
                    <td>${r.rbi ?? ''}</td>
                    <td>${r.walks ?? ''}</td>
                    <td>${r.strikeouts ?? ''}</td>
                    <td>${r.stolenBases ?? ''}</td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="13">No batting records</td></tr>';
        }

        loading.style.display = 'none';
        content.style.display = 'block';
    } catch (err) {
        loading.textContent = 'Failed to load player details';
    }
}

function closePlayerModal() {
    const modal = document.getElementById('player-modal');
    modal.style.display = 'none';
}

// click outside to close
window.addEventListener('click', (e) => {
    const modal = document.getElementById('player-modal');
    if (e.target === modal) modal.style.display = 'none';
});