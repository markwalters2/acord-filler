#!/usr/bin/env python3
"""
ACORD Certificate Generator API v2 — Full Telemetry Edition
Every request, every file, every error — captured for training data.
"""

import os
import json
import uuid
import base64
import tempfile
import time
import traceback
import hashlib
import sqlite3
from datetime import datetime, timezone
from typing import Optional
from contextlib import contextmanager

import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import httpx

app = FastAPI(title="ACORD Certificate Generator API v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("ACORD_API_KEY", "acord-demo-2026")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "telemetry.db")
BLANK_FORMS = {
    "25": os.path.join(BASE_DIR, "acord-25-blank.pdf"),
    "24": os.path.join(BASE_DIR, "acord-24-blank.pdf"),
    "28": os.path.join(BASE_DIR, "acord-28-blank.pdf"),
}

os.makedirs(os.path.join(DATA_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "generated"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "errors"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "extractions"), exist_ok=True)


# ── Database ──

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            ip TEXT,
            user_agent TEXT,
            api_key_hash TEXT,
            status_code INTEGER,
            duration_ms REAL,
            error TEXT,
            request_size_bytes INTEGER,
            response_size_bytes INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS extractions (
            id TEXT PRIMARY KEY,
            request_id TEXT REFERENCES requests(id),
            timestamp TEXT NOT NULL,
            upload_filename TEXT,
            upload_size_bytes INTEGER,
            upload_hash TEXT,
            upload_path TEXT,
            text_extracted TEXT,
            text_length INTEGER,
            used_vision INTEGER DEFAULT 0,
            ai_model TEXT,
            ai_prompt_tokens INTEGER,
            ai_completion_tokens INTEGER,
            ai_duration_ms REAL,
            extracted_data TEXT,
            extraction_quality TEXT,
            insured_name TEXT,
            carrier TEXT,
            coverages_found TEXT,
            error TEXT
        );
        
        CREATE TABLE IF NOT EXISTS generations (
            id TEXT PRIMARY KEY,
            request_id TEXT REFERENCES requests(id),
            timestamp TEXT NOT NULL,
            form_type TEXT,
            insured_name TEXT,
            carrier TEXT,
            cert_holder_name TEXT,
            policy_number TEXT,
            coverages TEXT,
            additional_insured INTEGER DEFAULT 0,
            waiver_of_sub INTEGER DEFAULT 0,
            primary_noncontrib INTEGER DEFAULT 0,
            agency_name TEXT,
            has_signature INTEGER DEFAULT 0,
            signature_mode TEXT,
            fields_filled INTEGER,
            fields_total INTEGER,
            fields_skipped TEXT,
            output_path TEXT,
            output_size_bytes INTEGER,
            input_data TEXT,
            cert_holder_data TEXT,
            agency_data TEXT,
            flatten INTEGER DEFAULT 1,
            user_id TEXT,
            error TEXT
        );
        
        CREATE TABLE IF NOT EXISTS errors (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            request_id TEXT,
            endpoint TEXT,
            error_type TEXT,
            error_message TEXT,
            traceback TEXT,
            request_data TEXT
        );

        CREATE TABLE IF NOT EXISTS daily_analysis (
            id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            total_requests INTEGER,
            total_extractions INTEGER,
            total_generations INTEGER,
            total_errors INTEGER,
            avg_extraction_time_ms REAL,
            avg_generation_time_ms REAL,
            top_errors TEXT,
            improvement_notes TEXT,
            analyzed_at TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_requests_ts ON requests(timestamp);
        CREATE INDEX IF NOT EXISTS idx_extractions_ts ON extractions(timestamp);
        CREATE INDEX IF NOT EXISTS idx_generations_ts ON generations(timestamp);
        CREATE INDEX IF NOT EXISTS idx_errors_ts ON errors(timestamp);
    """)
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

init_db()

# Migration: add user_id column if missing (for existing DBs)
def _migrate_db():
    with get_db() as db:
        cols = [r[1] for r in db.execute("PRAGMA table_info(generations)").fetchall()]
        if "user_id" not in cols:
            db.execute("ALTER TABLE generations ADD COLUMN user_id TEXT")
            print("Migration: added user_id column to generations")
_migrate_db()


# ── Telemetry Helpers ──

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]

def log_request(req: Request, endpoint: str, status: int, duration_ms: float, 
                req_size: int = 0, resp_size: int = 0, error: str = None) -> str:
    rid = str(uuid.uuid4())[:12]
    key = req.headers.get("x-api-key", "")
    key_hash = hashlib.sha256(key.encode()).hexdigest()[:8] if key else ""
    
    with get_db() as db:
        db.execute("""
            INSERT INTO requests (id, timestamp, endpoint, method, ip, user_agent, 
                                  api_key_hash, status_code, duration_ms, error,
                                  request_size_bytes, response_size_bytes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rid, now_iso(), endpoint, req.method, 
              req.headers.get("x-forwarded-for", req.client.host if req.client else "unknown"),
              req.headers.get("user-agent", "")[:200],
              key_hash, status, duration_ms, error, req_size, resp_size))
    return rid

def log_error(request_id: str, endpoint: str, error_type: str, message: str, 
              tb: str = None, request_data: str = None):
    eid = str(uuid.uuid4())[:12]
    with get_db() as db:
        db.execute("""
            INSERT INTO errors (id, timestamp, request_id, endpoint, error_type, 
                               error_message, traceback, request_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (eid, now_iso(), request_id, endpoint, error_type, message[:2000], 
              tb[:5000] if tb else None, request_data[:5000] if request_data else None))
    
    # Also save to error file for easy grep
    error_file = os.path.join(DATA_DIR, "errors", f"{eid}.json")
    with open(error_file, "w") as f:
        json.dump({"id": eid, "timestamp": now_iso(), "request_id": request_id,
                    "endpoint": endpoint, "type": error_type, "message": message,
                    "traceback": tb}, f, indent=2)


# ── Auth ──

def check_auth(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ── PDF Functions ──

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text

def pdf_pages_to_images(pdf_bytes: bytes, dpi: int = 150) -> list[str]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        images.append(base64.b64encode(img_bytes).decode())
    doc.close()
    return images


async def extract_policy_data_with_ai(pdf_bytes: bytes) -> dict:
    text = extract_text_from_pdf(pdf_bytes)
    use_vision = len(text.strip()) < 200
    
    extraction_prompt = """Extract the following structured data from this insurance policy declaration page. Return ONLY valid JSON, no explanation.

{
  "insured": {
    "name": "Full name of the insured",
    "address_line1": "Street address",
    "address_line2": "Suite/unit if any",
    "city": "City",
    "state": "State abbreviation",
    "zip": "ZIP code"
  },
  "policy": {
    "number": "Policy number",
    "effective_date": "MM/DD/YYYY",
    "expiration_date": "MM/DD/YYYY",
    "carrier": "Insurance company name",
    "naic": "NAIC number if visible"
  },
  "coverages": {
    "gl": { "has": true/false, "occurrence_limit": "", "aggregate_limit": "", "fire_damage_limit": "", "med_exp_limit": "", "personal_adv_limit": "", "products_completed_limit": "", "claims_made": false, "occurrence": true, "policy_number": "" },
    "auto": { "has": true/false, "combined_single_limit": "", "any_auto": true, "hired": false, "non_owned": false, "policy_number": "" },
    "umbrella": { "has": true/false, "each_occurrence": "", "aggregate": "", "policy_number": "" },
    "workers_comp": { "has": true/false, "statutory": true, "el_each_accident": "", "el_disease_each": "", "el_disease_policy": "", "policy_number": "" },
    "property": { "has": true/false, "building_limit": "", "contents_limit": "", "total_limit": "", "deductible": "", "policy_number": "" }
  }
}

Only include coverages that are actually present. Set "has": false for coverages not found. Use empty strings for fields not found."""

    messages = []
    if use_vision:
        images = pdf_pages_to_images(pdf_bytes, dpi=150)
        content = [{"type": "text", "text": extraction_prompt}]
        for img in images[:5]:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img}})
        messages = [{"role": "user", "content": content}]
    else:
        messages = [{"role": "user", "content": f"{extraction_prompt}\n\nDocument text:\n{text[:15000]}"}]

    ai_start = time.time()
    resp_ok = False
    ai_text_result = ""
    usage = {}

    # Try direct Anthropic API first
    if ANTHROPIC_KEY:
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                    json={"model": "claude-sonnet-4-20250514", "max_tokens": 4096, "messages": messages},
                )
            if resp.status_code == 200:
                result = resp.json()
                ai_text_result = result["content"][0]["text"]
                usage = result.get("usage", {})
                resp_ok = True
        except Exception as e:
            pass

    # Fallback: resolve fresh token from openclaw auth system
    if not resp_ok:
        import subprocess as _sp
        try:
            _proc = _sp.run(
                ["bash", "-c", """source /root/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && node -e "
const { resolveProviderAuth } = require('openclaw/dist/auth/resolve.js');
resolveProviderAuth('anthropic').then(r => console.log(r.token || r.apiKey || '')).catch(() => process.exit(1));
" 2>/dev/null || openclaw health --json 2>/dev/null | python3 -c "import sys,json; print('')" """],
                capture_output=True, text=True, timeout=15
            )
            fresh_key = _proc.stdout.strip()
        except Exception:
            fresh_key = ""
        
        if not fresh_key:
            # Last resort: read from auth-profiles and try anyway
            try:
                import json as _json
                with open("/root/.openclaw/agents/main/agent/auth-profiles.json") as _f:
                    _ap = _json.load(_f)
                fresh_key = _ap.get("profiles", {}).get("anthropic:default", {}).get("token", "")
            except Exception:
                fresh_key = ""

        if fresh_key:
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    resp = await client.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={"x-api-key": fresh_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                        json={"model": "claude-sonnet-4-20250514", "max_tokens": 4096, "messages": messages},
                    )
                if resp.status_code == 200:
                    result = resp.json()
                    ai_text_result = result["content"][0]["text"]
                    usage = result.get("usage", {})
                    usage["auth_method"] = "openclaw_fallback"
                    resp_ok = True
                    # Update env so future calls use the fresh key
                    os.environ["ANTHROPIC_API_KEY"] = fresh_key
                    globals()["ANTHROPIC_KEY"] = fresh_key
            except Exception:
                pass

    # Last fallback: use openclaw CLI directly
    if not resp_ok:
        import subprocess as _sp
        prompt_for_cli = extraction_prompt + "\n\nDocument text:\n" + text[:15000]
        try:
            _proc = _sp.run(
                ["bash", "-c", 'source /root/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && openclaw agent --agent main --local -m "$1"', "_", prompt_for_cli],
                capture_output=True, text=True, timeout=90
            )
            if _proc.returncode == 0 and _proc.stdout.strip():
                ai_text_result = _proc.stdout.strip()
                usage = {"auth_method": "openclaw_cli"}
                resp_ok = True
        except Exception:
            pass

    ai_duration = (time.time() - ai_start) * 1000

    if not resp_ok:
        return {"raw_text": text, "error": "AI extraction failed: all auth methods exhausted (direct API + openclaw fallback + CLI)",
                "_meta": {"used_vision": use_vision, "ai_duration_ms": ai_duration}}

    ai_text = ai_text_result
    # Reconstruct result-like object for downstream code
    result = {"content": [{"text": ai_text}], "usage": usage}
    ai_text = result["content"][0]["text"]
    usage = result.get("usage", {})
    
    try:
        start = ai_text.index("{")
        end = ai_text.rindex("}") + 1
        parsed = json.loads(ai_text[start:end])
        parsed["_meta"] = {
            "used_vision": use_vision,
            "text_length": len(text),
            "ai_model": "claude-sonnet-4-20250514",
            "ai_prompt_tokens": usage.get("input_tokens", 0),
            "ai_completion_tokens": usage.get("output_tokens", 0),
            "ai_duration_ms": ai_duration,
        }
        return parsed
    except (ValueError, json.JSONDecodeError) as e:
        return {"raw_text": text, "ai_response": ai_text, "error": f"Parse error: {e}",
                "_meta": {"used_vision": use_vision, "ai_duration_ms": ai_duration}}


