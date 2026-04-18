# CrewAI — Automated Project Planning, Estimation & Allocation

A production-ready Python project that uses a **CrewAI multi-agent system** to automatically plan, estimate, and allocate resources for any software project — then generate a Gantt chart from the results.

---

## Architecture — CrewAI Multi-Agent System

```
┌──────────────────────────────────────────────────────────────────┐
│                         CrewAI Crew                              │
│                    (Sequential Execution)                        │
│                                                                  │
│  ┌──────────────────────┐                                        │
│  │  Project Planner     │ → Breaks requirements into tasks       │
│  │  (GPT-4o-mini)       │   with scope, timelines, dependencies  │
│  └──────────┬───────────┘                                        │
│             │ task list                                          │
│  ┌──────────▼───────────┐                                        │
│  │  Estimation Analyst  │ → Estimates hours & resources per task │
│  │  (GPT-4o-mini)       │                                        │
│  └──────────┬───────────┘                                        │
│             │ task estimates                                     │
│  ┌──────────▼───────────┐                                        │
│  │ Resource Allocator   │ → Assigns team members, groups into    │
│  │  (GPT-4o-mini)       │   milestones, outputs ProjectPlan JSON │
│  └──────────────────────┘                                        │
└──────────────────────────────────────────────────────────────────┘
```

Each agent is defined in `config/agents.yaml` and each task in `config/tasks.yaml`. Inputs are interpolated at runtime via CrewAI's `{variable}` templating, keeping logic strictly separate from configuration.

The final agent outputs a **structured Pydantic model** (`ProjectPlan`) containing:
- `tasks` — list of `TaskEstimate` objects (name, hours, resources)
- `milestones` — list of `Milestone` objects grouping tasks into phases

---

## Project Structure

```
crewai-project-planner/
├── config/
│   ├── agents.yaml          # Agent roles, goals & backstories
│   └── tasks.yaml           # Task descriptions & expected outputs
├── src/
│   ├── __init__.py
│   ├── models.py            # Pydantic models (TaskEstimate, Milestone, ProjectPlan)
│   ├── crew.py              # Crew assembly — agents, tasks, sequential flow
│   └── visualizer.py        # Gantt chart generator (matplotlib)
├── output/                  # Auto-created at runtime
│   ├── plan.json            # Structured JSON output
│   └── gantt_chart.png      # Gantt chart image
├── main.py                  # Entry point — run this
├── pyproject.toml           # Poetry project configuration
├── requirements.txt         # pip-compatible dependencies
├── .env.example             # Environment variable template
├── .gitignore
└── README.md
```

---

## Quickstart

### Prerequisites

- Python 3.11+
- An [OpenAI API key](https://platform.openai.com/api-keys)

---

### Option A — pip (standard)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/crewai-project-planner.git
cd crewai-project-planner

# 2. Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Open .env and set your OPENAI_API_KEY

# 5. Run
python main.py
```

---

### Option B — Poetry (recommended)

```bash
# 1. Install Poetry if you haven't already
pip install poetry

# 2. Clone & install
git clone https://github.com/YOUR_USERNAME/crewai-project-planner.git
cd crewai-project-planner
poetry install

# 3. Configure environment
cp .env.example .env
# Open .env and set your OPENAI_API_KEY

# 4. Run
poetry run python main.py
# or, using the script shortcut defined in pyproject.toml:
poetry run plan
```

---

## Outputs

After the crew finishes (typically 1–3 minutes depending on model latency):

| File | Description |
|------|-------------|
| `output/plan.json` | Full structured `ProjectPlan` as JSON |
| `output/gantt_chart.png` | Gantt chart coloured by milestone |

### Example Gantt Chart

> *(Screenshot of a generated chart will appear here after your first run)*

![Gantt Chart](output/gantt_chart.png)

---

## Customising the Project Inputs

### Option 1 — Edit `main.py` directly

Open `main.py` and modify the `PROJECT_INPUTS` dictionary near the top:

```python
PROJECT_INPUTS = {
    "project": "Mobile App",           # Change project type
    "industry": "Healthcare",          # Change industry
    "project_objectives": "...",       # Your objectives
    "team_members": """
- Alice Smith (Project Manager)
- Bob Jones (Backend Engineer)
- Carol White (iOS Developer)
""",
    "project_requirements": """
- User authentication via OAuth2
- Patient appointment booking
- Push notifications
- HIPAA-compliant data storage
""",
}
```

### Option 2 — Environment variables (for CI / automation)

You can also override the model used:

```bash
# .env
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o        # upgrade from gpt-4o-mini for more detail
```

### Option 3 — Modify the YAML configs

- `config/agents.yaml` — change agent personas, goals, or backstories
- `config/tasks.yaml` — change task descriptions and expected output formats

The `{variable}` placeholders in both files are filled at runtime from `PROJECT_INPUTS`.

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | Your OpenAI API key |
| `OPENAI_MODEL_NAME` | No | `gpt-4o-mini` | Model to use for all agents |

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Multi-agent orchestration | `crewai` |
| LLM | OpenAI `gpt-4o-mini` |
| Structured output | `pydantic` v2 |
| Configuration | `pyyaml` |
| Gantt visualisation | `matplotlib` |
| Environment management | `python-dotenv` |

---

## License

MIT — feel free to use and adapt for your own projects.
