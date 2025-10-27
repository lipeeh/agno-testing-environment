"""AgentOS FastAPI Application for Production Deployment"""

from pathlib import Path
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Anthropic
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.os import AgentOS
from agno.team import Team
from agno.vectordb.pgvector import PgVector
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow
import os

# Database configuration
db_url = os.getenv("DB_URL", "postgresql+psycopg://agno_user:password@postgres:5432/agno_db")
db = PostgresDb(db_url=db_url)

# Vector database for knowledge
vector_db = PgVector(
    db_url=db_url, 
    table_name="knowledge_vectors"
)

# Configure models based on available API keys
models = {}

if os.getenv("OPENAI_API_KEY"):
    models["openai"] = OpenAIChat(model="gpt-4o")

if os.getenv("ANTHROPIC_API_KEY"):
    models["anthropic"] = Anthropic(model="claude-3-5-sonnet-20241022")

if os.getenv("GOOGLE_API_KEY"):
    models["gemini"] = Gemini(model="gemini-1.5-pro")

if os.getenv("GROQ_API_KEY"):
    models["groq"] = Groq(model="llama-3.1-70b-versatile")

# Add Perplexity via OpenRouter
if os.getenv("PERPLEXITY_API_KEY"):
    from agno.models.openrouter import OpenRouter
    models["perplexity"] = OpenRouter(
        model="perplexity/llama-3.1-sonar-huge-128k-online",
        api_key=os.getenv("PERPLEXITY_API_KEY")
    )

# Add XAI Grok via OpenRouter  
if os.getenv("XAI_API_KEY"):
    from agno.models.openrouter import OpenRouter
    models["grok"] = OpenRouter(
        model="x-ai/grok-beta",
        api_key=os.getenv("XAI_API_KEY")
    )

# Add OpenRouter models
if os.getenv("OPENROUTER_API_KEY"):
    from agno.models.openrouter import OpenRouter
    models["openrouter"] = OpenRouter(
        model="anthropic/claude-3.5-sonnet",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

# Setup basic agents with multiple model support
agents = []
teams = []
workflows = []

for model_name, model in models.items():
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
        description=f"AI Agent powered by {model_name}"
    )
    agents.append(agent)
    
    # Create a team for each model
    team = Team(
        id=f"team-{model_name}",
        name=f"Team {model_name.title()}",
        model=model,
        db=db,
        members=[agent],
        enable_user_memories=True,
        description=f"Team using {model_name} model"
    )
    teams.append(team)
    
    # Create a basic workflow
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
        ]
    )
    workflows.append(workflow)

# Setup knowledge base
knowledge = Knowledge(
    name="Agno Knowledge Base",
    description="Central knowledge repository for all agents",
    contents_db=db,
    vector_db=vector_db,
)

# Setup AgentOS
agent_os = AgentOS(
    description="Complete Agno Testing Environment",
    agents=agents,
    teams=teams,
    workflows=workflows,
    knowledge=[knowledge],
    db=db
)

# Get the FastAPI app
app = agent_os.get_app()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "agents": len(agents),
        "teams": len(teams),
        "workflows": len(workflows),
        "models": list(models.keys()),
        "database": "connected" if db else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)