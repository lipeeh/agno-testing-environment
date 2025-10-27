# 🚀 Deployment Guide - Coolify v4

**Step-by-step deployment guide for Agno Testing Environment**

## ⚙️ Prerequisites

- [x] **Hetzner VPS**: 8vCPU + 16GB RAM
- [x] **Coolify v4** installed and running
- [x] **Domain configured**: `agno.gohorse.srv.br`
- [x] **All LLM API Keys** available

## 📋 Step-by-Step Deployment

### **Step 1: Access Coolify Dashboard**

1. Open your Coolify v4 instance
2. Login with admin credentials
3. Navigate to main dashboard

### **Step 2: Create New Project**

1. Click **"Projects"** in sidebar
2. Click **"+ Add"** button
3. Configure project:
   - **Name**: `Agno Testing Environment`
   - **Description**: `Complete Agno agentic system for team testing`
4. Click **"Create"**

### **Step 3: Select Environment**

1. Select **"Production"** environment
2. Or choose your preferred environment

### **Step 4: Add Git Resource**

1. Click **"Add New Resource"**
2. Select **"Git Based"** (NOT Docker Based)
3. Configure Git settings:
   - **Source**: `Public Repository`
   - **Repository URL**: `https://github.com/lipeeh/agno-testing-environment`
   - **Branch**: `main`
4. Click **"Continue"**

### **Step 5: Configure Build**

1. **Build Pack**: Select `Docker Compose`
2. **Docker Compose Location**: `/compose.yml`
3. **Base Directory**: `/` (root)
4. Click **"Continue"**

### **Step 6: Configure Domain**

1. In **"Domains"** section:
   - **Add Domain**: `https://agno.gohorse.srv.br`
   - **Service**: `agno-app` (auto-detected)
2. **SSL**: Automatic via Let's Encrypt

### **Step 7: Environment Variables**

> ⚠️ **CRITICAL**: All variables with `:?` are REQUIRED

#### **Database Configuration**
```bash
POSTGRES_PASSWORD=SuaSenhaPostgresSuperSegura2024!
```

#### **LLM API Keys** (ALL REQUIRED)
```bash
OPENAI_API_KEY=sk-proj-sua_key_openai_aqui
ANTHROPIC_API_KEY=sk-ant-sua_key_anthropic_aqui  
GOOGLE_API_KEY=AIzaSua_key_google_aqui
GROQ_API_KEY=gsk_sua_key_groq_aqui
PERPLEXITY_API_KEY=pplx-sua_key_perplexity_aqui
XAI_API_KEY=xai-sua_key_grok_aqui
OPENROUTER_API_KEY=sk-or-sua_key_openrouter_aqui
```

1. Go to **"Environment Variables"** tab
2. Variables with red border are **REQUIRED**
3. Enter all values above
4. Click **"Save"**

### **Step 8: Deploy Application**

1. Click **"Deploy"** button (top right)
2. Monitor deployment in **"Deployments"** tab
3. Wait for both services to show **"Running"** status:
   - ✅ `postgres`: Running
   - ✅ `agno-app`: Running

**Expected deployment time**: 5-10 minutes

### **Step 9: Verify Deployment**

#### **Check Service Status**
In Coolify **"Services"** tab:
- `postgres`: ✅ Healthy
- `agno-app`: ✅ Healthy

#### **Test Endpoints**
1. **Main Interface**: https://agno.gohorse.srv.br/
2. **Health Check**: https://agno.gohorse.srv.br/health
3. **API Docs**: https://agno.gohorse.srv.br/docs
4. **Control Plane**: https://agno.gohorse.srv.br/playground

#### **Health Check Response**
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

## 🔍 Troubleshooting

### **Deployment Fails**

**Check Environment Variables**
- All required variables configured?
- API keys valid and active?
- No typos in variable names?

**View Logs**
1. Go to **"Deployments"** tab
2. Click on failed deployment
3. Check build and runtime logs

**Common Errors**
```bash
# Missing environment variable
ERROR: Missing required environment variable: OPENAI_API_KEY

# Invalid API key
ERROR: Authentication failed for provider: openai

# Database connection failed
ERROR: could not connect to server: Connection refused
```

### **Services Not Starting**

**PostgreSQL Issues**
- Wait for health check to pass (10-30 seconds)
- Check if `POSTGRES_PASSWORD` is set
- Verify sufficient disk space

**Application Issues**  
- Verify all API keys are valid
- Check if port 80 is available
- Monitor resource usage (CPU/RAM)

### **SSL/Domain Issues**

**DNS Propagation**
- Wait up to 24 hours for DNS propagation
- Use `dig agno.gohorse.srv.br` to verify

**Let's Encrypt**
- Coolify manages SSL automatically
- Check domain is publicly accessible
- Verify no conflicting SSL certificates

## 📏 Post-Deployment Configuration

### **Enable Auto-Deploy** (Optional)
1. Go to **"Settings"** tab
2. Enable **"Auto Deploy"**
3. Configure webhook in GitHub repository

### **Monitoring Setup**
1. **Real-time Logs**: Available in Coolify interface
2. **Resource Metrics**: CPU, RAM, Storage usage
3. **Health Checks**: Automatic every 30 seconds

### **Backup Configuration**
1. **Database Backups**: Configure in PostgreSQL service
2. **Volume Persistence**: Automatic via Docker volumes
3. **Configuration Backup**: Export environment variables

## ✅ Deployment Checklist

- [ ] Server meets minimum requirements (8vCPU, 16GB RAM)
- [ ] Coolify v4 is running and accessible
- [ ] Domain DNS is configured and propagated
- [ ] All 7 LLM API keys are valid and active
- [ ] Repository is public and accessible
- [ ] Environment variables are configured correctly
- [ ] Both services are running and healthy
- [ ] All endpoints are accessible via HTTPS
- [ ] Health check returns expected response
- [ ] Team can access and test the system

## 📞 Support

If you encounter issues:

1. **Check Logs**: Coolify deployment and runtime logs
2. **Verify Config**: Environment variables and API keys
3. **Resource Usage**: CPU, RAM, and disk space
4. **Network**: Domain resolution and SSL certificates

**Success Indicators**:
- ✅ All services running
- ✅ Health check passes
- ✅ All 7 models available
- ✅ Database connected
- ✅ HTTPS working

---

**Estimated Total Time**: 15-30 minutes

**Result**: Full Agno agentic system ready for team testing! 🎉