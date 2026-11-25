# LangGraph Research Agent

A Python research workflow built with LangGraph that creates analyst personas, conducts source-backed interviews, and compiles their findings into a structured final report.

## Overview

The project is organized as a state-driven LangGraph application:

1. **Create analysts** – Generates multiple analyst personas for a topic.
2. **Human feedback** – Allows the analyst set to be reviewed or regenerated before research begins.
3. **Conduct interviews** – Runs parallel interview subgraphs for each analyst.
4. **Search the web** – Uses Tavily to retrieve supporting sources for each interview.
5. **Write a section** – Converts interview findings and sources into an analyst-specific section.
6. **Finalize the report** – Combines the sections, introduction, and conclusion into a final report.

The main implementation lives under `src/langgraph_research_agent/`:

- `agent.py` – Orchestrates the complete research graph.
- `creating_analysts.py` – Generates and reviews analyst personas.
- `answering_questions.py` – Runs the interview, search, answer, and section-writing subgraph.
- `utils/nodes.py` – Graph node implementations.
- `utils/edges.py` – Routing and conditional graph logic.
- `utils/states.py` – Typed state definitions.
- `utils/models.py` – OpenAI chat model configuration.
- `utils/prompts.py` – Prompts for analysts, interviews, searches, and reports.
- `utils/objects.py` – Pydantic models for structured outputs.

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) for dependency and environment management
- An OpenAI API key
- A Tavily API key
- LangGraph CLI (included by the LangGraph ecosystem or installable separately)

## Installation

Clone the repository:

```bash
git clone https://github.com/Karim317/LangGraph_Research_Agent.git
cd LangGraph_Research_Agent
```

Create a virtual environment and install dependencies with `uv`:

```bash
uv sync
```

Activate the environment if needed:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Environment Variables

Create a `.env` file in the repository root:

```dotenv
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

| Variable | Required | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Used by `ChatOpenAI` for generating analysts, questions, answers, sections, and the final report. |
| `TAVILY_API_KEY` | Yes | Used by `TavilySearch` to find web sources during interviews. |

A `.env.example` file is not currently present in the repository, so the variables above are inferred from the implementation. The project loads `.env` through `python-dotenv`, and `langgraph.json` also points LangGraph to `.env`.

> Keep API keys secret. `.env` is excluded by `.gitignore` and should not be committed.

## Running with LangGraph

The repository configuration is in `langgraph.json`. It exposes these graphs:

- `create_analysts`
- `question_answer_graph`
- `agent_graph`

Start the LangGraph development server:

```bash
uv run langgraph dev
```

Then open the URL printed by LangGraph CLI, usually the LangGraph Studio or API endpoint shown in the terminal.

Use `agent_graph` for the complete workflow. Example input state:

```json
{
  "topic": "The future of small modular nuclear reactors",
  "max_analysts": 3,
  "human_analyst_feedback": null
}
```

The workflow can pause at the human-feedback step. Approve the generated analysts with:

```text
okay
```

Or provide feedback to regenerate them:

```text
Add a policy analyst and a grid-infrastructure engineer
```

## Direct Python Usage

The compiled research graph can also be invoked from Python:

```python
from langgraph_research_agent.agent import graph

initial_state = {
    "topic": "The impact of artificial intelligence on software engineering",
    "max_analysts": 3,
}

for event in graph.stream(initial_state, stream_mode="updates"):
    print(event)
```

For the standalone analyst-creation graph:

```python
from langgraph_research_agent.creating_analysts import graph

result = graph.invoke({
    "topic": "Renewable energy storage",
    "max_analysts": 3,
    "human_analyst_feedback": None,
})

print(result)
```

For the standalone interview subgraph:

```python
from langgraph_research_agent.answering_questions import question_answer_graph

print(question_answer_graph)
```

## Project Configuration

- `pyproject.toml` defines Python 3.11+, dependencies, package metadata, and the `langgraph-research-agent` console script.
- `uv.lock` contains the resolved dependency versions.
- `langgraph.json` defines package dependencies, graph entry points, and the environment file.

## Dependencies

Key libraries used by the project:

- `langgraph` – Graph orchestration and state management
- `langchain` / `langchain-core` – Messages and model abstractions
- `langchain-openai` – OpenAI chat models
- `langchain-tavily` – Tavily web search
- `python-dotenv` – Environment variable loading
- `colorama` – Terminal formatting support

## Development Notes

The main graph is configured with the OpenAI model `gpt-4o` at temperature `0` in `utils/models.py`. Web searches request up to three Tavily results per search operation.