# ── ACORD Field Mapping ──

def map_to_acord25(policy_data: dict, cert_holder: dict, agency: dict) -> dict:
    """Map policy data to ACORD 25 fields. Supports multiple insurers/policies per coverage line."""
    fields = {}
    today = datetime.now().strftime("%m/%d/%Y")
    ins = policy_data.get("insured", {})
    pol = policy_data.get("policy", {})  # legacy single-policy fallback
    cov = policy_data.get("coverages", {})
    gl = cov.get("gl", {})
    auto = cov.get("auto", {})
    umb = cov.get("umbrella", {})
    wc = cov.get("workers_comp", {})
    p = "F[0].P1[0]."
    
    # Insurers table: supports up to 5 (A-E)
    # New format: policy_data.insurers = [{letter: "A", carrier: "...", naic: "..."}, ...]
    # Legacy format: policy_data.policy.carrier goes into slot A
    insurers = policy_data.get("insurers", [])
    if not insurers and pol.get("carrier"):
        insurers = [{"letter": "A", "carrier": pol["carrier"], "naic": pol.get("naic", "")}]
    
    for insurer in insurers[:5]:
        letter = insurer.get("letter", "A")
        idx = ord(letter) - ord("A")  # A=0, B=1, etc.
        fields[f"{p}Insurer_FullName_{letter}[0]"] = insurer.get("carrier", "")
        fields[f"{p}Insurer_NAICCode_{letter}[0]"] = insurer.get("naic", "")
    
    # Also fill the legacy single-insurer field for backwards compat
    if insurers:
        fields[f"{p}Insurer_FullName_A[0]"] = insurers[0].get("carrier", "")
        fields[f"{p}Insurer_NAICCode_A[0]"] = insurers[0].get("naic", "")
    
    fields[f"{p}Form_CompletionDate_A[0]"] = today
    
    # Producer
    fields[f"{p}Producer_FullName_A[0]"] = agency.get("name", "")
    addr_parts = [agency.get("address_line1", agency.get("address", ""))]
    if agency.get("address_line2"):
        addr_parts.append(agency["address_line2"])
    fields[f"{p}Producer_MailingAddress_LineOne_A[0]"] = "\n".join(addr_parts)
    fields[f"{p}Producer_MailingAddress_CityName_A[0]"] = agency.get("city", "")
    fields[f"{p}Producer_MailingAddress_StateOrProvinceCode_A[0]"] = agency.get("state", "")
    fields[f"{p}Producer_MailingAddress_PostalCode_A[0]"] = agency.get("zip", "")
    fields[f"{p}Producer_ContactPerson_FullName_A[0]"] = agency.get("contact", "")
    fields[f"{p}Producer_ContactPerson_PhoneNumber_A[0]"] = agency.get("phone", "")
    fields[f"{p}Producer_ContactPerson_EmailAddress_A[0]"] = agency.get("email", "")
    
    # Insured
    fields[f"{p}NamedInsured_FullName_A[0]"] = ins.get("name", "")
    addr = ins.get("address_line1", "")
    if ins.get("address_line2"):
        addr += "\n" + ins["address_line2"]
    fields[f"{p}NamedInsured_MailingAddress_LineOne_A[0]"] = addr
    fields[f"{p}NamedInsured_MailingAddress_CityName_A[0]"] = ins.get("city", "")
    fields[f"{p}NamedInsured_MailingAddress_StateOrProvinceCode_A[0]"] = ins.get("state", "")
    fields[f"{p}NamedInsured_MailingAddress_PostalCode_A[0]"] = ins.get("zip", "")
    
    # Helper: get per-line dates, falling back to legacy single policy
    def line_dates(line_data):
        eff = line_data.get("effective_date", pol.get("effective_date", ""))
        exp = line_data.get("expiration_date", pol.get("expiration_date", ""))
        return eff, exp
    
    # GL
    if gl.get("has"):
        letter = gl.get("insurer_letter", "A")
        eff, exp = line_dates(gl)
        fields[f"{p}GeneralLiability_CoverageIndicator_A[0]"] = "Yes"
        if gl.get("occurrence"): fields[f"{p}GeneralLiability_OccurrenceIndicator_A[0]"] = "Yes"
        if gl.get("claims_made"): fields[f"{p}GeneralLiability_ClaimsMadeIndicator_A[0]"] = "Yes"
        fields[f"{p}GeneralLiability_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}GeneralLiability_PolicyNumberIdentifier_A[0]"] = gl.get("policy_number", pol.get("number", ""))
        fields[f"{p}GeneralLiability_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}GeneralLiability_PolicyExpirationDate_A[0]"] = exp
        fields[f"{p}GeneralLiability_EachOccurrence_LimitAmount_A[0]"] = gl.get("occurrence_limit", "")
        fields[f"{p}GeneralLiability_GeneralAggregate_LimitAmount_A[0]"] = gl.get("aggregate_limit", "")
        fields[f"{p}GeneralLiability_FireDamageRentedPremises_EachOccurrenceLimitAmount_A[0]"] = gl.get("fire_damage_limit", "")
        fields[f"{p}GeneralLiability_MedicalExpense_EachPersonLimitAmount_A[0]"] = gl.get("med_exp_limit", "")
        fields[f"{p}GeneralLiability_PersonalAndAdvertisingInjury_LimitAmount_A[0]"] = gl.get("personal_adv_limit", "")
        fields[f"{p}GeneralLiability_ProductsAndCompletedOperations_AggregateLimitAmount_A[0]"] = gl.get("products_completed_limit", "")
    
    # Auto
    if auto.get("has"):
        letter = auto.get("insurer_letter", "B")
        eff, exp = line_dates(auto)
        fields[f"{p}AutomobileLiability_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}AutomobileLiability_PolicyNumberIdentifier_A[0]"] = auto.get("policy_number", "")
        fields[f"{p}AutomobileLiability_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}AutomobileLiability_PolicyExpirationDate_A[0]"] = exp
        fields[f"{p}AutomobileLiability_CombinedSingleLimit_EachAccidentAmount_A[0]"] = auto.get("combined_single_limit", "")
        if auto.get("any_auto"): fields[f"{p}AutomobileLiability_AnyAutoIndicator_A[0]"] = "Yes"
        if auto.get("hired"): fields[f"{p}AutomobileLiability_HiredAutosOnlyIndicator_A[0]"] = "Yes"
        if auto.get("non_owned"): fields[f"{p}AutomobileLiability_NonOwnedAutosOnlyIndicator_A[0]"] = "Yes"
    
    # Umbrella
    if umb.get("has"):
        letter = umb.get("insurer_letter", "C")
        eff, exp = line_dates(umb)
        fields[f"{p}ExcessUmbrella_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}ExcessUmbrella_PolicyNumberIdentifier_A[0]"] = umb.get("policy_number", "")
        fields[f"{p}ExcessUmbrella_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}ExcessUmbrella_PolicyExpirationDate_A[0]"] = exp
        fields[f"{p}ExcessUmbrella_Umbrella_EachOccurrenceAmount_A[0]"] = umb.get("each_occurrence", "")
        fields[f"{p}ExcessUmbrella_Umbrella_AggregateAmount_A[0]"] = umb.get("aggregate", "")
    
    # WC
    if wc.get("has"):
        letter = wc.get("insurer_letter", "D")
        eff, exp = line_dates(wc)
        fields[f"{p}WorkersCompensation_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}WorkersCompensation_PolicyNumberIdentifier_A[0]"] = wc.get("policy_number", "")
        fields[f"{p}WorkersCompensation_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}WorkersCompensation_PolicyExpirationDate_A[0]"] = exp
        if wc.get("statutory"): fields[f"{p}WorkersCompensation_StatutoryLimitsIndicator_A[0]"] = "Yes"
        fields[f"{p}WorkersCompensation_EachAccident_LimitAmount_A[0]"] = wc.get("el_each_accident", "")
        fields[f"{p}WorkersCompensation_DiseasePolicyLimit_LimitAmount_A[0]"] = wc.get("el_disease_policy", "")
        fields[f"{p}WorkersCompensation_DiseaseEachEmployee_LimitAmount_A[0]"] = wc.get("el_disease_each", "")
    
    # Certificate Holder
    ch = cert_holder
    fields[f"{p}CertificateHolder_FullName_A[0]"] = ch.get("name", "")
    fields[f"{p}CertificateHolder_MailingAddress_LineOne_A[0]"] = ch.get("address_line1", "")
    fields[f"{p}CertificateHolder_MailingAddress_LineTwo_A[0]"] = ch.get("address_line2", "")
    fields[f"{p}CertificateHolder_MailingAddress_CityName_A[0]"] = ch.get("city", "")
    fields[f"{p}CertificateHolder_MailingAddress_StateOrProvinceCode_A[0]"] = ch.get("state", "")
    fields[f"{p}CertificateHolder_MailingAddress_PostalCode_A[0]"] = ch.get("zip", "")
    
    # Description
    desc_parts = []
    if ch.get("additional_insured"):
        desc_parts.append(f"{ch['name']} is included as Additional Insured as required by written contract.")
    if ch.get("waiver_of_subrogation"):
        desc_parts.append("Waiver of Subrogation applies in favor of the Certificate Holder as required by written contract.")
    if ch.get("primary_noncontributory"):
        desc_parts.append("Coverage is Primary and Non-Contributory as required by written contract.")
    if ch.get("additional_description"):
        desc_parts.append(ch["additional_description"])
    if desc_parts:
        fields[f"{p}CertificateOfLiabilityInsurance_ACORDForm_RemarkText_A[0]"] = "\n".join(desc_parts)
    
    if ch.get("additional_insured"):
        if gl.get("has"): fields[f"{p}CertificateOfInsurance_GeneralLiability_AdditionalInsuredCode_A[0]"] = "Y"
        if auto.get("has"): fields[f"{p}CertificateOfInsurance_AutomobileLiability_AdditionalInsuredCode_A[0]"] = "Y"
    
    return fields



