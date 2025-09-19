# SupabaseAPI

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)  [![Supabase](https://img.shields.io/badge/backend-Supabase-3ECF8E.svg)](https://supabase.com/)

---

## Requirements

- Python **3.11.x** (recommended)  
- Virtual environment (`venv`)  

---

## Setup

Clone the repository:

```bash
git clone https://github.com/MantequillaCraft/SupabaseAPI.git
cd SupabaseAPI
```

### Create virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

Run the API locally (example with FastAPI + Uvicorn):

```bash
uvicorn src.main:app --reload
```

Then open in browser:
```
http://127.0.0.1:8000
```

---

## Notes
- Always activate the virtual environment before running the project.  
- Dependencies are listed in `requirements.txt`.  
- Recommended to use Python 3.11.x for best compatibility.   
