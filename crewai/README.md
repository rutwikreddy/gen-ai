# CrewAI Incident Management System

Modular Python implementation of a CrewAI-based incident triage and analysis system for the Euron Learning App.

## Project Structure

```
crewai/
├── config.py          # Configuration and organization context
├── complaints.py      # Complaint data
├── agents.py          # Agent definitions
├── tasks.py           # Task definitions
├── crew.py            # Crew orchestration
├── main.py            # Entry point
├── .env.example       # Environment variable template
└── .gitignore         # Git ignore file
```

## Setup

### 1. Install Dependencies

```bash
pip install crewai openai python-dotenv
```

### 2. Configure API Key

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 3. Run the Analysis

```bash
python main.py
```

## Module Descriptions

### `config.py`
- Stores organization context (product stack, known incidents, SLA targets)
- Loads API key from environment variables
- Contains model configuration

### `complaints.py`
- Defines customer complaints data
- Formats complaint text for task processing

### `agents.py`
- Defines 7 specialized agents:
  - Incident Triage Lead
  - Customer Support Analyst
  - SRE / Infra Analyst
  - Backend & Data Analyst
  - QA Lead
  - Engineering Tech Lead
  - Communications Manager

### `tasks.py`
- Creates 7 sequential tasks for incident analysis
- Each task targets a specific aspect of incident management

### `crew.py`
- Orchestrates agents and tasks
- Configures the crew with sequential process

### `main.py`
- Entry point for the application
- Executes the crew and prints final report

## Security Notes

- **Never commit `.env` files** with actual API keys
- The `.env.example` file shows the structure without sensitive data
- API keys are loaded from environment variables at runtime
- Use `.gitignore` to prevent `.env` from being committed

## Output

The system produces:
- Risk assessments and hypotheses
- Structured incident analysis
- Infrastructure-level RCA
- Backend/data analysis
- QA test plans
- Customer communication templates
- Engineering action plan with priorities and tickets