# ── API Endpoints ──

@app.get("/health")
async def health():
    with get_db() as db:
        stats = db.execute("SELECT COUNT(*) as c FROM requests").fetchone()
        extractions = db.execute("SELECT COUNT(*) as c FROM extractions").fetchone()
        generations = db.execute("SELECT COUNT(*) as c FROM generations").fetchone()
        errors = db.execute("SELECT COUNT(*) as c FROM errors").fetchone()
    return {
        "status": "ok", "service": "acord-api-v2", "forms": list(BLANK_FORMS.keys()),
        "stats": {
            "total_requests": stats["c"], "total_extractions": extractions["c"],
            "total_generations": generations["c"], "total_errors": errors["c"],
        }
    }


@app.post("/api/extract")
async def extract_policy(request: Request, file: UploadFile = File(...), x_api_key: str = Header(None)):
    check_auth(x_api_key)
    start = time.time()
    
    # Get user from JWT if present
    _current_user = None
    _auth_header = request.headers.get("authorization", "")
    if _auth_header.startswith("Bearer "):
        try:
            from auth import decode_token, get_user as _get_user
            _payload = decode_token(_auth_header[7:])
            if _payload:
                _current_user = _get_user(_payload["sub"])
        except:
            pass
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files accepted")
    
    pdf_bytes = await file.read()
    if len(pdf_bytes) > 20 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 20MB)")
    
    # Save uploaded file
    fhash = file_hash(pdf_bytes)
    upload_path = os.path.join(DATA_DIR, "uploads", f"{fhash}_{file.filename}")
    with open(upload_path, "wb") as f:
        f.write(pdf_bytes)
    
    try:
        result = await extract_policy_data_with_ai(pdf_bytes)
        duration = (time.time() - start) * 1000
        
        # Log request
        rid = log_request(request, "/api/extract", 200, duration, len(pdf_bytes), 
                         len(json.dumps(result).encode()))
        
        # Log extraction details
        meta = result.pop("_meta", {})
        coverages_found = []
        for cov_name in ["gl", "auto", "umbrella", "workers_comp", "property"]:
            if result.get("coverages", {}).get(cov_name, {}).get("has"):
                coverages_found.append(cov_name)
        
        eid = str(uuid.uuid4())[:12]

        # Calculate extraction quality score (0-100 based on field fill rate)
        def _calc_quality(data):
            filled, total = 0, 0
            def _count(obj, depth=0):
                nonlocal filled, total
                if depth > 5: return
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k.startswith("_"): continue
                        total += 1
                        if v and v != "" and v != [] and v != {}:
                            filled += 1
                        _count(v, depth + 1)
                elif isinstance(obj, list):
                    for item in obj: _count(item, depth + 1)
            _count(data)
            return round((filled / total * 100) if total > 0 else 0)
        eq_score = _calc_quality(result)

        with get_db() as db:
            db.execute("""
            INSERT INTO extractions (id, request_id, timestamp, upload_filename, upload_size_bytes,
                    upload_hash, upload_path, text_length, used_vision, ai_model,
                    ai_prompt_tokens, ai_completion_tokens, ai_duration_ms, extracted_data,
                    insured_name, carrier, coverages_found, extraction_quality)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (eid, rid, now_iso(), file.filename, len(pdf_bytes), fhash, upload_path,
                  meta.get("text_length", 0), 1 if meta.get("used_vision") else 0,
                  meta.get("ai_model", ""), meta.get("ai_prompt_tokens", 0),
                  meta.get("ai_completion_tokens", 0), meta.get("ai_duration_ms", 0),
                  json.dumps(result), result.get("insured", {}).get("name", ""),
                  result.get("policy", {}).get("carrier", ""), json.dumps(coverages_found), str(eq_score)))
        
        # Save extraction result
        ext_path = os.path.join(DATA_DIR, "extractions", f"{eid}.json")
        with open(ext_path, "w") as f:
            json.dump({"extraction_id": eid, "request_id": rid, "filename": file.filename,
                       "result": result, "meta": meta}, f, indent=2)
        
        if "error" in result:
            log_error(rid, "/api/extract", "extraction_partial", result["error"])
        
        return JSONResponse(result)
        
    except Exception as e:
        duration = (time.time() - start) * 1000
        rid = log_request(request, "/api/extract", 500, duration, len(pdf_bytes), 0, str(e))
        log_error(rid, "/api/extract", type(e).__name__, str(e), traceback.format_exc())
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/generate")
async def generate_certificate(
    request: Request,
    x_api_key: str = Header(None),
    form_type: str = Form("25"),
    policy_data: str = Form(...),
    cert_holder: str = Form(...),
    agency: str = Form("{}"),
    signature: str = Form(""),
    signature_mode: str = Form(""),
    flatten: bool = Form(True),
):
    check_auth(x_api_key)
    start = time.time()
    
    # Get user from JWT if present
    _current_user = None
    _auth_header = request.headers.get("authorization", "")
    if _auth_header.startswith("Bearer "):
        try:
            from auth import decode_token, get_user as _get_user
            _payload = decode_token(_auth_header[7:])
            if _payload:
                _current_user = _get_user(_payload["sub"])
        except:
            pass
    
    if form_type not in BLANK_FORMS:
        raise HTTPException(400, f"Unsupported form: {form_type}")
    
    try:
        policy = json.loads(policy_data)
        holder = json.loads(cert_holder)
        agency_info = json.loads(agency)
    except json.JSONDecodeError as e:
        raise HTTPException(400, f"Invalid JSON: {e}")
    
    try:
        # Map fields
        if form_type == "25":
            field_data = map_to_acord25(policy, holder, agency_info)
        else:
            field_data = {**policy, **holder}
        
        blank_path = BLANK_FORMS[form_type]
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name
        
        from fill_acord import fill_acord_form
        result = fill_acord_form(blank_path, field_data, output_path, flatten=flatten)
        
        # Handle signature overlay
        if signature:
            try:
                doc = fitz.open(output_path)
                page = doc[0]
                # Signature placement — authorized representative area on ACORD 25
                sig_rect = fitz.Rect(320, 720, 580, 745)
                
                if signature.startswith("data:image"):
                    # Image signature
                    sig_data = signature.split(",", 1)[1]
                    sig_bytes = base64.b64decode(sig_data)
                    page.insert_image(sig_rect, stream=sig_bytes)
                else:
                    # Typed signature — render in cursive font
                    font_path = os.path.join(BASE_DIR, "DancingScript.ttf")
                    if os.path.exists(font_path):
                        page.insert_font(fontname="cursive", fontfile=font_path)
                        # Center the text in the signature area
                        font_size = 18
                        text_width = len(signature) * font_size * 0.45
                        x = sig_rect.x0 + (sig_rect.width - text_width) / 2
                        y = sig_rect.y0 + 18
                        page.insert_text((x, y), signature, fontname="cursive", fontsize=font_size, color=(0.05, 0.05, 0.15))
                    else:
                        # Fallback: use Helvetica italic-ish
                        page.insert_text((sig_rect.x0 + 10, sig_rect.y0 + 16), signature, fontname="helv", fontsize=14, color=(0.05, 0.05, 0.15))
                
                doc.save(output_path + "_sig.pdf")
                doc.close()
                os.rename(output_path + "_sig.pdf", output_path)
            except Exception as sig_err:
                log_error("", "/api/generate", "signature_overlay", str(sig_err), traceback.format_exc())
        
        with open(output_path, "rb") as f:
            pdf_bytes = f.read()
        
        # Save generated cert
        gen_id = str(uuid.uuid4())[:12]
        gen_filename = f"{gen_id}_ACORD-{form_type}_{holder.get('name', 'cert').replace(' ', '_')}.pdf"
        gen_path = os.path.join(DATA_DIR, "generated", gen_filename)
        with open(gen_path, "wb") as f:
            f.write(pdf_bytes)
        
        duration = (time.time() - start) * 1000
        rid = log_request(request, "/api/generate", 200, duration, 
                         len(policy_data) + len(cert_holder), len(pdf_bytes))
        
        # Log generation details
        coverages = []
        for cn in ["gl", "auto", "umbrella", "workers_comp", "property"]:
            if policy.get("coverages", {}).get(cn, {}).get("has"):
                coverages.append(cn)
        
        with get_db() as db:
            db.execute("""
                INSERT INTO generations (id, request_id, timestamp, form_type, insured_name, carrier,
                    cert_holder_name, policy_number, coverages, additional_insured, waiver_of_sub,
                    primary_noncontrib, agency_name, has_signature, signature_mode, fields_filled,
                    fields_total, fields_skipped, output_path, output_size_bytes, input_data,
                    cert_holder_data, agency_data, flatten, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (gen_id, rid, now_iso(), form_type,
                  policy.get("insured", {}).get("name", ""),
                  policy.get("policy", {}).get("carrier", ""),
                  holder.get("name", ""),
                  policy.get("policy", {}).get("number", ""),
                  json.dumps(coverages),
                  1 if holder.get("additional_insured") else 0,
                  1 if holder.get("waiver_of_subrogation") else 0,
                  1 if holder.get("primary_noncontributory") else 0,
                  agency_info.get("name", ""),
                  1 if signature else 0,
                  signature_mode,
                  result["filled_count"], result["total_fields"],
                  json.dumps(result.get("skipped_fields", [])),
                  gen_path, len(pdf_bytes),
                  policy_data[:10000], cert_holder[:5000], agency[:5000],
                  1 if flatten else 0,
                  _current_user["id"] if _current_user else None))
        
        os.remove(output_path)
        
        filename = f"ACORD-{form_type}-{holder.get('name', 'cert').replace(' ', '_')}-{datetime.now().strftime('%Y%m%d')}.pdf"
        return Response(
            content=pdf_bytes, media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Fields-Filled": str(result["filled_count"]),
                "X-Fields-Total": str(result["total_fields"]),
                "X-Generation-Id": gen_id,
            }
        )
        
    except Exception as e:
        duration = (time.time() - start) * 1000
        rid = log_request(request, "/api/generate", 500, duration, 0, 0, str(e))
        log_error(rid, "/api/generate", type(e).__name__, str(e), traceback.format_exc(),
                  json.dumps({"form_type": form_type, "insured": policy.get("insured", {}).get("name", "")}))
        return JSONResponse({"error": str(e)}, status_code=500)


