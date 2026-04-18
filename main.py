"""
main.py — Entry point for the CrewAI Project Planning system.

Run:
    python main.py

Outputs:
    output/plan.json        — Structured ProjectPlan as JSON
    output/gantt_chart.png  — Gantt chart visualisation
"""

from __future__ import annotations

import json
import os
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("OPENAI_MODEL_NAME", "gpt-4o-mini")

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


PROJECT_INPUTS = {
    "project": "Website",
    "industry": "Technology",
    "project_objectives": "Create a website for a small business",
    "team_members": """
- John Doe (Project Manager)
- Jane Doe (Software Engineer)
- Bob Smith (Designer)
- Alice Johnson (QA Engineer)
- Tom Brown (QA Engineer)
""",
    "project_requirements": """
- Create a responsive design that works well on desktop and mobile devices
- Implement a modern, visually appealing user interface with a clean look
- Develop a user-friendly navigation system with intuitive menu structure
- Include an "About Us" page highlighting the company's history and values
- Design a "Services" page showcasing the business's offerings with descriptions
- Create a "Contact Us" page with a form and integrated map for communication
- Implement a blog section for sharing industry news and company updates
- Ensure fast loading times and optimize for search engines (SEO)
- Integrate social media links and sharing capabilities
- Include a testimonials section to showcase customer feedback and build trust
""",
}


def main() -> None:
    from src.crew import build_crew
    from src.models import ProjectPlan
    from src.visualizer import generate_gantt_chart

    print("\n" + "=" * 60)
    print("  CrewAI — Automated Project Planning System")
    print("=" * 60 + "\n")

    crew = build_crew()
    result = crew.kickoff(inputs=PROJECT_INPUTS)

    plan: ProjectPlan = result.pydantic

    plan_path = OUTPUT_DIR / "plan.json"
    plan_path.write_text(plan.model_dump_json(indent=2))
    print(f"\n[✓] Project plan saved to: {plan_path}")

    gantt_path = OUTPUT_DIR / "gantt_chart.png"
    generate_gantt_chart(plan, gantt_path)
    print(f"[✓] Gantt chart saved to:   {gantt_path}")

    print("\n" + "=" * 60)
    print(f"  Done! {len(plan.tasks)} tasks across {len(plan.milestones)} milestones.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
