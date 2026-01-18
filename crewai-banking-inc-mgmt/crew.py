from crewai import Crew, Process
from agents import (
    get_llm,
    create_triage_lead,
    create_support_analyst,
    create_sre_infra,
    create_backend_analyst,
    create_qa_lead,
    create_tech_lead,
    create_comms_manager,
)
from tasks import (
    create_task0_context,
    create_task1_support,
    create_task2_sre,
    create_task3_backend,
    create_task4_qa,
    create_task5_comms,
    create_task6_plan,
)


def create_crew() -> Crew:
    """
    Create and return a configured CrewAI instance with all agents and tasks.
    
    Returns:
        Crew: Configured crew with sequential process
    """
    # Initialize LLM
    llm = get_llm()
    
    # Create agents
    triage_lead = create_triage_lead(llm)
    support_analyst = create_support_analyst(llm)
    sre_infra = create_sre_infra(llm)
    backend_analyst = create_backend_analyst(llm)
    qa_lead = create_qa_lead(llm)
    tech_lead = create_tech_lead(llm)
    comms_manager = create_comms_manager(llm)
    
    # Create tasks
    task0 = create_task0_context(triage_lead)
    task1 = create_task1_support(support_analyst)
    task2 = create_task2_sre(sre_infra)
    task3 = create_task3_backend(backend_analyst)
    task4 = create_task4_qa(qa_lead)
    task5 = create_task5_comms(comms_manager)
    task6 = create_task6_plan(tech_lead)
    
    # Create and return crew
    return Crew(
        agents=[triage_lead, support_analyst, sre_infra, backend_analyst, qa_lead, comms_manager, tech_lead],
        tasks=[task0, task1, task2, task3, task4, task5, task6],
        process=Process.sequential,
        verbose=True,
    )