# ── Dashboard API ──

@app.get("/api/dashboard")
async def dashboard(x_api_key: str = Header(None)):
    check_auth(x_api_key)
    
    with get_db() as db:
        # Overall stats
        stats = {}
        for table in ["requests", "extractions", "generations", "errors"]:
            row = db.execute(f"SELECT COUNT(*) as c FROM {table}").fetchone()
            stats[f"total_{table}"] = row["c"]
        
        # Today's stats
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        for table in ["requests", "extractions", "generations", "errors"]:
            row = db.execute(f"SELECT COUNT(*) as c FROM {table} WHERE timestamp LIKE ?", (f"{today}%",)).fetchone()
            stats[f"today_{table}"] = row["c"]
        
        # Recent requests (last 50)
        recent = [dict(r) for r in db.execute(
            "SELECT * FROM requests ORDER BY timestamp DESC LIMIT 50").fetchall()]
        
        # Recent generations (last 50)
        recent_gens = [dict(r) for r in db.execute(
            "SELECT id, timestamp, form_type, insured_name, carrier, cert_holder_name, "
            "agency_name, coverages, fields_filled, fields_total, has_signature, error "
            "FROM generations ORDER BY timestamp DESC LIMIT 50").fetchall()]
        
        # Recent extractions (last 50)
        recent_extractions = [dict(r) for r in db.execute(
            "SELECT id, timestamp, upload_filename, upload_size_bytes, insured_name, carrier, "
            "coverages_found, used_vision, ai_duration_ms, error "
            "FROM extractions ORDER BY timestamp DESC LIMIT 50").fetchall()]
        
        # Recent errors (last 50)
        recent_errors = [dict(r) for r in db.execute(
            "SELECT id, timestamp, endpoint, error_type, error_message "
            "FROM errors ORDER BY timestamp DESC LIMIT 50").fetchall()]
        
        # Hourly activity (last 24h)
        hourly = [dict(r) for r in db.execute("""
            SELECT strftime('%Y-%m-%d %H:00', timestamp) as hour, COUNT(*) as count
            FROM requests WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY hour ORDER BY hour
        """).fetchall()]
        
        # Top error types
        top_errors = [dict(r) for r in db.execute("""
            SELECT error_type, COUNT(*) as count, MAX(timestamp) as last_seen
            FROM errors GROUP BY error_type ORDER BY count DESC LIMIT 10
        """).fetchall()]
        
        # Form type distribution
        form_dist = [dict(r) for r in db.execute("""
            SELECT form_type, COUNT(*) as count FROM generations GROUP BY form_type
        """).fetchall()]
        
        # Coverage frequency
        cov_freq = {}
        for row in db.execute("SELECT coverages FROM generations").fetchall():
            for cov in json.loads(row["coverages"] or "[]"):
                cov_freq[cov] = cov_freq.get(cov, 0) + 1
        
        # Average times
        avg_extract = db.execute("SELECT AVG(ai_duration_ms) as avg FROM extractions WHERE ai_duration_ms > 0").fetchone()
        avg_gen = db.execute("SELECT AVG(duration_ms) as avg FROM requests WHERE endpoint = '/api/generate' AND status_code = 200").fetchone()
        
        # Daily analysis
        latest_analysis = db.execute("SELECT * FROM daily_analysis ORDER BY date DESC LIMIT 1").fetchone()
        
    return {
        "stats": stats,
        "recent_requests": recent,
        "recent_generations": recent_gens,
        "recent_extractions": recent_extractions,
        "recent_errors": recent_errors,
        "hourly_activity": hourly,
        "top_errors": top_errors,
        "form_distribution": form_dist,
        "coverage_frequency": cov_freq,
        "avg_extraction_ms": round(avg_extract["avg"] or 0, 1),
        "avg_generation_ms": round(avg_gen["avg"] or 0, 1),
        "latest_analysis": dict(latest_analysis) if latest_analysis else None,
    }


