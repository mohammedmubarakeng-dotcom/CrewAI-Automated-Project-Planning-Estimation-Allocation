import os
import yaml
from pathlib import Path

from crewai import Agent, Task, Crew

from src.models import ProjectPlan

CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_configs() -> tuple[dict, dict]:
    with open(CONFIG_DIR / "agents.yaml", "r") as f:
        agents_config = yaml.safe_load(f)
    with open(CONFIG_DIR / "tasks.yaml", "r") as f:
        tasks_config = yaml.safe_load(f)
    return agents_config, tasks_config


def build_crew() -> Crew:
    agents_config, tasks_config = _load_configs()

    project_planning_agent = Agent(config=agents_config["project_planning_agent"])
    estimation_agent = Agent(config=agents_config["estimation_agent"])
    resource_allocation_agent = Agent(config=agents_config["resource_allocation_agent"])

    task_breakdown = Task(
        config=tasks_config["task_breakdown"],
        agent=project_planning_agent,
    )

    time_resource_estimation = Task(
        config=tasks_config["time_resource_estimation"],
        agent=estimation_agent,
    )

    resource_allocation = Task(
        config=tasks_config["resource_allocation"],
        agent=resource_allocation_agent,
        output_pydantic=ProjectPlan,
    )

    crew = Crew(
        agents=[
            project_planning_agent,
            estimation_agent,
            resource_allocation_agent,
        ],
        tasks=[
            task_breakdown,
            time_resource_estimation,
            resource_allocation,
        ],
        verbose=True,
    )

    return crew
