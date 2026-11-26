# CampusCompass — Bennett University Edition

A responsive student-facing campus companion with a live public-news fetcher, interactive map, location permission button, official campus site-plan link, and campus quick links.

## Run on Windows
1. Install Python 3.9+.
2. Extract this folder.
3. Open PowerShell in the extracted `CampusCompass_Full` folder.
4. Run: `python server.py`
5. Open: `http://localhost:8000`

## Run on macOS/Linux
Run `python3 server.py`, then open `http://localhost:8000`.

## What's functional
- `/api/news` fetches Bennett University's public Media Centre and BU in the News pages on demand. The front end supports refresh, text search and source filtering.
- Interactive OpenStreetMap view centred on Bennett University.
- Browser geolocation: asks permission and shows your current position on the map.
- Official Bennett campus land-use map linked as a PDF (published within Bennett's green-campus policy document).
- Campus directory quick links.

## Important limitations / setup notes
- The university's published site plan is available as a PDF. The app links to the complete official plan and lists the labels visible on it. It does not claim to know precise GPS coordinates for every building or room.
- The public Media Centre feed is scraped server-side from Bennett's website. If Bennett changes its page markup, blocks automated requests, or is temporarily offline, the feed may be empty until the parser is updated. It does not invent news as a fallback.
- Internet is required for live news, map tiles, Leaflet CDN and Google Fonts.
- Browser geolocation generally requires `localhost` or HTTPS and user permission.
- No official university API, student login, timetable, internal noticeboard, or private campus system is connected.
- This is an independent student project, not an official Bennett University product. Confirm urgent announcements with official university channels.

## Data sources
- Bennett Media Centre: https://www.bennett.edu.in/media-center/
- Bennett BU in the News: https://www.bennett.edu.in/media-center/bu-in-news/
- Official campus land-use map PDF: https://www.bennett.edu.in/wp-content/uploads/2024/05/7.1.5_Policy.pdf (campus map appears on page 13)
- Campus reference coordinate used for map centring: 28.451082, 77.583973, documented in Bennett's published green-campus policy photo metadata.
