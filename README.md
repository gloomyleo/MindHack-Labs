<p align="center">
  <img src="assets/banner.svg" alt="MindHack Labs – AI Security & Red Team Projects" />
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![CI](https://img.shields.io/github/actions/workflow/status/your-username/MindHack-Labs/ci.yml?label=CI&logo=github-actions)](#)
[![Built with n8n](https://img.shields.io/badge/Built%20with-n8n-16A34A)](https://n8n.io/)

</div>

# MindHack Labs

**MindHack Labs** is a collection of **AI-focused security projects** for red teams and defenders, powered by **n8n** + **Python**.

## ✨ What’s Inside
- **Prompt Injection Testing** — simulate prompt-injection payloads against LLM apps and capture outcomes.
- **Deepfake Detection Engine** — ingest social media media links and detect AI-manipulated content.
- **AI Red Team Simulator** — plan and (optionally) execute MITRE ATT&CK-aligned simulations.
- **Post-Quantum Crypto Benchmarking** — benchmark PQC algorithms on real devices.

> Public, open-source, and classroom-ready. MIT licensed.

---

## 🚀 Quickstart

### 1) Clone & Setup
```bash
git clone https://github.com/<your-username>/MindHack-Labs.git
cd MindHack-Labs
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r python_apis/requirements.txt
```

### 2) Run the local APIs
In separate terminals:
```bash
python python_apis/prompt_test.py       # prompt injection examples
python python_apis/deepfake_api.py      # -> http://localhost:5001/detect
python python_apis/redteam_agent.py     # -> http://localhost:5002/simulate
python python_apis/pqc_benchmark.py     # -> http://localhost:5003/benchmark
```

### 3) Import n8n Workflows
- Start n8n (Docker or local).
- Import the workflows from `./n8n_workflows/`.
- Update the HTTP Request nodes to point to the local APIs (`http://host.docker.internal:<port>` when using Docker Desktop).

### 4) Optional Dashboards
Use `dashboards/` templates for Grafana / Superset / Google Data Studio.

---

## 🧭 Repository Layout

```
.
├── .github/                   # Issue templates and CI
├── assets/                    # Logos, banner
├── dashboards/                # Dashboard samples and schemas
├── docs/                      # GitHub Pages site (this repo's page)
├── n8n_workflows/             # Importable n8n .json workflows (placeholders)
├── python_apis/               # Flask APIs used by the workflows
├── samples/                   # Example payloads, data, and MITRE TTP lists
└── ...
```

---

## 👤 About the Maintainer

**Moazzam Hussain** — Senior Manager, Cybersecurity Technology & Engineering.  
Focus areas: **Security Engineering**, **AI Security**, **Zero Trust**, **OT/IT**, and **Cloud Security**.

- 🌐 LinkedIn: *add your link here*
- ✉️ Email: *add your contact email*
- 🧪 Research: AI threats (prompt injection, deepfakes), autonomous adversary simulation, PQC readiness

> If this repo helps you, ⭐ star it and share feedback or PRs. Contributions are welcome!

---

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## 🔒 Security
For vulnerabilities, see [SECURITY.md](SECURITY.md).

## 📜 License
MIT — see [LICENSE](LICENSE).
