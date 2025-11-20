"""
Script para crear las tablas de Supabase necesarias para el ARA Framework.
"""
import os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

def setup_database():
    """Crea las tablas necesarias en Supabase."""
    # Cargar .env desde la raíz del proyecto
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not service_role_key:
        print("❌ Error: SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar en .env")
        return
    
    client = create_client(supabase_url, service_role_key)
    
    # SQL para crear las 3 tablas
    sqls = [
        # 1. Tabla analysis_results
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
        
        # 2. Tabla papers_cache
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
        
        # 3. Tabla budget_tracking
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
    
    print("🔧 Creando tablas en Supabase...")
    
    for i, sql in enumerate(sqls, 1):
        try:
            # Ejecutar SQL usando la REST API de Supabase
            result = client.rpc('exec_sql', {'query': sql}).execute()
            print(f"✅ Tabla {i}/3 creada")
        except Exception as e:
            # Si la función exec_sql no existe, usar postgrest directamente
            print(f"⚠️  Tabla {i}/3: {str(e)[:100]}")
            print("💡 Consejo: Copia y pega el SQL en el SQL Editor de Supabase Dashboard")
    
    print("\n✅ Setup completado!")
    print(f"🔗 Dashboard: {supabase_url.replace('https://', 'https://supabase.com/dashboard/project/')}")
    print("\n📝 Si las tablas no se crearon automáticamente, ejecuta este SQL manualmente:")
    print("=" * 80)
    for sql in sqls:
        print(sql)
        print("-" * 80)

if __name__ == "__main__":
    setup_database()
