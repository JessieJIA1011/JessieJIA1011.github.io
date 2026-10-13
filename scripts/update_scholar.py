"""Update validated public Google Scholar totals; leave the cache intact on failure."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

URL = 'https://scholar.google.com/citations?user=MKyB5TQAAAAJ&hl=en'
TARGET = Path(__file__).resolve().parents[1] / 'data/scholar.json'


def parse_metrics(html: str) -> dict:
    table = re.search(r'<table\b[^>]*id="gsc_rsb_st"[^>]*>(.*?)</table>', html, re.S)
    if not table:
        raise ValueError('Scholar metrics table unavailable; retaining previous data')
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table[1], re.S)
    result = {}
    for label, key in [('Citations', 'citations'), ('h-index', 'h_index')]:
        row = next((row for row in rows if re.search(r'>' + re.escape(label) + r'</a>', row)), '')
        cells = re.findall(r'<td[^>]*class="gsc_rsb_std"[^>]*>\s*([\d,]+)\s*</td>', row)
        if len(cells) != 2:
            raise ValueError(f'Invalid {label} row; retaining previous data')
        result[key] = int(cells[0].replace(',', ''))
    if not (result['citations'] > 0 and 0 < result['h_index'] <= result['citations']):
        raise ValueError('Invalid metrics; retaining previous data')
    return result


def main() -> None:
    request = Request(URL, headers={'User-Agent': 'AcademicProfileMetrics/1.0'})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode('utf-8', errors='replace')
    data = parse_metrics(html)
    data.update(profile_id='MKyB5TQAAAAJ', source='Google Scholar', updated_at=datetime.now(timezone.utc).isoformat())
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    temp = TARGET.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    temp.replace(TARGET)
    print(f"Updated: {data['citations']} citations, h-index {data['h_index']}")


if __name__ == '__main__':
    main()
