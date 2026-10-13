# Gmail-Style NPTEL Email Demo (Educational UI Project)

An educational college project demonstrating a responsive Gmail-inspired email dashboard with an NPTEL examination hall-ticket notification sample email and PDF attachment download/preview integration.

> **Disclaimer:** This application is an educational UI demonstration. All emails displayed are clearly labeled as **DEMO / SAMPLE EMAIL** records.

---

## Project Structure

- [`index.html`](index.html) — Main Gmail-inspired dashboard UI (Inbox, Starred, Sent, Drafts, Trash, Search, Compose, and Full Email Reading Screen).
- [`styles.css`](styles.css) — Responsive stylesheet supporting desktop browsers and Android mobile browsers.
- [`app.js`](app.js) — Frontend logic for folder navigation, search filtering, reply/forward actions, inline PDF preview, and Hall Ticket download handling.
- [`server.py`](server.py) — Zero-dependency Python HTTP backend providing static file serving, `/api/health`, and `/api/download-hallticket`.
- `NOC26CS93S370700875.pdf` — Unmodified uploaded Hall Ticket PDF for **Pichika Venkateswarlu Jyoshika**.

---

## Extracted Candidate Details (From `NOC26CS93S370700875.pdf`)

| Field | Value |
| :--- | :--- |
| **Candidate Name** | Pichika Venkateswarlu Jyoshika |
| **Roll No** | `NOC26CS93S370700875` |
| **Course** | Programming with Generative AI (`SEM2NOC26: CS93`) |
| **Exam Date** | Friday, 16 October 2026 |
| **Session** | FN (Morning Session — Reporting: 08:00 am, Gate Closure: 09:30 am, Exam: 09:00 am) |
| **Seating Number** | 875 |
| **Exam Centre** | iON Digital Zone iDZ Zoo Park Tirupathi |
| **Centre Address** | Zoo Park Road, CherloPalli Village, Chittoor District, Tirupathi, Andhra Pradesh, India – 517503 |

---

## Running the Project

### Option 1: Run with the Python Backend Server (Recommended for Desktop & Android Mobile)

```powershell
python server.py
```

- **Desktop Browser:** Open `http://localhost:8000`
- **Android Mobile Browser (same Wi-Fi/LAN):** Open the `Android / LAN URL` printed in the terminal (e.g., `http://192.168.x.x:8000`)

### Option 2: Open Directly in Browser

Double-click `index.html` to open it directly in any desktop browser. The relative link `./NOC26CS93S370700875.pdf` is pre-configured to download or open the PDF from the same folder.

---

## Configuring or Replacing the Hall Ticket PDF

1. Place your PDF file in the project root directory (`c:\Users\pichi\Downloads\New folder\gmail\`).
2. If using a different filename, update `HALL_TICKET_CONFIG.pdfFileName` and `HALL_TICKET_CONFIG.pdfRelativeUrl` at the top of [`app.js`](app.js), and `PDF_FILENAME` in [`server.py`](server.py).
