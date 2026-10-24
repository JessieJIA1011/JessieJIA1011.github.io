(() => {
  const url = 'https://raw.githubusercontent.com/JessieJIA1011/JessieJIA1011.github.io/main/data/scholar.json';
  async function update() {
    try {
      const response = await fetch(`${url}?refresh=${Math.floor(Date.now() / 60000)}`, {cache: 'no-store'});
      if (!response.ok) return;
      const data = await response.json();
      const date = new Date(data.updated_at);
      if (data.profile_id !== 'MKyB5TQAAAAJ' || data.source !== 'Google Scholar' ||
          !Number.isInteger(data.citations) || data.citations <= 0 ||
          !Number.isInteger(data.h_index) || data.h_index <= 0 || data.h_index > data.citations ||
          !Number.isFinite(date.getTime())) return;
      const values = document.querySelectorAll('.citation-metrics .metric-value');
      if (values.length !== 2) return;
      const panel = document.querySelector('.citation-metrics');
      const displayedAt = Date.parse(panel.dataset.updatedAt || '');
      if (Number.isFinite(displayedAt) && date.getTime() < displayedAt) return;
      panel.dataset.updatedAt = data.updated_at;
      values[0].textContent = data.citations.toLocaleString('en-US');
      values[1].textContent = String(data.h_index);
      document.querySelector('.citation-metrics').setAttribute('aria-label', 'Google Scholar citation metrics');
      const formatted = date.toLocaleDateString('en-GB', {day:'numeric', month:'long', year:'numeric', timeZone:'Asia/Hong_Kong'});
      document.querySelector('.metrics-source').textContent = `Updated ${formatted} · Source: Google Scholar`;
    } catch (_) {
      // Keep the last published snapshot if the data request fails.
    }
  }
  update();
})();
