"""
Script para ver el reporte generado desde Supabase
"""
import os
from supabase import create_client

# Configuración
SUPABASE_URL = "https://dixawjrgwttdbdvtbmqb.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpeGF3anJnd3R0ZGJkdnRibXFiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjM5MTczMywiZXhwIjoyMDc3OTY3NzMzfQ.DMe2Mw2rm6dZx87fAOBwIt5Uc37OCmyPxBThaLNZAe4")

# ID del último reporte
REPORT_ID = "e3bbf88b-8c99-40d8-8251-d6903901b2cd"

def view_report(report_id: str = REPORT_ID):
    """Ver reporte desde Supabase"""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Obtener reporte
    response = client.table("analyses").select("*").eq("id", report_id).execute()
    
    if response.data:
        report = response.data[0]
        
        print("╭" + "─" * 70 + "╮")
        print(f"│ 📊 REPORTE DE INVESTIGACIÓN")
        print("├" + "─" * 70 + "┤")
        print(f"│ ID: {report['id']}")
        print(f"│ Nicho: {report['niche_name']}")
        print(f"│ Status: {report['status']}")
        print(f"│ Creado: {report['created_at']}")
        print("╰" + "─" * 70 + "╯\n")
        
        # Mostrar secciones
        sections = [
            ("niche_analysis", "1. ANÁLISIS DE NICHO"),
            ("literature_review", "2. REVISIÓN DE LITERATURA"),
            ("technical_architecture", "3. ARQUITECTURA TÉCNICA"),
            ("implementation_roadmap", "4. ROADMAP DE IMPLEMENTACIÓN"),
            ("final_report", "5. REPORTE FINAL")
        ]
        
        for field, title in sections:
            if report.get(field):
                content = report[field]
                print(f"\n{'='*80}")
                print(f" {title}")
                print(f"{'='*80}\n")
                print(content[:1000])  # Primeros 1000 chars
                print(f"\n... (Total: {len(content)} caracteres)")
        
        # Estadísticas
        print(f"\n{'='*80}")
        print(" 📊 ESTADÍSTICAS")
        print(f"{'='*80}")
        total_chars = sum(len(str(report.get(field, ""))) for field, _ in sections)
        print(f"Total caracteres: {total_chars:,}")
        print(f"Total palabras: ~{total_chars // 5:,}")
        
    else:
        print(f"❌ No se encontró reporte con ID: {report_id}")

if __name__ == "__main__":
    view_report()
