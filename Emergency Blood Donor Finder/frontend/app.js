const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : 'https://your-railway-app.up.railway.app';

const donorList = document.getElementById('donorList');
const searchForm = document.getElementById('searchForm');
const bloodGroupInput = document.getElementById('bloodGroup');
const cityInput = document.getElementById('city');

async function loadDonors() {
  const params = new URLSearchParams();
  const bloodGroup = bloodGroupInput.value.trim();
  const city = cityInput.value.trim();

  if (bloodGroup) params.append('blood_group', bloodGroup);
  if (city) params.append('city', city);

  const url = `${API_BASE_URL}/api/donors?${params.toString()}`;

  try {
    const response = await fetch(url);
    const result = await response.json();
    const donors = result.donors || [];

    donorList.innerHTML = donors.length
      ? donors.map(donor => `
        <article class="donor-card">
          <h4>${donor.name}</h4>
          <span class="badge">${donor.blood_group}</span>
          <p><strong>City:</strong> ${donor.city}</p>
          <p><strong>Status:</strong> ${donor.available ? 'Available' : 'Not Available'}</p>
        </article>
      `).join('')
      : `<p>No donors found for the selected filters.</p>`;
  } catch (error) {
    donorList.innerHTML = '<p>Unable to load donors. Check the backend URL.</p>';
    console.error(error);
  }
}

searchForm.addEventListener('submit', (event) => {
  event.preventDefault();
  loadDonors();
});

loadDonors();
