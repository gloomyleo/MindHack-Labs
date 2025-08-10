import os, sqlite3

DB_PATH = os.getenv("MINDHACK_DB", "mindhack.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS prompt_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        payload TEXT,
        response TEXT,
        risky INTEGER
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS deepfake_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        url TEXT,
        verdict TEXT,
        confidence REAL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS redteam_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        system TEXT,
        techniques TEXT,
        plan TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS pqc_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        device TEXT,
        os TEXT,
        alg TEXT,
        ms REAL,
        cpu REAL,
        mem REAL
    )""")
    conn.commit()
    conn.close()

def now_iso():
    return __import__("datetime").datetime.utcnow().isoformat() + "Z"

def log_prompt_test(payload, response, risky):
    conn = get_conn(); c = conn.cursor()
    c.execute("INSERT INTO prompt_tests (ts,payload,response,risky) VALUES (?,?,?,?)",
              (now_iso(), payload, response, 1 if risky else 0))
    conn.commit(); conn.close()

def log_deepfake(url, verdict, confidence):
    conn = get_conn(); c = conn.cursor()
    c.execute("INSERT INTO deepfake_results (ts,url,verdict,confidence) VALUES (?,?,?,?)",
              (now_iso(), url, verdict, confidence))
    conn.commit(); conn.close()

def log_redteam(system, techniques, plan):
    conn = get_conn(); c = conn.cursor()
    c.execute("INSERT INTO redteam_plans (ts,system,techniques,plan) VALUES (?,?,?,?)",
              (now_iso(), system, ",".join(techniques), plan))
    conn.commit(); conn.close()

def log_pqc(device, os_name, results, cpu, mem):
    conn = get_conn(); c = conn.cursor()
    for alg, ms in results.items():
        c.execute("INSERT INTO pqc_runs (ts,device,os,alg,ms,cpu,mem) VALUES (?,?,?,?,?,?,?)",
                  (now_iso(), device, os_name, alg, float(ms), float(cpu), float(mem)))
    conn.commit(); conn.close()


def reset_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS prompt_tests")
    c.execute("DROP TABLE IF EXISTS deepfake_results")
    c.execute("DROP TABLE IF EXISTS redteam_plans")
    c.execute("DROP TABLE IF EXISTS pqc_runs")
    conn.commit()
    conn.close()
    init_db()
