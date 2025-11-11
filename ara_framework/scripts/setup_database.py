"""
Script para crear tablas en Supabase usando conexión directa a PostgreSQL.
Requiere: pip install psycopg2-binary
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

def get_postgres_connection_string():
    """Construye la cadena de conexión PostgreSQL desde las variables de entorno."""
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    supabase_url = os.getenv("SUPABASE_URL")
    
    if not supabase_url:
        print("❌ Error: SUPABASE_URL debe estar en .env")
        return None
    
    # Extraer project_id de la URL (formato: https://xxx.supabase.co)
    parsed = urlparse(supabase_url)
    project_id = parsed.hostname.replace(".supabase.co", "")
    
    # Intentar obtener SUPABASE_DB_PASSWORD del .env
    db_password = os.getenv("SUPABASE_DB_PASSWORD")
    
    if not db_password:
        print("\n⚠️  SUPABASE_DB_PASSWORD no encontrado en .env")
        print("📝 Para obtener tu password de PostgreSQL:")
        print(f"   1. Ve a: https://supabase.com/dashboard/project/{project_id}/settings/database")
        print("   2. En la sección 'Connection String', copia el password")
        print("   3. Agrégalo a .env como: SUPABASE_DB_PASSWORD=tu_password")
        print("\n💡 O ejecuta el SQL manualmente en el SQL Editor del Dashboard\n")
        return None
    
    # Construir connection string
    # Formato Supabase: postgresql://postgres.[PROJECT-ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
    conn_string = f"postgresql://postgres.{project_id}:{db_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
    
    return conn_string

def setup_database():
    """Crea las tablas usando conexión directa a PostgreSQL."""
    
    conn_string = get_postgres_connection_string()
    if not conn_string:
        return False
    
    # SQLs para crear las tablas
    sqls = [
        # Tabla 1: analysis_results
        """
        CREATE TABLE IF NOT EXISTS analysis_results (
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
        
        CREATE INDEX IF NOT EXISTS idx_analysis_niche ON analysis_results(niche_name);
        CREATE INDEX IF NOT EXISTS idx_analysis_status ON analysis_results(status);
        CREATE INDEX IF NOT EXISTS idx_analysis_created ON analysis_results(created_at DESC);
        """,
        
        # Tabla 2: papers_cache
        """
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
        CREATE INDEX IF NOT EXISTS idx_papers_citations ON papers_cache(citation_count DESC);
        """,
        
        # Tabla 3: budget_tracking
        """
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
        CREATE INDEX IF NOT EXISTS idx_budget_model ON budget_tracking(model_name);
        """
    ]
    
    print("🔧 Conectando a PostgreSQL de Supabase...")
    
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión establecida")
        print("\n🔧 Creando tablas...")
        
        for i, sql in enumerate(sqls, 1):
            try:
                cursor.execute(sql)
                print(f"✅ Tabla {i}/3 creada")
            except Exception as e:
                print(f"⚠️  Tabla {i}/3: {str(e)[:100]}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ ¡Setup completado!")
        print(f"🔗 Verifica en: https://supabase.com/dashboard/project/{get_project_id()}/editor")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Error de conexión: {str(e)[:200]}")
        print("\n💡 Verifica:")
        print("   1. SUPABASE_DB_PASSWORD correcto en .env")
        print("   2. Conexión pooler habilitada en Supabase")
        print("\n📝 Alternativa: Ejecuta el SQL manualmente en SQL Editor")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)[:200]}")
        return False

def get_project_id():
    """Obtiene el project ID de Supabase."""
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    supabase_url = os.getenv("SUPABASE_URL", "")
    return supabase_url.replace("https://", "").replace(".supabase.co", "")

if __name__ == "__main__":
    success = setup_database()
    
    if not success:
        print("\n" + "=" * 80)
        print("📝 SQL para ejecutar manualmente:")
        print("=" * 80)
        print("""
-- Tabla 1: analysis_results
CREATE TABLE IF NOT EXISTS analysis_results (
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

CREATE INDEX IF NOT EXISTS idx_analysis_niche ON analysis_results(niche_name);
CREATE INDEX IF NOT EXISTS idx_analysis_status ON analysis_results(status);
CREATE INDEX IF NOT EXISTS idx_analysis_created ON analysis_results(created_at DESC);

-- Tabla 2: papers_cache
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
CREATE INDEX IF NOT EXISTS idx_papers_citations ON papers_cache(citation_count DESC);

-- Tabla 3: budget_tracking
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
CREATE INDEX IF NOT EXISTS idx_budget_model ON budget_tracking(model_name);
        """)
    
    exit(0 if success else 1)
