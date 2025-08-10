import os, sqlite3, csv
from apps.db import init_db, get_conn

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def seed_prompt_tests(rows):
    conn = get_conn(); c = conn.cursor()
    for r in rows:
        c.execute("INSERT INTO prompt_tests (ts,payload,response,risky) VALUES (?,?,?,?)",
                  (r['ts'], r['payload'], r['response'], int(r['risky'])))
    conn.commit(); conn.close()

def seed_deepfakes(rows):
    conn = get_conn(); c = conn.cursor()
    for r in rows:
        c.execute("INSERT INTO deepfake_results (ts,url,verdict,confidence) VALUES (?,?,?,?)",
                  (r['ts'], r['url'], r['verdict'], float(r['confidence'])))
    conn.commit(); conn.close()

def seed_redteam(rows):
    conn = get_conn(); c = conn.cursor()
    for r in rows:
        c.execute("INSERT INTO redteam_plans (ts,system,techniques,plan) VALUES (?,?,?,?)",
                  (r['ts'], r['system'], r['techniques'], r['plan']))
    conn.commit(); conn.close()

def seed_pqc(rows):
    conn = get_conn(); c = conn.cursor()
    for r in rows:
        c.execute("INSERT INTO pqc_runs (ts,device,os,alg,ms,cpu,mem) VALUES (?,?,?,?,?,?,?)",
                  (r['ts'], r['device'], r['os'], r['alg'], float(r['ms']), float(r['cpu']), float(r['mem'])))
    conn.commit(); conn.close()

if __name__ == "__main__":
    init_db()
    base = os.path.join(os.path.dirname(__file__), "samples")
    seed_prompt_tests(load_csv(os.path.join(base, "prompt_injection_samples.csv")))
    seed_deepfakes(load_csv(os.path.join(base, "deepfake_results_samples.csv")))
    seed_redteam(load_csv(os.path.join(base, "redteam_plans_samples.csv")))
    seed_pqc(load_csv(os.path.join(base, "pqc_runs_samples.csv")))
    print("Seeded sample data into SQLite (mindhack.db).")

def main(reset: bool = False):
    if reset:
        from apps.db import reset_db
        reset_db()
    init_db()
    base = os.path.join(os.path.dirname(__file__), "samples")
    seed_prompt_tests(load_csv(os.path.join(base, "prompt_injection_samples.csv")))
    seed_deepfakes(load_csv(os.path.join(base, "deepfake_results_samples.csv")))
    seed_redteam(load_csv(os.path.join(base, "redteam_plans_samples.csv")))
    seed_pqc(load_csv(os.path.join(base, "pqc_runs_samples.csv")))
    print("Seeded sample data into SQLite (mindhack.db).")

if __name__ == "__main__":
    main()
