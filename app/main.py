"""AgentOS FastAPI Application with CORS hardened for production domains"""

import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Core Agno imports
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.os import AgentOS
from agno.team import Team
from agno.vectordb.pgvector import PgVector
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step

# FastAPI & CORS
from fastapi.middleware.cors import CORSMiddleware

# AG-UI interface (disabled until correct import path/version is confirmed)
AGUI = None

# Model imports with error handling
try:
    from agno.models.openai import OpenAIChat
except ImportError:
    logger.warning("OpenAI model not available")
    OpenAIChat = None

try:
    from agno.models.anthropic import Claude
except ImportError:
    logger.warning("Anthropic model not available")
    Claude = None

try:
    from agno.models.google import Gemini
except ImportError:
    logger.warning("Google model not available")
    Gemini = None

try:
    from agno.models.groq import Groq
except ImportError:
    logger.warning("Groq model not available")
    Groq = None

# Database configuration (prefer single DATABASE_URL)
db_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL") or os.getenv("AGENTOS_DATABASE_URL") or "postgresql+psycopg://agno_user:password@postgres:5432/agno_db"
logger.info(f"Connecting to database: {db_url.split('@')[1] if '@' in db_url else db_url}")

# Normalize SQLAlchemy URL if using postgres:// scheme
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)

db = PostgresDb(db_url=db_url)

# Vector database for knowledge
vector_db = PgVector(
    db_url=db_url,
    table_name="knowledge_vectors",
)

# Configure models based on available API keys
models: Dict[str, Any] = {}

if os.getenv("OPENAI_API_KEY") and OpenAIChat:
    try:
        models["openai"] = OpenAIChat(id="gpt-4o")
        logger.info("✅ OpenAI model configured")
    except Exception as e:
        logger.error(f"❌ Failed to configure OpenAI: {e}")

if os.getenv("ANTHROPIC_API_KEY") and Claude:
    try:
        models["anthropic"] = Claude(id="claude-3-5-sonnet-20241022")
        logger.info("✅ Anthropic model configured")
    except Exception as e:
        logger.error(f"❌ Failed to configure Anthropic: {e}")

if os.getenv("GOOGLE_API_KEY") and Gemini:
    try:
        models["gemini"] = Gemini(model="gemini-1.5-pro")
        logger.info("✅ Google model configured")
    except Exception as e:
        logger.error(f"❌ Failed to configure Google: {e}")

if os.getenv("GROQ_API_KEY") and Groq:
    try:
        models["groq"] = Groq(id="llama-3.1-70b-versatile")
        logger.info("✅ Groq model configured")
    except Exception as e:
        logger.error(f"❌ Failed to configure Groq: {e}")

if not models:
    logger.warning("⚠️  No LLM models configured. Creating basic agent for testing.")
    models["basic"] = None

logger.info(f"Configured {len(models)} model(s): {list(models.keys())}")

# Setup knowledge base
knowledge = None
try:
    knowledge = Knowledge(
        name="Agno Knowledge Base",
        description="Central knowledge repository for all agents",
        vector_db=vector_db,
    )
    logger.info("✅ Knowledge base configured")
except Exception as e:
    logger.error(f"❌ Failed to configure knowledge base: {e}")

# Setup agents, teams, and workflows
agents = []
teams = []
workflows = []

for model_name, model in models.items():
    try:
        agent = Agent(
            name=f"Agent {model_name.title()}",
            model=model,
            db=db,
            enable_session_summaries=True,
            enable_user_memories=True,
            add_history_to_context=True,
            num_history_runs=5,
            add_datetime_to_context=True,
            markdown=True,
            description=f"AI Agent powered by {model_name}",
            knowledge=knowledge,
            add_knowledge_to_context=True,
            search_knowledge=True,
        )
        agents.append(agent)

        team = Team(
            id=f"team-{model_name}",
            name=f"Team {model_name.title()}",
            model=model,
            db=db,
            members=[agent],
            enable_user_memories=True,
            description=f"Team using {model_name} model",
        )
        teams.append(team)

        workflow = Workflow(
            id=f"workflow-{model_name}",
            name=f"Workflow {model_name.title()}",
            description=f"Basic workflow using {model_name}",
            db=db,
            steps=[
                Step(
                    name="analysis",
                    description="Analyze the input and provide insights",
                    agent=agent,
                )
            ],
        )
        workflows.append(workflow)

        logger.info(f"✅ Created agent, team, and workflow for {model_name}")

    except Exception as e:
        logger.error(f"❌ Failed to create resources for {model_name}: {e}")

# Setup AgentOS (without AG-UI for now)
interfaces = []

try:
    agent_os = AgentOS(
        description="Complete Agno Testing Environment",
        agents=agents,
        teams=teams,
        workflows=workflows,
        knowledge=[knowledge] if knowledge else [],
        interfaces=interfaces,
    )
    logger.info("✅ AgentOS initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize AgentOS: {e}")
    agent_os = AgentOS(
        description="Minimal Agno Testing Environment",
        agents=[],
        teams=[],
        workflows=[],
        knowledge=[],
        interfaces=[],
    )

# Get the FastAPI app
app = agent_os.get_app()

# Enable CORS (hardened)
DEFAULT_ALLOWED = [
    "https://agno.gohorse.srv.br",
    "http://ikccgcgkk08gcgw8kkw8c4cg.65.108.223.117.sslip.io",
    "http://localhost:3000",
    "https://localhost:3000",
]
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
ALLOWED_ORIGINS = [FRONTEND_ORIGIN] + DEFAULT_ALLOWED if FRONTEND_ORIGIN else DEFAULT_ALLOWED

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "origins": ALLOWED_ORIGINS}

@app.get("/")
async def root():
    return {
        "name": "AgentOS API",
        "description": "Complete Agno Testing Environment",
        "id": agent_os.id if hasattr(agent_os, "id") else "unknown",
        "version": "1.0.0",
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Agno Testing Environment...")
    uvicorn.run(app, host="0.0.0.0", port=80)
}