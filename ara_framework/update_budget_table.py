"""
Script para actualizar la tabla budget_tracking con las columnas faltantes.
"""
from supabase import create_client
from config.settings import settings

def update_budget_table():
    """Agrega columnas faltantes a budget_tracking."""
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    
    sql = """
    -- Agregar columnas faltantes a budget_tracking
    ALTER TABLE budget_tracking 
    ADD COLUMN IF NOT EXISTS period_start TIMESTAMPTZ DEFAULT DATE_TRUNC('month', NOW()),
    ADD COLUMN IF NOT EXISTS period_end TIMESTAMPTZ DEFAULT DATE_TRUNC('month', NOW()) + INTERVAL '30 days',
    ADD COLUMN IF NOT EXISTS credits_remaining FLOAT,
    ADD COLUMN IF NOT EXISTS usage_percentage FLOAT,
    ADD COLUMN IF NOT EXISTS requests_by_model JSONB DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS alert_triggered BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS alert_threshold FLOAT DEFAULT 0.80,
    ADD COLUMN IF NOT EXISTS credits_limit INTEGER DEFAULT 300,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();
    """
    
    print("🔧 Actualizando tabla budget_tracking...")
    
    try:
        # Intentar con PostgREST
        result = client.rpc('exec_sql', {'query': sql}).execute()
        print("✅ Tabla actualizada exitosamente")
    except Exception as e:
        error_msg = str(e)
        if 'exec_sql' in error_msg:
            print("⚠️  No se pudo ejecutar automáticamente")
            print("\n📝 Copia y pega este SQL en el SQL Editor de Supabase:")
            print("=" * 80)
            print(sql)
            print("=" * 80)
            print(f"\n🔗 Dashboard: https://supabase.com/dashboard/project/dixawjrgwttdbdvtbmqb/sql")
        else:
            print(f"❌ Error: {error_msg}")
            print("\n📝 Copia y pega este SQL en el SQL Editor de Supabase:")
            print("=" * 80)
            print(sql)
            print("=" * 80)

if __name__ == "__main__":
    update_budget_table()