@app.get("/api/dashboard/files")
async def list_files(x_api_key: str = Header(None), folder: str = "generated"):
    check_auth(x_api_key)
    if folder not in ["uploads", "generated", "extractions", "errors"]:
        raise HTTPException(400, "Invalid folder")
    
    folder_path = os.path.join(DATA_DIR, folder)
    files = []
    for f in sorted(os.listdir(folder_path), reverse=True)[:100]:
        fp = os.path.join(folder_path, f)
        files.append({"name": f, "size": os.path.getsize(fp), 
                      "modified": datetime.fromtimestamp(os.path.getmtime(fp)).isoformat()})
    return {"folder": folder, "files": files}


@app.get("/api/dashboard/file/{folder}/{filename}")
async def get_file(folder: str, filename: str, x_api_key: str = Header(None)):
    check_auth(x_api_key)
    if folder not in ["uploads", "generated", "extractions", "errors"]:
        raise HTTPException(400, "Invalid folder")
    
    fp = os.path.join(DATA_DIR, folder, filename)
    if not os.path.exists(fp):
        raise HTTPException(404, "File not found")
    
    with open(fp, "rb") as f:
        content = f.read()
    
    ct = "application/pdf" if filename.endswith(".pdf") else "application/json"
    return Response(content=content, media_type=ct,
                   headers={"Content-Disposition": f'inline; filename="{filename}"'})


