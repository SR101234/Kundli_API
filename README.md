# Complete Vedic & KP Kundli Calculation Engine

A production-grade, highly precise Vedic Astrology (Jyotish) and Krishnamurti Paddhati (KP) calculation engine powered by **Swiss Ephemeris** with a **FastAPI (Python)** backend and an interactive **React** frontend.

---

## 🏛️ Architecture Recommendation: Python vs. NodeJS Backend

When building a serious astrological calculation engine, **Python is unequivocally superior to Node.js for the calculation backend**, while **React is the gold standard for the frontend**:

| Factor | Python (FastAPI + Swiss Ephemeris) | Node.js (Express / NestJS) | Verdict |
| :--- | :--- | :--- | :--- |
| **Astronomical Accuracy** | Native C bindings via `pyswisseph` compiled cleanly across platforms. | Brittle `node-gyp` C++ bindings (`swisseph`) that frequently break on Windows, memory leaks during long runs. | **Python Wins Decisively** |
| **Rules Engine Complexity** | Clean dataclasses, pattern matching, matrix calculations (SAV 337 points, KP 249 sub-divisions). | Clunky object graphs, requires custom math libraries for trigonometric ephemeris interpolations. | **Python Wins** |
| **Testing & Golden Fixtures** | Built-in `pytest` fixtures for testing seconds-of-arc boundary precision and leap years. | `jest` / `vitest` works, but lacks astronomical testing suites. | **Python Wins** |
| **API Performance** | FastAPI (ASGI / Uvicorn) delivers high-throughput async JSON responses with automatic OpenAPI docs. | Fast, but lacks Pydantic's automated structural schema validation. | **Python Wins** |
| **User Interface** | Server-rendered templates are static and clumsy for charts. | **React + Vite** provides interactive SVGs, real-time chart switching (North/South Indian), and fluid tab navigation. | **React Wins for Frontend** |

> **Conclusion**: The best architecture is a **Python (FastAPI) calculation backend** + **React (Vite) frontend**.

---

## 📦 System Architecture & Modules

```
kundli/
├── astronomy/           # Swiss Ephemeris wrapper, Julian Day, Planetary Longitudes, Houses, Ayanamsa
│   ├── ayanamsa.py      # Lahiri, KP, Raman, Yukteshwar, Fagan-Bradley, Sayana
│   ├── coordinates.py   # Geographic coordinates, IANA timezones, birth input models
│   ├── ephemeris.py     # Swiss Ephemeris interface
│   ├── houses.py        # Placidus, Whole Sign, Equal, Sripati house cusps & ascendant
│   └── planets.py       # Sun through Ketu, retrograde detection, speed, combustion
├── core/                # Vedic astrological foundational rules
│   ├── zodiac.py        # 12 Rashis, lords, elements, mobility, varna, vashya
│   ├── nakshatra.py     # 27 Nakshatras, 108 Padas, Gana, Nadi, Yoni, Rajju
│   ├── dignity.py       # Exaltation, debilitation, Moolatrikona, Panchadha Maitri
│   ├── panchang.py      # Tithi, Vara, Nakshatra, Yoga, Karana, Sunrise/Sunset
│   ├── aspects.py       # Vedic Drishti (Mars 4/7/8, Jupiter 5/7/9, Saturn 3/7/10)
│   └── house_lords.py   # Kendras, Trikonas, Dusthanas, Upachayas, Marakas
├── charts/              # Chart generation and renderers
│   ├── d1.py            # Janma Kundli, Chandra Kundli, Surya Kundli
│   ├── divisional.py    # Shodashavargas (D1 to D60: D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60)
│   └── chart_renderer.py # North Indian Diamond & South Indian Square SVG renderers
├── kp/                  # Krishnamurti Paddhati (KP) Engine
│   ├── sublords.py      # KP 249 sub-division algorithm & Sub-Sub Lords
│   ├── cusps.py         # Placidus 12 cusps with Sign/Star/Sub/Sub-sub lords
│   ├── significators.py # 4-Step KP Significators (Levels 1 to 4)
│   └── ruling_planets.py# Ruling Planets (RP) at birth
├── ashtakavarga/        # Ashtakavarga Engine
│   ├── bav.py           # Bhinnashtakavarga for 7 planets from 8 reference points
│   ├── sav.py           # Sarvashtakavarga 337-point matrix & sign strength
│   ├── reductions.py    # Trikona Shodhana, Ekadhipatya Shodhana, Shodhya Pinda
│   └── kakshya.py       # 8 Kakshya divisions (3°45')
├── dasha/               # Dasha Timeline Engine
│   ├── vimshottari.py   # 120-year Vimshottari (Maha, Antar, Pratyantar, Sookshma)
│   └── yogini.py        # 36-year Yogini Dasha
├── yogas/               # Auspicious Yogas Rule Engine
│   └── detection_engine.py # Gajakesari, Budhaditya, Panch Mahapurusha, Raj Yoga, Vipreet Raj, Neech Bhanga
├── doshas/              # Inauspicious Doshas Rule Engine
│   └── detection_engine.py # Manglik (with cancellations), Kaal Sarp (12 types), Pitra, Guru Chandal, Kemadruma, Gand Mool
├── matching/            # Marriage Compatibility Engine
│   ├── ashtakoota.py    # 36-Gun Milan (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi)
│   └── compatibility.py # Full matching with Manglik neutralization
├── transits/            # Transit (Gochar) & Sade Sati Engine
│   ├── gochar.py        # Current transits vs natal Moon & Ascendant
│   └── sade_sati.py     # Saturn Sade Sati (Rising, Peak, Setting) & Dhaiya
├── strengths/           # Planetary Strengths
│   └── shadbala.py      # Six-fold Shadbala (Sthana, Dig, Kala, Cheshta, Naisargika, Drik)
└── api/                 # FastAPI REST API
    ├── routes/          # Modular endpoints for each calculation subsystem
    └── main.py          # CORS, routing, static frontend mounting
```

