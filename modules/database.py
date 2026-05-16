"""
database.py — PostgreSQL via Railway
Koneksi persisten, data tidak pernah hilang.
"""
import os
import psycopg2
import psycopg2.extras
import pandas as pd


def get_connection():
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        try:
            import streamlit as st
            url = st.secrets.get("DATABASE_URL", "")
        except Exception:
            pass
    if not url:
        raise ValueError("DATABASE_URL tidak ditemukan.")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    conn = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
    conn.autocommit = False
    return conn


def run(sql, params=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute(sql, params or ())
    conn.commit()
    c.close()
    conn.close()


def fetch(sql, params=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute(sql, params or ())
    rows = c.fetchall()
    c.close()
    conn.close()
    return [dict(r) for r in rows]


def fetchone(sql, params=None):
    rows = fetch(sql, params)
    return rows[0] if rows else None


def qdf(sql, params=None):
    rows = fetch(sql, params)
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def init_database():
    conn = get_connection()
    c = conn.cursor()

    tables = [
        """CREATE TABLE IF NOT EXISTS app_settings (
            id SERIAL PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT NOT NULL DEFAULT 'viewer',
            email TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS batch_production (
            id SERIAL PRIMARY KEY,
            batch_number TEXT UNIQUE NOT NULL,
            production_date TEXT NOT NULL,
            vehicle_type TEXT DEFAULT 'Kendaraan Multifungsi Nasional',
            total_units INTEGER DEFAULT 0,
            total_defect INTEGER DEFAULT 0,
            total_rework INTEGER DEFAULT 0,
            defect_rate REAL DEFAULT 0.0,
            rework_rate REAL DEFAULT 0.0,
            pic TEXT, status TEXT DEFAULT 'In Progress',
            notes TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS defect_records (
            id SERIAL PRIMARY KEY,
            batch_id INTEGER, batch_number TEXT,
            defect_type TEXT NOT NULL,
            defect_stage TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            root_cause TEXT, corrective_action TEXT, pic TEXT,
            follow_up_status TEXT DEFAULT 'Open',
            found_date TEXT, resolved_date TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS iso9001_evaluation (
            id SERIAL PRIMARY KEY,
            eval_date TEXT NOT NULL, batch_number TEXT,
            process_documentation REAL DEFAULT 0,
            process_control REAL DEFAULT 0,
            internal_audit REAL DEFAULT 0,
            corrective_action REAL DEFAULT 0,
            continuous_improvement REAL DEFAULT 0,
            average_score REAL DEFAULT 0,
            category TEXT, evaluator TEXT, notes TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS iatf16949_evaluation (
            id SERIAL PRIMARY KEY,
            eval_date TEXT NOT NULL, batch_number TEXT,
            risk_based_thinking REAL DEFAULT 0,
            defect_prevention REAL DEFAULT 0,
            supplier_quality REAL DEFAULT 0,
            continuous_improvement REAL DEFAULT 0,
            average_score REAL DEFAULT 0,
            category TEXT, evaluator TEXT, notes TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS engineering_lifecycle (
            id SERIAL PRIMARY KEY,
            eval_date TEXT NOT NULL, batch_number TEXT,
            design_control REAL DEFAULT 0,
            change_control REAL DEFAULT 0,
            verification_validation REAL DEFAULT 0,
            integration_process REAL DEFAULT 0,
            traceability REAL DEFAULT 0,
            design_change_communication REAL DEFAULT 0,
            average_score REAL DEFAULT 0,
            maturity_level TEXT, evaluator TEXT, notes TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS quality_consistency (
            id SERIAL PRIMARY KEY,
            eval_date TEXT NOT NULL, batch_number TEXT,
            quality_uniformity REAL DEFAULT 0,
            low_defect_rate REAL DEFAULT 0,
            inter_batch_stability REAL DEFAULT 0,
            low_rework_rate REAL DEFAULT 0,
            spec_conformance REAL DEFAULT 0,
            average_score REAL DEFAULT 0,
            category TEXT, evaluator TEXT, notes TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS interview_data (
            id SERIAL PRIMARY KEY,
            interview_date TEXT NOT NULL,
            informant_name TEXT NOT NULL,
            position TEXT, work_unit TEXT,
            interview_result TEXT, key_insights TEXT,
            finding_category TEXT, interviewer TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS about_platform (
            id SERIAL PRIMARY KEY,
            key TEXT UNIQUE NOT NULL, value TEXT,
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS media_storage (
            id SERIAL PRIMARY KEY,
            media_key TEXT UNIQUE NOT NULL,
            filename TEXT, data TEXT, mime_type TEXT,
            uploaded_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS maung_defects (
            id SERIAL PRIMARY KEY,
            batch TEXT NOT NULL,
            tanggal TEXT,
            defect TEXT NOT NULL,
            kategori TEXT NOT NULL,
            jenis TEXT NOT NULL,
            source TEXT DEFAULT 'MoM',
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS pls_results (
            id SERIAL PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            label TEXT,
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
                """CREATE TABLE IF NOT EXISTS maung_defects (
            id SERIAL PRIMARY KEY,
            batch TEXT NOT NULL,
            tanggal TEXT,
            defect TEXT NOT NULL,
            kategori TEXT NOT NULL,
            jenis TEXT NOT NULL,
            unit_no TEXT,
            source TEXT DEFAULT 'MoM',
            pic TEXT,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT NOW()
        )""",
    ]

    for sql in tables:
        c.execute(sql)

    conn.commit()
    c.close()
    conn.close()


def get_setting(key, default=""):
    row = fetchone("SELECT value FROM app_settings WHERE key=%s", (key,))
    return row['value'] if row and row['value'] else default


def set_setting(key, value):
    run("""INSERT INTO app_settings (key,value) VALUES (%s,%s)
           ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value, updated_at=NOW()""",
        (key, value))


def get_media(key):
    return fetchone("SELECT data, mime_type FROM media_storage WHERE media_key=%s", (key,))


def save_media(key, filename, data_b64, mime_type):
    run("""INSERT INTO media_storage (media_key,filename,data,mime_type) VALUES (%s,%s,%s,%s)
           ON CONFLICT(media_key) DO UPDATE SET data=EXCLUDED.data,
           mime_type=EXCLUDED.mime_type, uploaded_at=NOW()""",
        (key, filename, data_b64, mime_type))


def delete_media(key):
    run("DELETE FROM media_storage WHERE media_key=%s", (key,))


def get_category(score):
    if score >= 85:   return "Sangat Baik"
    elif score >= 75: return "Baik"
    elif score >= 60: return "Cukup"
    else:             return "Perlu Perbaikan"


def get_lifecycle_maturity(score):
    if score >= 85:   return "Optimized"
    elif score >= 75: return "Managed"
    elif score >= 60: return "Defined"
    elif score >= 40: return "Developing"
    else:             return "Initial"


# ── PLS-SEM Result Helpers ─────────────────────────────────

PLS_DEFAULTS = {
    # Hipotesis
    "h1_beta":   ("0.318", "β ISO 9001 → Y"),
    "h1_tstat":  ("3.847", "T-Statistik H1"),
    "h1_pval":   ("0.001", "P-Value H1"),
    "h1_status": ("Diterima", "Status H1"),
    "h2_beta":   ("0.217", "β IATF 16949 → Y"),
    "h2_tstat":  ("2.913", "T-Statistik H2"),
    "h2_pval":   ("0.004", "P-Value H2"),
    "h2_status": ("Diterima", "Status H2"),
    "h3_beta":   ("0.532", "β Engineering Lifecycle → Y"),
    "h3_tstat":  ("6.124", "T-Statistik H3"),
    "h3_pval":   ("0.000", "P-Value H3"),
    "h3_status": ("Diterima", "Status H3"),
    # Model fit
    "model_r2":  ("0.729", "R² (Koefisien Determinasi)"),
    "model_q2":  ("0.548", "Q² (Predictive Relevance)"),
    # Validitas & Reliabilitas
    "ave_x1":    ("0.624", "AVE X1 ISO 9001"),
    "ave_x2":    ("0.587", "AVE X2 IATF 16949"),
    "ave_x3":    ("0.671", "AVE X3 Engineering Lifecycle"),
    "ave_y":     ("0.612", "AVE Y Konsistensi Mutu"),
    "cr_x1":     ("0.891", "CR X1"),
    "cr_x2":     ("0.857", "CR X2"),
    "cr_x3":     ("0.908", "CR X3"),
    "cr_y":      ("0.884", "CR Y"),
    "ca_x1":     ("0.852", "Cronbach Alpha X1"),
    "ca_x2":     ("0.801", "Cronbach Alpha X2"),
    "ca_x3":     ("0.876", "Cronbach Alpha X3"),
    "ca_y":      ("0.841", "Cronbach Alpha Y"),
    # Status data
    "data_status": ("Dummy — Menunggu Data Riil Kuesioner", "Status Data"),
    "n_responden": ("0", "Jumlah Responden"),
    "periode":     ("-", "Periode Pengumpulan Data"),
}


def get_pls(key):
    """Get PLS result value, fallback to default."""
    row = fetchone("SELECT value FROM pls_results WHERE key=%s", (key,))
    if row and row.get('value'):
        return row['value']
    return PLS_DEFAULTS.get(key, ("", ""))[0]


def set_pls(key, value):
    """Upsert PLS result value."""
    label = PLS_DEFAULTS.get(key, ("", key))[1]
    run("""INSERT INTO pls_results (key, value, label)
           VALUES (%s,%s,%s)
           ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value, updated_at=NOW()""",
        (key, value, label))


def get_pls_float(key):
    try:
        return float(get_pls(key))
    except Exception:
        return 0.0