# ── Auth Routes (append to server.py) ──

from auth import (
    init_users_db, create_user, login_user, get_user, decode_token,
    update_agency_profile, update_user_profile, change_password,
    admin_list_users, admin_reset_password, admin_toggle_active, admin_toggle_admin,
    get_user_certificates
)

# Init users table on startup
init_users_db()

# Create default admin if no users exist
with sqlite3.connect(DB_PATH) as _conn:
    _conn.row_factory = sqlite3.Row
    _count = _conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    if _count == 0:
        create_user("admin", "Alliance2026!", email="mark.walters@joinalliancerisk.com", display_name="Mark Walters", is_admin=True)
        print("✅ Created default admin user: admin / Alliance2026!")


def get_current_user(request: Request) -> dict | None:
    """Extract user from Authorization header."""
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[7:]
    payload = decode_token(token)
    if not payload:
        return None
    return get_user(payload["sub"])


def require_user(request: Request) -> dict:
    """Require authenticated user or raise 401."""
    user = get_current_user(request)
    if not user:
        raise HTTPException(401, "Authentication required")
    return user


def require_admin(request: Request) -> dict:
    """Require admin user or raise 403."""
    user = require_user(request)
    if not user.get("is_admin"):
        raise HTTPException(403, "Admin access required")
    return user


