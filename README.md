# 🤖 Agno Testing Environment

**Complete Agno agentic system deployment for Coolify v4**

Multi-agent framework with FastAPI, PostgreSQL, and comprehensive LLM support for testing and experimentation.

[![Deploy Status](https://img.shields.io/badge/Deploy-Ready-brightgreen)]() [![Coolify](https://img.shields.io/badge/Coolify-v4-blue)]() [![Python](https://img.shields.io/badge/Python-3.11-blue)]() [![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()

## 🚀 Quick Deploy

### Prerequisites
- **Server**: 8vCPU + 16GB RAM (Hetzner VPS recommended)
- **Coolify v4** instance running
- **Domain**: DNS configured (e.g., `agno.gohorse.srv.br`)
- **API Keys**: OpenAI, Anthropic, Google, Groq, Perplexity, XAI, OpenRouter

### 1-Click Coolify v4 Deployment

1. **Create New Resource** in Coolify
2. **Select**: `Git Based` → `Public Repository`
3. **Repository URL**: `https://github.com/lipeeh/agno-testing-environment`
4. **Build Pack**: `Docker Compose`
5. **Compose File**: `compose.yml`
6. **Configure Environment Variables** (see below)
7. **Deploy** 🚀

## 🔐 Environment Variables

Configure these **required** variables in Coolify:

```bash
# Database
POSTGRES_PASSWORD=your_super_secure_password

# LLM API Keys (ALL REQUIRED)
OPENAI_API_KEY=sk-proj-your_key
ANTHROPIC_API_KEY=sk-ant-your_key
GOOGLE_API_KEY=AIzaSy_your_key
GROQ_API_KEY=gsk_your_key
PERPLEXITY_API_KEY=pplx-your_key
XAI_API_KEY=xai-your_key
OPENROUTER_API_KEY=sk-or-your_key
```

> **⚠️ Security**: Never commit real API keys! Use the `.env.example` template.

## 🏗️ Architecture

### Services
- **agno-app**: FastAPI application with AgentOS runtime
- **postgres**: PostgreSQL 16 with pgvector extension

### Features
- ✅ **Multi-Agent System**: 7 agents (one per LLM provider)
- ✅ **Team Management**: Organized teams per model
- ✅ **Workflow Engine**: Automated multi-step processes
- ✅ **Knowledge Base**: Vector-powered RAG capabilities
- ✅ **Session Management**: Persistent conversations and memories
- ✅ **Control Plane**: Web interface for testing and monitoring
- ✅ **Health Monitoring**: Built-in health checks and metrics
- ✅ **Data Persistence**: PostgreSQL with volume persistence

## 🌐 Endpoints

Once deployed, access these endpoints:

| Endpoint | Description |
|----------|-------------|
| `/` | Main AgentOS interface |
| `/docs` | FastAPI interactive documentation |
| `/playground` | Control Plane for agent testing |
| `/health` | System health and status |

## 🤖 Supported Models

| Provider | Model | Capabilities |
|----------|-------|-------------|
| **OpenAI** | GPT-4o | General purpose, coding, analysis |
| **Anthropic** | Claude 3.5 Sonnet | Reasoning, writing, research |
| **Google** | Gemini 1.5 Pro | Multimodal, long context |
| **Groq** | Llama 3.1 70B | Fast inference, open source |
| **Perplexity** | Sonar Huge | Real-time web search |
| **XAI** | Grok Beta | Conversational AI |
| **OpenRouter** | Multiple | Access to various models |

## 📊 System Requirements

### Minimum
- **CPU**: 4 vCPU
- **RAM**: 8GB
- **Storage**: 20GB SSD
- **Network**: 1Gbps

### Recommended
- **CPU**: 8+ vCPU
- **RAM**: 16GB+
- **Storage**: 50GB+ SSD
- **Network**: 1Gbps+

## 🔧 Development

### Local Development

```bash
# Clone repository
git clone https://github.com/lipeeh/agno-testing-environment.git
cd agno-testing-environment

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Run with Docker Compose
docker-compose up -d

# Access local instance
open http://localhost:80
```

### File Structure

```
agno-testing-environment/
├── compose.yml           # Docker Compose configuration
├── Dockerfile            # Application container
├── requirements.txt      # Python dependencies
├── app/
│   └── main.py          # FastAPI application with AgentOS
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚨 Troubleshooting

### Common Issues

**❌ API Key Errors**
- Verify all API keys are valid and active
- Check rate limits and usage quotas
- Ensure environment variables are properly set

**❌ Database Connection Failed**
- Wait for PostgreSQL health check to pass
- Verify `POSTGRES_PASSWORD` is set correctly
- Check Docker network connectivity

**❌ Memory Issues**
- Ensure minimum 8GB RAM available
- Monitor resource usage in Coolify
- Consider upgrading server specifications

### Health Check

Monitor system status:

```bash
curl https://agno.gohorse.srv.br/health
```

Expected response:
```json
{
  "status": "healthy",
  "agents": 7,
  "teams": 7, 
  "workflows": 7,
  "models": ["openai", "anthropic", "gemini", "groq", "perplexity", "grok", "openrouter"],
  "database": "connected"
}
```

## 🎯 Testing Scenarios

### Agent Capabilities
- **Code Generation**: Complex programming tasks
- **Data Analysis**: CSV/JSON processing and insights
- **Research**: Web search and information synthesis
- **Creative Writing**: Articles, documentation, creative content
- **Problem Solving**: Multi-step reasoning and analysis
- **Team Collaboration**: Multi-agent workflows

### Workflow Examples
- **Research Pipeline**: Search → Analyze → Summarize → Report
- **Code Review**: Analyze → Test → Document → Optimize
- **Content Creation**: Research → Draft → Review → Publish

## 📈 Monitoring

### Built-in Metrics
- Agent response times
- Token usage per model
- Database query performance
- Memory and CPU utilization
- Error rates and health status

### Coolify Integration
- Real-time logs
- Resource monitoring
- Automatic restarts
- SSL certificate management
- Domain routing

## 🔒 Security

- **Environment Isolation**: Docker containers
- **API Key Management**: Secure environment variables
- **HTTPS**: Automatic SSL via Let's Encrypt
- **Database Security**: Isolated PostgreSQL instance
- **Access Control**: Configurable authentication

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For issues and questions:

- **GitHub Issues**: [Create Issue](https://github.com/lipeeh/agno-testing-environment/issues)
- **Agno Documentation**: [docs.agno.com](https://docs.agno.com)
- **Coolify Documentation**: [coolify.io/docs](https://coolify.io/docs)

---

**Built with ❤️ for the Agno community**

*Ready to deploy your agentic AI system? Click the deploy button above!* 🚀