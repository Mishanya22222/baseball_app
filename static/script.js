// Fetch years on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchYears();
    
    // Add change listener to year selector
    document.getElementById('yearSelect').addEventListener('change', (e) => {
        if (e.target.value) {
            handleYearSelect(e.target.value);
        }
    });
});

// Fetch years from the backend
async function fetchYears() {
    try {
        const response = await fetch('/years');
        if (!response.ok) throw new Error('Failed to fetch years');
        
        const years = await response.json();
        populateYearSelector(years);
    } catch (error) {
        console.error('Error fetching years:', error);
        updateErrorMessage('Failed to load years. Please try again.');
    }
}

// Populate the year selector dropdown
function populateYearSelector(years) {
    const select = document.getElementById('yearSelect');
    select.innerHTML = '<option value="">Choose a year...</option>';
    
    // Sort years in descending order (newest first)
    const sortedYears = years.sort((a, b) => b - a);
    
    sortedYears.forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        select.appendChild(option);
    });
}

// Handle year selection
async function handleYearSelect(year) {
    showSpinner(true);
    try {
        // You can add more functionality here to fetch data for the selected year
        updateDataContainer(`Selected year: ${year}`);
    } catch (error) {
        console.error('Error selecting year:', error);
        updateErrorMessage('Failed to load data for the selected year.');
    } finally {
        showSpinner(false);
    }
}

// Show/hide loading spinner
function showSpinner(show) {
    const spinner = document.getElementById('loadingSpinner');
    spinner.style.display = show ? 'flex' : 'none';
}

// Update data container
function updateDataContainer(content) {
    const container = document.getElementById('dataContainer');
    container.innerHTML = `<p class="data-text">${content}</p>`;
}

// Update error message
function updateErrorMessage(message) {
    const container = document.getElementById('dataContainer');
    container.innerHTML = `<p class="error-message">${message}</p>`;
}