---

## 🛡️ Admin Panel & 10 Kundli Check Limit

### 1. User Contact Collection & 10 Check Quota (Pop-up Modal Flow)
- **Pop-up Prompt on Click**: When a user clicks **"✨ Generate Vedic & KP Kundli"**, a sleek modal pop-up appears prompting them for their contact details (**Full Name**, **Email Address**, and **Mobile Number**) before executing the chart calculation.
- **Quota Tracking**: Every user is automatically allocated a limit of **10 free Kundli checks**.
- **Pre-fill & Persistence**: Returning users have their contact details safely cached in local storage and pre-filled in the pop-up for immediate 1-click confirmation.
- **Remaining Checks**: Displayed in real-time in the header and form (e.g., `8 of 10 Checks Remaining`).
- **Limit Enforcement**: Once a user reaches 10 checks, subsequent calculation requests are blocked with an HTTP 403 error alerting them that their limit has been reached. Admins can reset or increase limits at any time.

### 2. Full Data Persistence in MongoDB (`kundli_db`)
Every Kundli calculation records in MongoDB collections (`users` and `kundli_records`):
- **User Contact Info**: User Full Name, Email Address (indexed & unique), Mobile Number
- **Seeker Birth Info**: Seeker / Native Name, Birth Date, Exact Time, Timezone, Latitude, Longitude, Ayanamsa, House System
- **Astrological Results**: Calculated Ascendant sign, Moon sign, Moon Nakshatra & Pada
- **Timestamp**: Exact local creation timestamp (`YYYY-MM-DD HH:MM:SS`)
- **Indexes**: Fast indexing on `email`, `mobile`, `user_id`, and `created_at` for high concurrency.

### 3. Interactive Admin Portal (`/api/admin`)
- Accessible via the **"🛡️ Admin Panel"** button in the header.
- **Default Passcode**: `admin@kundli2026` (configurable via `ADMIN_KEY` environment variable).
- **Features**:
  - **KPI Dashboard**: Total registered users, total Kundlis generated, checks used today, users who hit the 10 limit.
  - **User Management**: View all users, search by name/email/phone, view visual quota progress bars, and perform a **1-click Reset** or custom limit expansion (e.g., extend to 20, 50, etc.).
  - **Birth Information Audit Log**: Complete history of every birth chart generated with user contact info, native coordinates, and timestamps.
  - **Export to CSV**: Instant 1-click export of all user leads and birth data records for CRM or team analysis.

---

## 🚀 Running the Project

### 1. Start the Backend API (FastAPI)
The backend runs with Python 3.12+ and includes the built React frontend:

```powershell
# From project root:
.\.venv\Scripts\python.exe run_server.py
```
- Web Application: **http://127.0.0.1:8000**
- Interactive Swagger / OpenAPI Docs: **http://127.0.0.1:8000/docs**

### 2. Frontend Development Server (Optional)
If you want live hot-reloading for React:

```powershell
cd frontend
npm run dev
```
Open **http://localhost:3000** in your browser.

---

## 🌐 Hostinger VPS KVM 2 Production Deployment

See [DEPLOYMENT_GUIDE.md](file:///d:/Junk/Kundli-API/DEPLOYMENT_GUIDE.md) for full instructions.

### 1-Click Automated Deployment:
```bash
# On your Hostinger VPS:
git clone <repo-url> /opt/Kundli-API
cd /opt/Kundli-API
chmod +x deploy.sh
sudo ./deploy.sh
```
This automatically sets up **Docker**, boots **MongoDB 7.0**, builds the **FastAPI + Swiss Ephemeris** container, and launches the application at `http://YOUR_SERVER_IP:8000`.

---

## 🧪 Running the Test Suite

```powershell
.\.venv\Scripts\pytest.exe -v
```
All 15 automated verification tests validate:
- Exact planetary longitudes, Ascendant, and Panchang for the reference chart (`2001-08-15 14:35:00, Agra, India`)
- Ashtakavarga traditional 337-point total conservation
- KP 249 sub-division boundary transitions
- 36-Gun Milan Ashtakoota score calculations
- Vimshottari Dasha balance and running hierarchy
- 10-check limit enforcement and automatic user registration
- Admin panel security, user quota resets, custom limit updates, and search queries
- All REST API endpoints (`/generate`, `/basic`, `/kp`, `/ashtakavarga`, `/divisional`, `/matching`, etc.)
