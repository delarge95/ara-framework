"""
Script alternativo para crear tablas en Supabase usando HTTP directo.
Usa la API REST de PostgREST para ejecutar SQL.
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def setup_database():
    """Crea las tablas usando la API REST de Supabase."""
    # Cargar .env
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not service_role_key:
        print("❌ Error: SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar en .env")
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
    
    print("🔧 Creando tablas en Supabase via HTTP...")
    
    # Endpoint para ejecutar SQL (usando pg_meta o extensión personalizada)
    # Método 1: Intentar con el endpoint de management API
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json"
    }
    
    success_count = 0
    for i, sql in enumerate(sqls, 1):
        try:
            # Usar psycopg2 con supabase-py para ejecutar SQL raw
            from supabase import create_client
            client = create_client(supabase_url, service_role_key)
            
            # Intentar ejecutar SQL usando el cliente
            # PostgREST no soporta DDL directamente, necesitamos usar psycopg2
            print(f"⏳ Tabla {i}/3: Intentando crear via cliente Python...")
            
            # Como no podemos ejecutar DDL directamente con supabase-py,
            # usamos un enfoque diferente: crear una función temporal
            result = client.postgrest.rpc('exec_sql', {'query': sql}).execute()
            print(f"✅ Tabla {i}/3 creada")
            success_count += 1
            
        except Exception as e:
            error_msg = str(e)
            if "PGRST202" in error_msg or "Could not find" in error_msg:
                # Función exec_sql no existe, usar método alternativo
                print(f"⚠️  Tabla {i}/3: Función exec_sql no disponible")
                print(f"💡 Intentando método alternativo...")
                
                # Método 2: Usar psycopg2 directamente
                try:
                    import psycopg2
                    
                    # Construir connection string desde URL de Supabase
                    # URL format: https://xxx.supabase.co
                    project_id = supabase_url.replace("https://", "").replace(".supabase.co", "")
                    conn_string = f"postgresql://postgres.{project_id}:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
                    
                    print(f"❌ Necesitas psycopg2 y la password de Postgres")
                    print(f"💡 Ejecuta manualmente en SQL Editor de Supabase")
                    break
                    
                except ImportError:
                    print(f"❌ Tabla {i}/3: psycopg2 no instalado")
                    print(f"💡 Ejecuta: pip install psycopg2-binary")
                    break
            else:
                print(f"❌ Tabla {i}/3: Error inesperado: {error_msg[:100]}")
    
    if success_count == 3:
        print("\n✅ ¡Todas las tablas creadas exitosamente!")
        print(f"🔗 Dashboard: {supabase_url.replace('https://', 'https://supabase.com/dashboard/project/')}")
        return True
    else:
        print("\n⚠️  No se pudieron crear las tablas automáticamente")
        print("\n📝 SOLUCIÓN: Ejecuta este SQL manualmente en el SQL Editor:")
        print("=" * 80)
        print(f"🔗 {supabase_url.replace('https://', 'https://supabase.com/dashboard/project/')}")
        print("=" * 80)
        for i, sql in enumerate(sqls, 1):
            print(f"\n-- Tabla {i}/3:")
            print(sql)
            print("-" * 80)
        return False

if __name__ == "__main__":
    success = setup_database()
    exit(0 if success else 1)