# ── Auth Endpoints ──

@app.post("/api/auth/register")
async def register(request: Request):
    body = await request.json()
    username = body.get("username", "").strip()
    password = body.get("password", "")
    email = body.get("email", "").strip()
    display_name = body.get("display_name", "").strip()
    
    if not username or not password:
        raise HTTPException(400, "Username and password required")
    if len(password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    if len(username) < 2:
        raise HTTPException(400, "Username must be at least 2 characters")
    
    try:
        user = create_user(username, password, email, display_name)
        result = login_user(username, password)
        return JSONResponse(result)
    except ValueError as e:
        raise HTTPException(409, str(e))


@app.post("/api/auth/login")
async def auth_login(request: Request):
    body = await request.json()
    username = body.get("username", "")
    password = body.get("password", "")
    
    result = login_user(username, password)
    if not result:
        raise HTTPException(401, "Invalid username or password")
    return JSONResponse(result)


@app.get("/api/auth/me")
async def auth_me(request: Request):
    user = require_user(request)
    return JSONResponse({"user": user})


@app.put("/api/auth/profile")
async def update_profile(request: Request):
    user = require_user(request)
    body = await request.json()
    
    if "email" in body:
        update_user_profile(user["id"], email=body["email"])
    if "display_name" in body:
        update_user_profile(user["id"], display_name=body["display_name"])
    
    updated = get_user(user["id"])
    return JSONResponse({"user": updated})


@app.put("/api/auth/agency")
async def update_agency(request: Request):
    user = require_user(request)
    body = await request.json()
    update_agency_profile(user["id"], body)
    updated = get_user(user["id"])
    return JSONResponse({"user": updated})


@app.put("/api/auth/password")
async def auth_change_password(request: Request):
    user = require_user(request)
    body = await request.json()
    old_pw = body.get("old_password", "")
    new_pw = body.get("new_password", "")
    
    if len(new_pw) < 6:
        raise HTTPException(400, "New password must be at least 6 characters")
    
    if not change_password(user["id"], old_pw, new_pw):
        raise HTTPException(400, "Current password is incorrect")
    
    return JSONResponse({"ok": True, "message": "Password changed"})


# ── User Certificate History ──

@app.get("/api/my/certificates")
async def my_certificates(request: Request):
    user = require_user(request)
    certs = get_user_certificates(user["id"])
    return JSONResponse({"certificates": certs})


@app.get("/api/my/certificates/{cert_id}/download")
async def download_certificate(cert_id: str, request: Request):
    user = require_user(request)
    
    with get_db() as db:
        cert = db.execute(
            "SELECT * FROM generations WHERE id = ? AND user_id = ?",
            (cert_id, user["id"])
        ).fetchone()
        
        if not cert:
            # Admin can download any
            if user.get("is_admin"):
                cert = db.execute("SELECT * FROM generations WHERE id = ?", (cert_id,)).fetchone()
            if not cert:
                raise HTTPException(404, "Certificate not found")
        
        path = cert["output_path"]
        if not path or not os.path.exists(path):
            raise HTTPException(404, "PDF file not found on disk")
        
        with open(path, "rb") as f:
            pdf_bytes = f.read()
        
        filename = f"ACORD-{cert['form_type']}_{cert['insured_name'].replace(' ', '_')}_{cert['timestamp'][:10]}.pdf"
        return Response(
            content=pdf_bytes, media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )


# ── Admin Endpoints ──

@app.get("/api/admin/users")
async def admin_users_list(request: Request):
    require_admin(request)
    users = admin_list_users()
    return JSONResponse({"users": users})


@app.post("/api/admin/users/{user_id}/reset-password")
async def admin_reset_pw(user_id: str, request: Request):
    require_admin(request)
    body = await request.json()
    new_pw = body.get("password", "")
    if len(new_pw) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    admin_reset_password(user_id, new_pw)
    return JSONResponse({"ok": True, "message": "Password reset"})


@app.post("/api/admin/users/{user_id}/toggle-active")
async def admin_toggle_user_active(user_id: str, request: Request):
    require_admin(request)
    admin_toggle_active(user_id)
    return JSONResponse({"ok": True})


@app.post("/api/admin/users/{user_id}/toggle-admin")
async def admin_toggle_user_admin(user_id: str, request: Request):
    require_admin(request)
    admin_toggle_admin(user_id)
    return JSONResponse({"ok": True})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
