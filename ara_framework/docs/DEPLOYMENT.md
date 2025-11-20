# 🚀 ARA Framework - Deployment Guide

Guía completa para deployment de ARA Framework en diferentes entornos: local, Docker, y cloud (AWS/GCP/Azure).

---

## 📋 Tabla de Contenidos

- [Prerequisitos Generales](#-prerequisitos-generales)
- [Deployment Local](#-deployment-local)
- [Deployment con Docker](#-deployment-con-docker)
- [Deployment Cloud (AWS)](#-deployment-cloud-aws)
- [Deployment Cloud (GCP)](#-deployment-cloud-gcp)
- [Deployment Cloud (Azure)](#-deployment-cloud-azure)
- [Configuración de Producción](#-configuración-de-producción)
- [Monitoring y Logs](#-monitoring-y-logs)
- [Troubleshooting](#-troubleshooting)

---

## 🔧 Prerequisitos Generales

### Requerimientos Mínimos

- **CPU**: 2 cores (4+ recomendado)
- **RAM**: 4GB (8GB+ recomendado)
- **Disco**: 10GB espacio libre
- **OS**: Windows 10+, Ubuntu 20.04+, macOS 12+

### Software Base

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Redis** (opcional, para cache) ([Download](https://redis.io/download))
- **Docker** (para deployment containerizado) ([Download](https://www.docker.com/get-started))

### API Keys Necesarias

Al menos **1 LLM API** (recomendado: Gemini, gratis):

| Servicio         | Requerido      | Costo    | Obtener                                                    |
| ---------------- | -------------- | -------- | ---------------------------------------------------------- |
| Gemini 2.5 Pro   | ⚠️ Recomendado | Gratis   | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| OpenAI GPT-4o    | Opcional       | Gratis\* | [OpenAI Platform](https://platform.openai.com/api-keys)    |
| Anthropic Claude | Opcional       | Pago     | [Anthropic Console](https://console.anthropic.com/)        |
| Supabase         | ⚠️ Recomendado | Gratis   | [Supabase Dashboard](https://supabase.com/)                |

\*GPT-4o gratis con Tier 1 (requiere primer pago de $5)

---

## 💻 Deployment Local

### 1. Setup Básico (Windows)

```powershell
# Clonar repositorio
git clone https://github.com/tu-usuario/ara_framework.git
cd ara_framework

# Crear entorno virtual
python -m venv .venv_py312
.\.venv_py312\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Copiar .env template
cp .env.example .env
```

### 2. Setup Básico (Linux/Mac)

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ara_framework.git
cd ara_framework

# Crear entorno virtual
python3.12 -m venv .venv_py312
source .venv_py312/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Copiar .env template
cp .env.example .env
```

### 3. Configurar .env

Editar `.env` con tus credenciales:

```bash
# REQUERIDO: Al menos 1 LLM
GEMINI_API_KEY=AIzaSy...  # Obtener en aistudio.google.com

# RECOMENDADO: Persistencia
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# OPCIONAL: Cache
REDIS_URL=redis://localhost:6379/0

# OPCIONAL: LLMs adicionales
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEEPSEEK_API_KEY=sk-...
```

### 4. Setup Supabase (2 minutos)

**Crear proyecto**:

1. Ve a [supabase.com](https://supabase.com)
2. Click "New Project"
3. Nombre: `ara-framework`
4. Region: `us-east-1` (o más cercana)
5. Copia URL + Keys al `.env`

**Crear tablas**:

Opción A - Automático:

```bash
python setup_supabase_postgres.py
# Agrega SUPABASE_DB_PASSWORD al .env si pide
```

Opción B - Manual:

1. Dashboard → SQL Editor
2. Ejecuta este SQL:

```sql
-- Tabla análisis
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    niche_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    report_markdown TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    duration_seconds FLOAT,
    credits_used FLOAT DEFAULT 0,
    errors TEXT[]
);

CREATE INDEX IF NOT EXISTS idx_analysis_niche ON analyses(niche_name);
CREATE INDEX IF NOT EXISTS idx_analysis_status ON analyses(status);
CREATE INDEX IF NOT EXISTS idx_analysis_created ON analyses(created_at DESC);

-- Tabla cache papers
CREATE TABLE IF NOT EXISTS papers_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paper_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT,
    authors JSONB DEFAULT '[]'::jsonb,
    year INTEGER,
    citation_count INTEGER DEFAULT 0,
    venue TEXT,
    url TEXT,
    pdf_url TEXT,
    fields_of_study TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb,
    cached_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_papers_paper_id ON papers_cache(paper_id);
CREATE INDEX IF NOT EXISTS idx_papers_year ON papers_cache(year DESC);

-- Tabla tracking budget
CREATE TABLE IF NOT EXISTS budget_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name TEXT NOT NULL,
    credits_used FLOAT NOT NULL,
    analysis_id UUID,
    agent_name TEXT,
    task_description TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_budget_timestamp ON budget_tracking(timestamp DESC);
```

### 5. Setup Redis (Opcional)

**Windows**:

```powershell
# Opción 1: WSL
wsl --install
wsl sudo apt install redis-server
wsl redis-server

# Opción 2: Memurai (puerto Redis para Windows)
# Descargar: https://www.memurai.com/get-memurai
```

**Linux**:

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**Mac**:

```bash
brew install redis
brew services start redis
```

**Verificar**:

```bash
redis-cli ping
# Debe responder: PONG
```

### 6. Validar Setup

```bash
# Test de conexiones
python test_api_connections.py

# Output esperado:
# ✅ Gemini API (Google)
# ✅ Supabase Database
# ✅ Semantic Scholar API
# Total: 3/6 servicios (FUNCIONAL)

# Test suite completo
pytest tests/
# Output esperado: 37/37 passing
```

### 7. Primer Análisis

```bash
python -m cli.main run "Rust WASM for audio processing"
```

**Tiempo**: 53-63 minutos  
**Costo**: 1-2.33 créditos (~$0.05-$0.12)  
**Output**: `outputs/rust_wasm_audio_YYYYMMDD/final_report.md`

---

## 🐳 Deployment con Docker

### 1. Dockerfile

Crear `Dockerfile` en la raíz:

```dockerfile
FROM python:3.12-slim

# Variables de build
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Variables de entorno por defecto
ENV ENV=production
ENV DEBUG=False
ENV LOG_LEVEL=INFO

# Exponer puerto (si se agrega API en futuro)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Comando por defecto
CMD ["python", "-m", "cli.main", "--help"]
```

### 2. Docker Compose

Crear `docker-compose.yml`:

```yaml
version: "3.8"

services:
  ara-framework:
    build: .
    container_name: ara-framework
    env_file:
      - .env
    volumes:
      - ./outputs:/app/outputs
      - ./logs:/app/logs
    depends_on:
      - redis
    networks:
      - ara-network
    command: tail -f /dev/null # Mantener contenedor vivo

  redis:
    image: redis:7-alpine
    container_name: ara-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - ara-network
    command: redis-server --appendonly yes

volumes:
  redis-data:

networks:
  ara-network:
    driver: bridge
```

### 3. Build y Run

```bash
# Build imagen
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f ara-framework

# Ejecutar análisis
docker-compose exec ara-framework python -m cli.main run "test niche"

# Detener servicios
docker-compose down

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v
```

### 4. Docker Hub (Opcional)

```bash
# Tag imagen
docker tag ara-framework:latest tu-usuario/ara-framework:1.0.0

# Push a Docker Hub
docker push tu-usuario/ara-framework:1.0.0

# Pull en otro servidor
docker pull tu-usuario/ara-framework:1.0.0
```

---

## ☁️ Deployment Cloud (AWS)

### Opción 1: EC2 (IaaS)

**1. Crear instancia EC2**:

- AMI: Ubuntu 22.04 LTS
- Tipo: t3.medium (2 vCPUs, 4GB RAM)
- Storage: 20GB gp3
- Security Group: SSH (22), HTTP (80), HTTPS (443)

**2. Conectar y setup**:

```bash
# SSH a la instancia
ssh -i tu-key.pem ubuntu@<ec2-public-ip>

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.12 python3.12-venv python3.12-dev -y

# Instalar Git
sudo apt install git -y

# Clonar repo
git clone https://github.com/tu-usuario/ara_framework.git
cd ara_framework

# Setup (ver sección Local)
python3.12 -m venv .venv_py312
source .venv_py312/bin/activate
pip install -r requirements.txt

# Configurar .env
nano .env
# (Pegar tus API keys)

# Validar
python test_api_connections.py
```

**3. Configurar como servicio (systemd)**:

```bash
# Crear archivo servicio
sudo nano /etc/systemd/system/ara-framework.service
```

Contenido:

```ini
[Unit]
Description=ARA Framework Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ara_framework
Environment="PATH=/home/ubuntu/ara_framework/.venv_py312/bin"
ExecStart=/home/ubuntu/ara_framework/.venv_py312/bin/python -m cli.main run "default niche"
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y arrancar
sudo systemctl daemon-reload
sudo systemctl enable ara-framework
sudo systemctl start ara-framework

# Ver status
sudo systemctl status ara-framework
```

### Opción 2: ECS (Container)

**1. Push imagen a ECR**:

```bash
# Autenticar Docker con ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag y push
docker tag ara-framework:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ara-framework:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ara-framework:latest
```

**2. Crear Task Definition**:

```json
{
  "family": "ara-framework",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "ara-framework",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/ara-framework:latest",
      "essential": true,
      "environment": [
        { "name": "ENV", "value": "production" },
        { "name": "GEMINI_API_KEY", "value": "tu-key" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ara-framework",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**3. Crear servicio ECS**:

```bash
aws ecs create-service \
  --cluster ara-cluster \
  --service-name ara-service \
  --task-definition ara-framework:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## ☁️ Deployment Cloud (GCP)

### Opción 1: Compute Engine

Similar a AWS EC2, usar Ubuntu 22.04 VM.

### Opción 2: Cloud Run

**1. Build con Cloud Build**:

```bash
# Submit build
gcloud builds submit --tag gcr.io/tu-proyecto/ara-framework

# Deploy a Cloud Run
gcloud run deploy ara-framework \
  --image gcr.io/tu-proyecto/ara-framework \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 1 \
  --set-env-vars GEMINI_API_KEY=tu-key,ENV=production
```

---

## ☁️ Deployment Cloud (Azure)

### Opción 1: Virtual Machine

Similar a AWS EC2, usar Ubuntu 22.04.

### Opción 2: Container Instances

```bash
# Deploy container
az container create \
  --resource-group ara-rg \
  --name ara-framework \
  --image tu-usuario/ara-framework:latest \
  --cpu 1 \
  --memory 2 \
  --environment-variables GEMINI_API_KEY=tu-key ENV=production
```

---

## 🔐 Configuración de Producción

### 1. .env para Producción

```bash
# ENVIRONMENT
ENV=production
DEBUG=False
LOG_LEVEL=WARNING
LOG_FORMAT=json

# SECURITY
MONTHLY_CREDIT_LIMIT=1000.0  # Aumentar para producción

# PERFORMANCE
REDIS_URL=redis://production-redis:6379/0  # Usar Redis para cache

# APIS
GEMINI_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...

# MONITORING (opcional)
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

### 2. Configuración de Redis

**redis.conf** optimizado:

```conf
# Persistencia
save 900 1
save 300 10
save 60 10000

# Memoria
maxmemory 256mb
maxmemory-policy allkeys-lru

# Performance
tcp-backlog 511
timeout 0
tcp-keepalive 300
```

### 3. Nginx Reverse Proxy (si se agrega API web)

```nginx
server {
    listen 80;
    server_name ara.tu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Monitoring y Logs

### 1. Logs Estructurados

ARA usa **structlog** para logs JSON:

```python
# Ver logs
tail -f logs/ara_framework.log | jq .

# Filtrar por level
tail -f logs/ara_framework.log | jq 'select(.level == "error")'

# Filtrar por componente
tail -f logs/ara_framework.log | jq 'select(.component == "budget_manager")'
```

### 2. Monitoring con Langfuse (Opcional)

```bash
# Agregar al .env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com

# Ver traces en: langfuse.com/dashboard
```

### 3. Health Checks

```bash
# Script de health check
cat > healthcheck.sh << 'EOF'
#!/bin/bash
python -c "
from config.settings import settings
from core.budget_manager import BudgetManager
print('OK')
"
EOF

chmod +x healthcheck.sh
./healthcheck.sh
```

---

## 🔧 Troubleshooting

### Problema: "Module not found"

```bash
# Verificar instalación
pip list | grep langgraph

# Reinstalar
pip install --force-reinstall langgraph
```

### Problema: "Supabase connection failed"

```bash
# Verificar credenciales
python -c "
from config.settings import settings
print(settings.SUPABASE_URL)
print(len(settings.SUPABASE_SERVICE_ROLE_KEY))
"

# Test manual
python test_api_connections.py
```

### Problema: "Redis connection refused"

```bash
# Verificar Redis corriendo
redis-cli ping

# Si no responde, iniciar
sudo systemctl start redis-server  # Linux
brew services start redis          # Mac
```

### Problema: "API rate limit exceeded"

```bash
# Ver uso actual
python -m cli.main budget

# Configurar límite menor
# En .env: MONTHLY_CREDIT_LIMIT=100.0
```

### Problema: "Out of memory"

```bash
# Aumentar swap (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# O usar máquina con más RAM (8GB+ recomendado)
```

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/ara_framework/issues)
- **Docs**: [Documentación completa](../README.md)
- **Email**: tu-email@example.com

---

_Última actualización: 2025-11-08_  
_Versión: 1.0.0_
