document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:5000/api';
    const loadingElement = document.getElementById('loading');
    const contentElement = document.getElementById('content');
    
    // Fetch all data concurrently
    Promise.all([
        fetch(`${API_BASE_URL}/driver-standings`).then(res => res.json()),
        fetch(`${API_BASE_URL}/constructor-standings`).then(res => res.json()),
        fetch(`${API_BASE_URL}/next-race`).then(res => res.json()),
        fetch(`${API_BASE_URL}/current-season`).then(res => res.json()),
        fetch(`${API_BASE_URL}/last-race-podium`).then(res => res.json())
    ])
    .then(([driverStandings, constructorStandings, nextRace, seasonData, lastRacePodium]) => {
        // Populate driver standings
        populateDriverStandings(driverStandings);
        
        // Populate constructor standings
        populateConstructorStandings(constructorStandings);
        
        // Populate next race info
        populateNextRace(nextRace);
        
        // Populate last race podium
        populateLastRacePodium(lastRacePodium);
        
        // Hide loading and show content
        loadingElement.style.display = 'none';
        contentElement.style.display = 'block';
    })
    .catch(error => {
        console.error('Error fetching F1 data:', error);
        loadingElement.innerHTML = `
            <p class="error">Error loading F1 data. Please try again later.</p>
            <p class="error-details">${error.message}</p>
        `;
    });
    
    function populateDriverStandings(drivers) {
        const driverStandingsElement = document.getElementById('driver-standings');
        
        if (!drivers || drivers.error) {
            driverStandingsElement.innerHTML = '<p class="error">Unable to load driver standings</p>';
            return;
        }
        
        let html = '<table class="standings-table driver-standings-table">';
        html += '<thead><tr><th>Pos</th><th>Driver</th><th>Car</th><th>Pts</th></tr></thead>';
        html += '<tbody>';
        
        drivers.forEach(driver => {
            // Add a class for top 3 drivers
            const rowClass = driver.position <= 3 ? `top-${driver.position}` : '';
            
            html += `
                <tr class="${rowClass}">
                    <td class="position">${driver.position || '-'}</td>
                    <td class="driver-info">
                        <div class="driver-details">
                            <span class="driver-name">${driver.full_name}</span>
                        </div>
                    </td>
                    <td class="team">${driver.team}</td>
                    <td class="points">${driver.points}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        driverStandingsElement.innerHTML = html;
    }
    
    function populateConstructorStandings(constructors) {
        const constructorStandingsElement = document.getElementById('constructor-standings');
        
        if (!constructors || constructors.error) {
            constructorStandingsElement.innerHTML = '<p class="error">Unable to load constructor standings</p>';
            return;
        }
        
        let html = '<table class="standings-table">';
        html += '<thead><tr><th>Pos</th><th>Team</th><th>Points</th></tr></thead>';
        html += '<tbody>';
        
        constructors.forEach(constructor => {
            html += `
                <tr>
                    <td>${constructor.position}</td>
                    <td>${constructor.team}</td>
                    <td class="points">${constructor.points}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        constructorStandingsElement.innerHTML = html;
    }
    
    function populateNextRace(race) {
        const nextRaceElement = document.getElementById('next-race-info');
        
        if (!race || race.error) {
            nextRaceElement.innerHTML = '<p class="error">Unable to load next race information</p>';
            return;
        }
        
        const raceDate = new Date(race.date);
        const formattedDate = raceDate.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // Format race time if available
        let timeString = '';
        if (race.time) {
            const timeParts = race.time.split(':');
            const hour = parseInt(timeParts[0]);
            const minute = parseInt(timeParts[1]) || 0;
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const hour12 = hour % 12 || 12;
            timeString = `<span class="race-time">${hour12}:${minute.toString().padStart(2, '0')} ${ampm} ${race.timezone}</span>`;
        }
        
        nextRaceElement.innerHTML = `
            <div class="next-race-banner">
                <div class="next-race-header">
                    <h2>Next Race</h2>
                    <div class="countdown-badge">${race.days_until} days to go</div>
                </div>
                <div class="next-race-content">
                    <div class="race-title">
                        <h3>${race.name}</h3>
                        <p class="race-round">Round ${race.round}</p>
                    </div>
                    <div class="race-details">
                        <p class="race-location"><i class="fas fa-map-marker-alt"></i> ${race.location}, ${race.country}</p>
                        <p class="race-date"><i class="far fa-calendar-alt"></i> ${formattedDate} ${timeString}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    function populateLastRacePodium(podiumData) {
        // Add this section to the HTML first
        const raceResultsSection = document.createElement('section');
        raceResultsSection.className = 'last-race-results';
        raceResultsSection.innerHTML = `
            <h2>Last Race Results</h2>
            <div class="last-race-container">
                <div class="standings-card">
                    <h3>Last Race Podium</h3>
                    <div id="last-race-podium"></div>
                </div>
            </div>
        `;
        
        // Insert after current-standings section
        const currentStandingsSection = document.querySelector('.current-standings');
        currentStandingsSection.parentNode.insertBefore(raceResultsSection, currentStandingsSection.nextSibling);
        
        const podiumElement = document.getElementById('last-race-podium');
        
        if (!podiumData || podiumData.error || !podiumData.podium) {
            podiumElement.innerHTML = '<p class="error">Unable to load last race podium</p>';
            return;
        }
        
        podiumElement.innerHTML = `
            <div class="podium">
                <h4>Results from ${podiumData.race_name}</h4>
                <div class="podium-positions">
                    ${podiumData.podium.map(driver => `
                        <div class="podium-position position-${driver.position}">
                            <div class="position-number">${driver.position}</div>
                            <div class="driver-code">${driver.driver_code}</div>
                            <div class="driver-name">${driver.full_name}</div>
                            <div class="driver-team">${driver.team}</div>
                        </div>
                    `).join('')}
                </div>
                <p class="race-date">Race date: ${new Date(podiumData.race_date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                })}</p>
            </div>
        `;
    }
});