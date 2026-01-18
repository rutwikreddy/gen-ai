"""
Main entry point for the CrewAI incident management system.
"""
from crew import create_crew


def main():
    """Execute the incident analysis crew."""
    crew = create_crew()
    result = crew.kickoff()
    
    print("\n" + "=" * 80)
    print("FINAL INCIDENT + ENGINEERING REPORT")
    print("=" * 80 + "\n")
    print(result)


if __name__ == "__main__":
    main()
