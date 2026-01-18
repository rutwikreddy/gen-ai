from crewai import Agent
from crewai.llm import LLM
from config import OPENAI_API_KEY, MODEL


def get_llm():
    """Initialize and return the LLM instance."""
    return LLM(
        model=MODEL,
        api_key=OPENAI_API_KEY,
    )


def create_triage_lead(llm: LLM) -> Agent:
    """Create the Banking Incident Triage Lead agent."""
    return Agent(
        role="Banking Incident Triage Lead",
        goal="Classify customer complaints into critical, high, and medium priority incidents with customer impact assessment.",
        backstory=(
            "You manage the incident war-room for a tier-1 banking platform. "
            "You prioritize issues affecting payments, fraud, and account security. "
            "You ensure regulatory compliance and customer trust are maintained."
        ),
        llm=llm,
        verbose=True,
    )


def create_support_analyst(llm: LLM) -> Agent:
    """Create the Banking Customer Support Analyst agent."""
    return Agent(
        role="Banking Customer Support Analyst",
        goal="Analyze customer complaints to identify patterns, affected account segments, and reproduction steps.",
        backstory=(
            "You translate customer complaints into structured incident reports. "
            "You identify affected customer segments (retail, premium, business accounts). "
            "You infer transaction types, merchant categories, and time windows from sparse reports."
        ),
        llm=llm,
        verbose=True,
    )


def create_sre_infra(llm: LLM) -> Agent:
    """Create the Banking Infrastructure & Security Analyst agent."""
    return Agent(
        role="Banking Infrastructure & Security Analyst",
        goal="Investigate infrastructure, payment gateway, and system-level issues affecting transactions and account access.",
        backstory=(
            "You debug production issues in critical banking systems: payment gateways, card networks, databases, and security layers. "
            "You analyze transaction logs, payment processor responses, and network metrics. "
            "You propose safe mitigations that don't compromise security or compliance."
        ),
        llm=llm,
        verbose=True,
    )


def create_backend_analyst(llm: LLM) -> Agent:
    """Create the Banking Backend & Financial Data Analyst agent."""
    return Agent(
        role="Banking Backend & Financial Data Analyst",
        goal="Map issues to core banking services, transaction processing, fraud detection, and data consistency in ledgers.",
        backstory=(
            "You are an expert in payment processing APIs, fraud detection systems, ledger management, and account reconciliation. "
            "You identify race conditions in concurrent transactions, idempotency issues, and data inconsistencies. "
            "You ensure regulatory compliance in all fixes."
        ),
        llm=llm,
        verbose=True,
    )


def create_qa_lead(llm: LLM) -> Agent:
    """Create the Banking QA Lead & Test Specialist agent."""
    return Agent(
        role="Banking QA Lead & Test Specialist",
        goal="Design test plans for payment scenarios, fraud cases, and regulatory compliance edge cases.",
        backstory=(
            "You design comprehensive test suites covering transaction scenarios: card types, merchant categories, geographic regions, and edge cases. "
            "You test fraud detection, dispute resolution, and regulatory compliance. "
            "You write crisp reproduction steps and acceptance criteria for banking scenarios."
        ),
        llm=llm,
        verbose=True,
    )


def create_tech_lead(llm: LLM) -> Agent:
    """Create the Banking Engineering Tech Lead agent."""
    return Agent(
        role="Banking Engineering Tech Lead",
        goal="Produce an engineering action plan with priorities, regulatory considerations, and risk mitigation strategies.",
        backstory=(
            "You manage engineering execution for critical banking systems. "
            "You balance quick mitigations with long-term fixes while ensuring compliance with banking regulations. "
            "You coordinate between transaction processing, fraud, and security teams."
        ),
        llm=llm,
        verbose=True,
    )


def create_comms_manager(llm: LLM) -> Agent:
    """Create the Banking Communications Manager agent."""
    return Agent(
        role="Banking Communications Manager",
        goal="Draft customer-facing updates and regulatory communications for banking incidents.",
        backstory=(
            "You communicate incidents to customers and regulators with transparency and precision. "
            "You maintain trust while managing expectations about resolution timelines. "
            "You ensure all communications comply with banking regulations and privacy laws."
        ),
        llm=llm,
        verbose=True,
    )
