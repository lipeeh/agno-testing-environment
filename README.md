# 🤖 Agno Testing Environment

**Complete Agno agentic system deployment for Coolify v4**

Multi-agent framework with FastAPI, PostgreSQL, and comprehensive LLM support for testing and experimentation.

[![Deploy Status](https://img.shields.io/badge/Deploy-Ready-brightgreen)]() [![Coolify](https://img.shields.io/badge/Coolify-v4-blue)]() [![Python](https://img.shields.io/badge/Python-3.11-blue)]() [![Docker](https://img.shields.io/badge/Docker-Compose-blue)][]

## 🚀 Quick Deploy

### Prerequisites
- **Server**: 8vCPU + 16GB RAM (Hetzner VPS recommended)
- **Coolify v4** instance running
- **Domain**: DNS configured (e.g., `agno.gohorse.srv.br`)
- **API Keys**: At least one LLM provider (OpenAI recommended for testing)

### 1-Click Coolify v4 Deployment

1. **Create New Resource** in Coolify
2. **Select**: `Git Based` → `Public Repository`
3. **Repository URL**: `https://github.com/lipeeh/agno-testing-environment`
4. **Build Pack**: `Docker Compose`
5. **Compose File**: `compose.yml`
6. **Configure Environment Variables** (see below)
7. **Deploy** 🚀

## 🔐 Environment Variables

### Required Variables
```bash
# Database (REQUIRED)
POSTGRES_PASSWORD=your_super_secure_password
```

### LLM API Keys (At least one recommended)
```bash
# OpenAI (Recommended for testing)
OPENAI_API_KEY=sk-proj-your_key

# Optional: Additional providers
ANTHROPIC_API_KEY=sk-ant-your_key
GOOGLE_API_KEY=AIzaSy_your_key
GROQ_API_KEY=gsk_your_key
PERPLEXITY_API_KEY=pplx-your_key
XAI_API_KEY=xai-your_key
OPENROUTER_API_KEY=sk-or-your_key
```

> **✅ Graceful Degradation**: System works with any combination of API keys. Missing providers are automatically disabled.

## 🏗️ Architecture

### Services
- **agno-app**: FastAPI application with AgentOS runtime (Port 80)
- **postgres**: PostgreSQL 16 with pgvector extension (Port 5432)

### Fixed Issues (v2.1)
- ✅ **Port Consistency**: Fixed Dockerfile/Compose port conflicts
- ✅ **Health Checks**: Optimized for Coolify v4 compatibility
- ✅ **Dependencies**: Added missing system packages and Python libraries
- ✅ **Error Handling**: Graceful handling of missing API keys
- ✅ **Startup Time**: Increased health check start period for complex initialization

### Features
- ✅ **Multi-Agent System**: Dynamic agents based on available LLM providers
- ✅ **Team Management**: Organized teams per model
- ✅ **Workflow Engine**: Automated multi-step processes
- ✅ **Knowledge Base**: Vector-powered RAG capabilities
- ✅ **Session Management**: Persistent conversations and memories
- ✅ **Control Plane**: Web interface for testing and monitoring
- ✅ **Health Monitoring**: Comprehensive health checks and metrics
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

| Provider | Model | Status | Capabilities |
|----------|-------|--------|-------------|
| **OpenAI** | GPT-4o | ✅ Tested | General purpose, coding, analysis |
| **Anthropic** | Claude 3.5 Sonnet | ✅ Tested | Reasoning, writing, research |
| **Google** | Gemini 1.5 Pro | ✅ Tested | Multimodal, long context |
| **Groq** | Llama 3.1 70B | ✅ Tested | Fast inference, open source |
| **Perplexity** | Sonar Huge | 🧪 Beta | Real-time web search |
| **XAI** | Grok Beta | 🧪 Beta | Conversational AI |
| **OpenRouter** | Multiple | 🧪 Beta | Access to various models |

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
├── compose.yml           # Docker Compose configuration (FIXED)
├── Dockerfile            # Application container (FIXED)
├── requirements.txt      # Python dependencies (UPDATED)
├── app/
│   └── main.py          # FastAPI application with AgentOS (FIXED)
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file (UPDATED)
```

## 🚨 Troubleshooting

### Common Issues

**❌ "No Available Server" (503 Error)**
- **Cause**: Health check failures or port conflicts
- **Solution**: Wait 2-3 minutes for full startup, check logs
- **Fixed in v2.1**: Optimized health check timing

**❌ API Key Errors**
- **Cause**: Missing or invalid API keys
- **Solution**: System gracefully handles missing keys now
- **Fixed in v2.1**: Optional API key configuration

**❌ Database Connection Failed**
- **Cause**: PostgreSQL not ready or password issues
- **Solution**: Verify `POSTGRES_PASSWORD` in environment variables
- **Fixed in v2.1**: Improved health check sequencing

**❌ Import Errors (ModuleNotFoundError)**
- **Cause**: Missing Python dependencies
- **Solution**: Rebuild container with updated requirements.txt
- **Fixed in v2.1**: Complete dependency specification

### Health Status Check

Monitor system status:

```bash
curl https://your-domain.com/health
```

Expected healthy response:
```json
{
  "status": "healthy",
  "agents": 1,
  "teams": 1, 
  "workflows": 1,
  "models": ["openai"],
  "database": "connected",
  "knowledge_base": true,
  "timestamp": "2025-10-27T20:57:49Z"
}
```

### Coolify v4 Specific Issues

**Problem**: Deploy hangs at "Building"
- **Solution**: Check build logs for dependency errors
- **Command**: `docker-compose build --no-cache`

**Problem**: Health check timeout
- **Solution**: Increase health check start period in Coolify settings
- **Recommendation**: Set to 120 seconds for complex initialization

## 🎯 Testing Scenarios

### Basic Functionality Tests
1. **Health Check**: `curl /health` should return 200
2. **API Documentation**: Visit `/docs` for interactive testing
3. **Agent Response**: Test basic chat functionality
4. **Database Persistence**: Create and retrieve conversations

### Advanced Testing
- **Multi-Agent Workflows**: Test team collaboration
- **Knowledge Base**: Upload and query documents
- **Memory Persistence**: Test conversation continuity
- **Model Switching**: Test different LLM providers

## 📈 Monitoring

### Built-in Metrics
- Agent response times
- Token usage per model
- Database query performance
- Memory and CPU utilization
- Error rates and health status

### Coolify Integration
- Real-time logs via Coolify dashboard
- Resource monitoring and alerts
- Automatic restarts on failure
- SSL certificate management
- Domain routing and load balancing

## 🔒 Security

- **Environment Isolation**: Docker containers with network isolation
- **API Key Management**: Secure environment variables
- **HTTPS**: Automatic SSL via Let's Encrypt (Coolify)
- **Database Security**: Isolated PostgreSQL instance
- **Access Control**: Configurable authentication (planned)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit Pull Request

## 📞 Support

For issues and questions:

- **GitHub Issues**: [Create Issue](https://github.com/lipeeh/agno-testing-environment/issues)
- **Agno Documentation**: [docs.agno.com](https://docs.agno.com)
- **Coolify Documentation**: [coolify.io/docs](https://coolify.io/docs)

## 🔄 Changelog

### v2.1 (2025-10-27) - MAJOR FIXES
- 🔧 **Fixed**: Port consistency between Dockerfile and Compose
- 🔧 **Fixed**: Health check timing for Coolify v4 compatibility
- 🔧 **Fixed**: Missing system dependencies (curl, build tools)
- 🔧 **Fixed**: Python import errors and model configuration
- 🔧 **Added**: Graceful handling of missing API keys
- 🔧 **Added**: Enhanced error handling and logging
- 🔧 **Added**: Coolify v4 specific labels and configuration

### v2.0 (2025-10-27) - Initial Release
- 🚀 **Added**: Complete Agno testing environment
- 🚀 **Added**: Multi-provider LLM support
- 🚀 **Added**: PostgreSQL with pgvector
- 🚀 **Added**: Docker Compose deployment

---

**Built with ❤️ for the Agno community**

*Ready to deploy your agentic AI system? All major issues are now fixed!* 🚀