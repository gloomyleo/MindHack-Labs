import os, sqlite3, pandas as pd, streamlit as st, matplotlib.pyplot as plt

DB_PATH = os.getenv("MINDHACK_DB", "mindhack.db")

st.set_page_config(page_title="MindHack-Labs Dashboard", layout="wide")
st.title("MindHack-Labs — Dashboard")

# Sidebar: utilities & theme
with st.sidebar:
    st.subheader("Utilities")
    theme = st.radio("Theme", ["Light","Dark"], index=1)
    set_chart_style(theme)
    cols = st.columns(2)
    with cols[0]:
        if st.button("📥 Load sample data"):
            try:
                import os
                import seed_db
                base = os.path.join(os.path.dirname(__file__), "samples")
                seed_db.init_db()
                seed_db.seed_prompt_tests(seed_db.load_csv(os.path.join(base, "prompt_injection_samples.csv")))
                seed_db.seed_deepfakes(seed_db.load_csv(os.path.join(base, "deepfake_results_samples.csv")))
                seed_db.seed_redteam(seed_db.load_csv(os.path.join(base, "redteam_plans_samples.csv")))
                seed_db.seed_pqc(seed_db.load_csv(os.path.join(base, "pqc_runs_samples.csv")))
                st.success("Sample data loaded into mindhack.db")
                load_table.clear()
            except Exception as e:
                st.error(f"Failed to load samples: {e}")
    with cols[1]:
        if st.button("🗑️ Reset database"):
            try:
                from apps.db import reset_db
                reset_db()
                st.warning("Database reset. Tables recreated and now empty.")
                load_table.clear()
            except Exception as e:
                st.error(f"Failed to reset DB: {e}")


def set_chart_style(theme: str):
    import matplotlib as mpl
    # Light/dark minimal styles; do not set specific colors to comply with constraints
    if theme == "Dark":
        mpl.rcParams.update({
            "figure.facecolor": "#0e1117",
            "axes.facecolor": "#0e1117",
            "axes.edgecolor": "#cccccc",
            "text.color": "#e6e6e6",
            "axes.labelcolor": "#e6e6e6",
            "xtick.color": "#cccccc",
            "ytick.color": "#cccccc",
            "grid.color": "#333333",
        })
    else:
        mpl.rcParams.update({
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "text.color": "black",
            "axes.labelcolor": "black",
            "xtick.color": "black",
            "ytick.color": "black",
            "grid.color": "#dddddd",
        })


# Sidebar: load sample data into SQLite
with st.sidebar:
    st.subheader("Utilities")
    if st.button("📥 Load sample data"):
        try:
            import os
            import seed_db
            base = os.path.join(os.path.dirname(__file__), "samples")
            seed_db.init_db()
            seed_db.seed_prompt_tests(seed_db.load_csv(os.path.join(base, "prompt_injection_samples.csv")))
            seed_db.seed_deepfakes(seed_db.load_csv(os.path.join(base, "deepfake_results_samples.csv")))
            seed_db.seed_redteam(seed_db.load_csv(os.path.join(base, "redteam_plans_samples.csv")))
            seed_db.seed_pqc(seed_db.load_csv(os.path.join(base, "pqc_runs_samples.csv")))
            st.success("Sample data loaded into mindhack.db")
            # Clear caches so UI refreshes
            load_table.clear()
        except Exception as e:
            st.error(f"Failed to load samples: {e}")


import pandas as pd
import os

def offline_demo():
    st.sidebar.subheader("Offline Demo Mode")
    if st.sidebar.button("Load Offline Samples"):
        try:
            pi_df = pd.read_csv(os.path.join("samples", "pqc_benchmark_results.csv"))
            st.success("Offline PQC benchmark results loaded.")
        except Exception as e:
            st.error(f"Failed to load offline samples: {e}")


def _export_csv(df, label):
    if df is None or df.empty:
        return
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"Download {label} as CSV",
        data=csv,
        file_name=f"{label.replace(' ', '_').lower()}.csv",
        mime="text/csv",
        use_container_width=True
    )


@st.cache_data
def load_table(name: str, limit: int = 500):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {name} ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return df

tabs = st.tabs(["Prompt Injection", "Deepfakes", "AI Red Team", "PQC", "Help"])

with tabs[0]:
    st.subheader("Prompt Injection Tests")
    df = load_table("prompt_tests")
    st.dataframe(df)
    _export_csv(df, "PQC Runs")
    _export_csv(df, "AI Red Team Plans")
    _export_csv(df, "Deepfake Results")
    _export_csv(df, "Prompt Injection Logs")
    if not df.empty and "risky" in df.columns:
        risky_count = int(df["risky"].sum())
        total = int(len(df))
        st.write(f"Risky: {risky_count} / {total}")
        fig = plt.figure()
        plt.bar(["Risky","Safe"], [risky_count, total - risky_count])
        st.pyplot(fig)

with tabs[1]:
    st.subheader("Deepfake Results")
    df = load_table("deepfake_results")
    st.dataframe(df)
    if not df.empty and "verdict" in df.columns:
        counts = df["verdict"].value_counts()
        fig = plt.figure()
        counts.plot(kind="bar")
        st.pyplot(fig)

with tabs[2]:
    st.subheader("AI Red Team Plans")
    df = load_table("redteam_plans")
    st.dataframe(df)

with tabs[3]:
    st.subheader("PQC Runs")
    df = load_table("pqc_runs")
    st.dataframe(df)
    if not df.empty:
        fig = plt.figure()
        for device, g in df.groupby("device"):
            g2 = g.groupby("alg")["ms"].mean()
            plt.plot(g2.index, g2.values, marker="o", label=device)
        plt.legend()
        plt.ylabel("ms (avg)")
        st.pyplot(fig)

with tabs[4]:
    st.subheader("Help & Quick Links")
    st.markdown("""
**How to use**
1. Use the sidebar to **Load sample data** (or seed via CLI).
2. Explore each tab; download CSVs for offline sharing.
3. Switch the **Theme** if you prefer a light/dark look.
4. Click **Reset database** to start fresh.

**API endpoints**
- `POST /api/prompt-test`
- `POST /api/deepfake/detect`
- `POST /api/redteam/simulate`
- `GET  /api/pqc/benchmark`
- `GET  /api/logs/<table>` → `prompt_tests`, `deepfake_results`, `redteam_plans`, `pqc_runs`

**CLI shortcuts**
```bash
python apps/prompt_injection/cli.py --payload "Ignore prior instructions..."
python apps/ai_redteam/cli.py --system "Ubuntu" --ttps "T1059,T1041"
python apps/pqc_benchmark/cli.py
python apps/deepfake_detection/cli.py --url "file://samples/media/sample1.png"
```
    """)
