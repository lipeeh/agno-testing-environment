"""Model registry and AgentOS app wiring with tools integration"""

import os
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.os import AgentOS
from agno.team import Team
from agno.vectordb.pgvector import PgVector
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step
from fastapi.middleware.cors import CORSMiddleware

# Import tools
from tools.web.google_search import GoogleSearchTools
from tools.system.file_tools import FileTools
from tools.system.shell_tools import ShellTools

# Providers
try:
    from agno.models.openai import OpenAIChat
except ImportError:
    OpenAIChat = None
try:
    from agno.models.anthropic import Claude
except ImportError:
    Claude = None
try:
    from agno.models.groq import Groq
except ImportError:
    Groq = None

# ---------- Config ----------
# Database URL with new PostgreSQL credentials
DB_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("DB_URL")
    or os.getenv("AGENTOS_DATABASE_URL")
    or "postgresql+psycopg://postgres:AkqT0Q5kVnCXyIgYPXc2SsTmljgI1DuOTpiXoS5tVAHjl1zKQFFEAYUvlT3pht5k@j8k08cosc8k0g0s0wcsocogo:5432/postgres"
)
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+psycopg://", 1)
logger.info(f"DB: {DB_URL.split('@')[1] if '@' in DB_URL else DB_URL}")

# CORS
DEFAULT_ALLOWED: List[str] = [
    "https://agno.gohorse.srv.br",
    "http://ikccgcgkk08gcgw8kkw8c4cg.65.108.223.117.sslip.io",
    "http://localhost:3000",
    "https://localhost:3000",
]
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
ALLOWED_ORIGINS = [FRONTEND_ORIGIN] + DEFAULT_ALLOWED if FRONTEND_ORIGIN else DEFAULT_ALLOWED

# ---------- DB / VectorDB ----------
db = PostgresDb(db_url=DB_URL)
vector_db = PgVector(db_url=DB_URL, table_name="knowledge_vectors")

# ---------- Tools initialization ----------
logger.info("Initializing tools...")
google_search = GoogleSearchTools()
file_tools = FileTools()
shell_tools = ShellTools()
logger.info("Tools initialized: GoogleSearch, FileTools, ShellTools")

# ---------- Model registry ----------
models: Dict[str, Any] = {}

# OpenAI lineup (enable if key present)
if os.getenv("OPENAI_API_KEY") and OpenAIChat:
    models.update(
        {
            "gpt-4o": OpenAIChat(id="gpt-4o"),
            "gpt-4.1": OpenAIChat(id="gpt-4.1"),
            "gpt-4o-mini": OpenAIChat(id="gpt-4o-mini"),
        }
    )
    logger.info("OpenAI: gpt-4o, gpt-4.1, gpt-4o-mini enabled")

# Anthropic lineup
if os.getenv("ANTHROPIC_API_KEY") and Claude:
    models.update(
        {
            "claude-sonnet-4": Claude(id="claude-3-5-sonnet-20241022"),
            "claude-opus-4.1": Claude(id="claude-3-opus-20240229"),
            "claude-haiku-3.5": Claude(id="claude-3-5-haiku-20241022"),
        }
    )
    logger.info("Anthropic: sonnet, opus, haiku enabled")

# Groq lineup (replace deprecated)
if os.getenv("GROQ_API_KEY") and Groq:
    models.update(
        {
            "llama-3.3-70b": Groq(id="llama-3.3-70b"),
            "llama-3.1-8b-instant": Groq(id="llama-3.1-8b-instant"),
            "mixtral-8x7b-32768": Groq(id="mixtral-8x7b-32768"),
        }
    )
    logger.info("Groq: 3.3-70b, 3.1-8b-instant, mixtral enabled")

if not models:
    logger.warning("No models enabled — check API keys.")

# ---------- Knowledge ----------
knowledge = None
try:
    knowledge = Knowledge(
        name="Agno Knowledge Base",
        description="Central knowledge repository",
        vector_db=vector_db,
    )
except Exception as e:
    logger.warning(f"Knowledge disabled: {e}")

# ---------- Agents / Teams / Workflows ----------
agents: List[Agent] = []
teams: List[Team] = []
workflows: List[Workflow] = []

# Choose defaults
DEFAULTS = {
    "openai": "gpt-4o",
    "anthropic": "claude-sonnet-4",
    "groq": "llama-3.3-70b",
}

for name, model in models.items():
    provider = (
        "openai" if name.startswith("gpt") else "anthropic" if name.startswith("claude") else "groq"
    )
    
    # Create agent with tools integrated
    agent = Agent(
        id=f"agent-{name}",
        name=f"Agent {name}",
        model=model,
        db=db,
        enable_session_summaries=True,
        enable_user_memories=True,
        add_history_to_context=True,
        num_history_runs=5,
        add_datetime_to_context=True,
        markdown=True,
        description=f"Agent using {name} with Google Search, File Operations, and Shell Tools",
        knowledge=knowledge,
        add_knowledge_to_context=True,
        search_knowledge=True,
        # Register tools with agent
        tools=[
            google_search.search_web,
            google_search.search_images,
            file_tools.create_file,
            file_tools.read_file,
            file_tools.list_files,
            file_tools.delete_file,
            file_tools.get_file_info,
            shell_tools.execute_command,
            shell_tools.list_allowed_commands,
            shell_tools.get_system_info
        ]
    )
    agents.append(agent)
    
    logger.info(f"Agent {name} created with {len(agent.tools)} tools")

    team = Team(
        id=f"team-{provider}",
        name=f"Team {provider}",
        model=model,
        db=db,
        members=[agent],
        enable_user_memories=True,
        description=f"Team for provider {provider} with integrated tools",
    )
    teams.append(team)

    wf = Workflow(
        id=f"workflow-{name}",
        name=f"Workflow {name}",
        description=f"Workflow for {name}",
        db=db,
        steps=[Step(name="analysis", description="Analyze and respond with tools", agent=agent)],
    )
    workflows.append(wf)

logger.info(f"Created {len(agents)} agents, {len(teams)} teams, {len(workflows)} workflows")

# ---------- App ----------
agent_os = AgentOS(
    description="Complete Agno Testing Environment with Integrated Tools",
    agents=agents,
    teams=teams,
    workflows=workflows,
    knowledge=[knowledge] if knowledge else [],
    interfaces=[],
)

app = agent_os.get_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "ok", 
        "origins": ALLOWED_ORIGINS, 
        "models": list(models.keys()),
        "agents_with_tools": len(agents),
        "tools_per_agent": len(agents[0].tools) if agents else 0
    }

@app.get("/")
async def root():
    return {
        "name": "AgentOS API", 
        "description": "Complete Agno Testing Environment with Integrated Tools", 
        "version": "1.0.0",
        "tools_enabled": ["GoogleSearch", "FileTools", "ShellTools"]
    }

@app.get("/tools")
async def tools_info():
    """Endpoint to check available tools"""
    if not agents:
        return {"error": "No agents available"}
    
    agent_tools = []
    for agent in agents[:1]:  # Show tools from first agent
        tools_info = []
        for tool in agent.tools:
            tools_info.append({
                "name": tool.__name__ if hasattr(tool, '__name__') else str(tool),
                "doc": tool.__doc__ if hasattr(tool, '__doc__') else None
            })
        agent_tools.append({
            "agent_id": agent.id,
            "tools_count": len(agent.tools),
            "tools": tools_info
        })
    
    return {
        "total_agents": len(agents),
        "sample_agent_tools": agent_tools
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)