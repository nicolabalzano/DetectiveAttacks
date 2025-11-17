# Vuln Score Lite

A simplified vulnerability scoring service that stores only CVE IDs and fetches full data from `cvwelib` on demand.

## Features

- **Minimal Storage**: Only CVE IDs are stored in history
- **Real-time Data**: Fetches fresh CVE data from cvwelib for each request
- **Multiple Scoring Modes**: 
  - Mode 0: Base score (simple average)
  - Mode 1: Impact-weighted score
  - Mode 2: Exploitability-weighted score
  - Mode 3: Severity-weighted score
  - Mode 4: CWE-count weighted score

## Architecture

```
vuln_score_lite/
├── app.py                      # Flask application
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── controller/
│   ├── DashboardController.py # Dashboard logic
│   └── HistoryController.py   # History management
├── model/
│   ├── Database.py            # JSON file database (CVE IDs)
│   ├── ScoreHistory.py        # Score history database
│   └── files/
│       ├── history.json       # CVE ID storage
│       └── score_history.json # Score calculations with timestamps
└── utils/
    ├── CVEHelper.py           # CVE data parsing
    ├── CVELibClient.py        # cvwelib API client
    └── ScoreCalculator.py     # Score calculation logic
```

## API Endpoints

### POST /api/addhistory
Add a single CVE to history

**Request:**
```json
{
  "cveId": "CVE-2024-12345"
}
```

**Response:**
```json
{
  "success": true,
  "message": "CVE-2024-12345 added successfully"
}
```

### GET /api/getdashboard
Get all CVEs and dashboard data

**Response:**
```json
{
  "cveList": [
    {
      "id": "CVE-2024-12345",
      "description": "...",
      "baseScore": 7.5,
      "impactScore": 5.9,
      "exploitabilityScore": 3.9,
      "severity": "HIGH",
      "cwes": ["CWE-79"],
      "published": "2024-01-15T..."
    }
  ],
  "cveCount": 1,
  "severityCounts": {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 0,
    "LOW": 0,
    "NONE": 0
  },
  "metadata": {
    "cveCount": 1,
    "createdAt": "2025-11-14T...",
    "updatedAt": "2025-11-14T..."
  }
}
```

### POST /api/updatedashboard
Calculate score with optional CVE exclusions

**Request:**
```json
{
  "list": ["CVE-2024-99999"],
  "mode": 1
}
```

**Response:**
```json
{
  "newScore": 7.52,
  "checkedIds": ["CVE-2024-99999"]
}
```

### POST /api/calculate-all-scores
Calculate all 5 score modes at once and save to history

**Request:**
```json
{
  "list": []  // Optional: CVEs to exclude
}
```

**Response:**
```json
{
  "success": true,
  "scores": {
    "0": 6.5,
    "1": 7.2,
    "2": 6.8,
    "3": 7.5,
    "4": 6.9
  },
  "message": "All scores calculated and saved to history"
}
```

### GET /api/score-history
Get score calculation history with timestamps

**Query Parameters:**
- `limit` (optional): Maximum number of entries to return

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "timestamp": "2025-11-14T15:30:00.123Z",
      "scores": {
        "0": 6.5,
        "1": 7.2,
        "2": 6.8,
        "3": 7.5,
        "4": 6.9
      },
      "excludedCves": []
    }
  ],
  "count": 1
}
```

## Running with Docker

The service is designed to run in Docker and is configured to work with the existing DetectiveAttacks docker-compose setup.

**Port:** 5005

**Dependencies:**
- `cvwelib` service (for CVE/CWE data)

## Differences from vuln_score

1. **Storage**: Only CVE IDs stored (not full CVE objects)
2. **No asset tracking**: Simplified to focus on CVE scoring
3. **No relationship queries**: Does not fetch related CVEs
4. **Single CVE addition**: `/api/addhistory` adds only the specified CVE
5. **Real-time data**: Always fetches fresh data from cvwelib

## Configuration

Environment variables can be set in docker-compose.yml:

- `CVWELIB_URL`: URL of cvwelib service (default: http://cvwelib:5001)
- `FLASK_ENV`: Flask environment (default: production)
