import json
from crewai import Task
from crewai.agent import Agent
from config import ORG_CONTEXT
from complaints import COMPLAINT_TEXT


def create_task0_context(agent: Agent) -> Task:
    """Create context risk assessment task."""
    return Task(
        description=(
            "You are given org/system context and recent release notes.\n\n"
            f"ORG CONTEXT (memory):\n{json.dumps(ORG_CONTEXT, indent=2)}\n\n"
            "Summarize the key risk areas implied by recent changes and known incidents.\n"
            "Output:\n"
            "1) 5-8 bullet 'risk hypotheses'\n"
            "2) What you would watch first in metrics/logs\n"
            "3) Any immediate suspicion about which complaints map to known incidents"
        ),
        expected_output="Risk hypotheses + what-to-check list.",
        agent=agent,
    )


def create_task1_support(agent: Agent) -> Task:
    """Create support analysis task."""
    return Task(
        description=(
            f"Analyze the following customer complaints:\n{COMPLAINT_TEXT}\n\n"
            "Create a structured support summary:\n"
            "- Group into incident buckets\n"
            "- For each bucket: user impact, affected platform (mobile/web), time sensitivity\n"
            "- Provide probable reproduction hints\n"
            "- Add severity guess (P0/P1/P2) with justification\n"
            "Use the org context memory to map issues to past incidents or releases."
        ),
        expected_output="Structured incident buckets with severity and repro hints.",
        agent=agent,
    )


def create_task2_sre(agent: Agent) -> Task:
    """Create SRE/infrastructure analysis task."""
    return Task(
        description=(
            "Investigate infra-level signals for each incident bucket.\n"
            "Use these tools (call them conceptually; they return mock outputs):\n"
            "- mock_log_search(query)\n"
            "- mock_metrics_fetch(metric)\n\n"
            "Output per bucket:\n"
            "- Key metrics snapshot\n"
            "- Log evidence\n"
            "- Likely infra causes\n"
            "- Safe mitigation steps (feature flag, rollback, scaling, CDN config, cache tuning)\n"
            "- Confidence score (0-100) and assumptions"
        ),
        expected_output="Infra-focused RCA with mitigations and confidence.",
        agent=agent,
    )


def create_task3_backend(agent: Agent) -> Task:
    """Create backend/data analysis task."""
    return Task(
        description=(
            "Investigate backend/data causes for each incident bucket.\n"
            "Use these tools (conceptually):\n"
            "- mock_log_search(query)\n"
            "- mock_db_query(sql)\n\n"
            "Output per bucket:\n"
            "- Suspected service/component\n"
            "- Data consistency risks\n"
            "- Root cause hypotheses\n"
            "- Proposed code-level fixes\n"
            "- Idempotency + retry handling recommendations\n"
            "- Confidence score and what extra data you need"
        ),
        expected_output="Backend RCA mapped to services + fixes.",
        agent=agent,
    )


def create_task4_qa(agent: Agent) -> Task:
    """Create QA planning task."""
    return Task(
        description=(
            "Create a QA plan based on the incidents.\n"
            "For each bucket:\n"
            "- Repro steps (as precise as possible)\n"
            "- Device/OS/browser matrix\n"
            "- Test cases (manual + automated)\n"
            "- Regression suite additions\n"
            "- Acceptance criteria for 'fixed'\n"
            "Also propose a release validation checklist for hotfix deployment."
        ),
        expected_output="QA repro + test plan + acceptance criteria.",
        agent=agent,
    )


def create_task5_comms(agent: Agent) -> Task:
    """Create communications task."""
    return Task(
        description=(
            "Draft customer communication artifacts.\n"
            "Output:\n"
            "1) Status page incident update (short, clear)\n"
            "2) Support macro replies for each complaint type\n"
            "3) Temporary workarounds (if any)\n"
            "Rules: No blaming vendors; be transparent; mention impact + what we're doing."
        ),
        expected_output="Status update + support macros + workarounds.",
        agent=agent,
    )


def create_task6_plan(agent: Agent) -> Task:
    """Create engineering action plan task."""
    return Task(
        description=(
            "Synthesize all prior findings into an engineering-ready action plan.\n"
            "Output MUST include:\n"
            "A) Prioritized list (P0/P1/P2) with reasoning\n"
            "B) Owners by role (SRE/Backend/Mobile/Web/QA)\n"
            "C) Quick mitigations vs long-term fixes\n"
            "D) Rollback/feature-flag plan\n"
            "E) Monitoring/alerts to add\n"
            "F) Bug tickets list (title, description, acceptance criteria)\n"
            "G) A postmortem outline (timeline, root cause, contributing factors, action items)\n\n"
            "Also produce a small JSON block at the end with:\n"
            "{ incidents: [...], priorities: {...}, next_24h: [...], next_7d: [...] }"
        ),
        expected_output="Full action plan + tickets + postmortem outline + JSON summary.",
        agent=agent,
    )
