---
title: Corespace API
emoji: ⚡
colorFrom: indigo
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
---

# corespace API Server

A standalone, high-performance FastAPI server for **corespace** that authenticates, solves CAPTCHAs, and scrapes student academic data from both **SRM Student Portal** (`sp.srmist.edu.in`) and **SRM Academia** (`academia.srmist.edu.in`).

---

## Features

- **Dual-Portal Support**:
  - **SRM Student Portal (`sp.srmist.edu.in`)**: Active portal with complete anti-bot telemetry, dynamic nonce extraction, and auto-handled security parameters.
  - **SRM Academia Portal (`academia.srmist.edu.in`)**: Legacy Zoho portal with ghost session termination and data decoding.
- **Built-in In-Process CAPTCHA Solver**:
  - Uses an integrated ONNX CRNN deep learning model (`model/captcha_crnn.onnx`) via `onnxruntime`.
  - Automatically predicts and solves SRM Student Portal CAPTCHAs in ~5ms without needing any external OCR microservices.
- **Complete Academic Data Scraping**:
  - **Attendance**: Subject-wise attendance percentages, hours conducted, hours absent, slots, and faculty.
  - **Marks**: Test-wise assessments (cycle tests, internal exams, lab assessments, component scores).
  - **Timetable**: Slot matrix, day-order mapping, room numbers, and schedules.
  - **Profile**: Student name, registration number, department, program, semester, batch.
- **RESTful Endpoints & CORS**: Fully enabled CORS for easy integration with any React, React Native, Flutter, Swift, or web/mobile frontend.

---

## Directory Structure

```
server/
├── core/
│   ├── academia_client.py       # Legacy Academia portal network client
│   ├── portal_client.py         # SRM Student Portal network client (telemetry, anti-bot, login)
│   ├── session.py               # Academia session & ghost session terminator
│   ├── decoder.py               # HTML decoder & sanitizer
│   └── config.py                # Portal endpoints & headers
├── services/
│   ├── portal_attendance_service.py # Parses Student Portal attendance table
│   ├── portal_marks_service.py      # Parses Student Portal marks & inner modals
│   ├── portal_timetable_service.py  # Parses Student Portal timetable & slot map
│   ├── portal_profile_service.py    # Parses Student Portal personal details
│   ├── attendance_service.py        # Parses Academia attendance
│   ├── marks_service.py             # Parses Academia marks
│   ├── timetable_service.py         # Parses Academia timetable
│   ├── profile_service.py           # Parses Academia profile
│   └── calendar_service.py          # Parses Academic planner
├── models/
│   └── schemas.py               # Pydantic request & response schemas
├── model/
│   └── captcha_crnn.onnx        # ONNX deep learning model for portal CAPTCHA
├── utils/
│   ├── captcha_solver.py        # In-process ONNX CAPTCHA inference runner
│   └── text.py                  # Text parsing helpers
├── tests/
│   └── verify.py                # Offline parser verification tests
├── main.py                      # FastAPI application & API routes
├── requirements.txt             # Python dependencies
└── .env                         # Server environment variables
```

---

## Setup & Running

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration (`.env`)

```env
ENV=development
PORT=8000
HOST=0.0.0.0
```

### 3. Start the Server

```bash
uvicorn main:app --reload --port 8000
```

The interactive Swagger API documentation will be available at:
`http://localhost:8000/docs`

---

## API Endpoints

### 1. SRM Student Portal (`sp.srmist.edu.in`)

#### `POST /portal/login`
Logs into the student portal and returns cookies along with all scraped academic data (Attendance, Marks, Timetable, Profile).
- **Body**:
  ```json
  {
    "username": "netid_or_email",
    "password": "your_password"
  }
  ```
  *(Captcha is auto-solved by default using the built-in ONNX model. You can also pass `"captcha": "xyz12"` manually if desired).*

#### `POST /portal/refresh`
Refreshes and scrapes the latest academic data using session cookies without re-authenticating.
- **Body**:
  ```json
  {
    "cookies": { ... },
    "username": "netid_or_email",
    "password": "your_password"
  }
  ```

#### `POST /portal/captcha`
Fetches a fresh CAPTCHA image and nonce (useful if building a manual CAPTCHA fallback UI).

---

### 2. SRM Academia Portal (`academia.srmist.edu.in`)

#### `POST /login`
Logs in to Academia and retrieves attendance, marks, profile, and timetable.
- **Body**:
  ```json
  {
    "username": "email@srmist.edu.in",
    "password": "your_password",
    "captcha": "optional_if_prompted",
    "cdigest": "optional_if_prompted"
  }
  ```

#### `POST /refresh`
Refreshes Academia data using active session cookies.

---

### 3. Utility Endpoints

#### `POST /captcha/solve`
Directly solves a base64-encoded CAPTCHA image using the built-in model.
- **Body**: `{"image": "data:image/png;base64,..."}`

#### `GET /version`
Health check endpoint returning server status.
