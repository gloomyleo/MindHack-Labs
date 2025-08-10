import os, sqlite3, pandas as pd, streamlit as st, matplotlib.pyplot as plt

DB_PATH = os.getenv("MINDHACK_DB", "mindhack.db")

st.set_page_config(page_title="MindHack-Labs Dashboard", layout="wide")
st.title("MindHack-Labs — Dashboard")

@st.cache_data
def load_table(name: str, limit: int = 500):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {name} ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return df

tabs = st.tabs(["Prompt Injection", "Deepfakes", "AI Red Team", "PQC"])

with tabs[0]:
    st.subheader("Prompt Injection Tests")
    df = load_table("prompt_tests")
    st.dataframe(df)
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
