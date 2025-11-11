"""Test simple del pipeline - sin emojis para evitar problemas de encoding en PowerShell"""
import asyncio
import sys

# Add parent dir to path
sys.path.insert(0, r"d:\Downloads\TRABAJO_DE_GRADO\ara_framework")

from core.pipeline import AnalysisPipeline

async def main():
    print("\n" + "=" * 80)
    print("INICIANDO TEST SIMPLE DEL PIPELINE")
    print("=" * 80 + "\n")
    
    niche = "Rust WebAssembly for real-time audio processing"
    
    print(f"Niche: {niche}")
    print(f"Timeout: 10 minutos (para test rapido)")
    print("\n" + "-" * 80 + "\n")
    
    try:
        pipeline = AnalysisPipeline(
            timeout_minutes=10,
            enable_telemetry=False,
            enable_circuit_breaker=False,
        )
        
        print("[1/5] Creando pipeline...")
        result = await pipeline.run_analysis(niche)
        
        print("\n" + "-" * 80)
        print(f"STATUS: {result.status}")
        print(f"Errores: {len(result.errors)}")
        
        if result.errors:
            print("\nERRORES ENCONTRADOS:")
            for i, error in enumerate(result.errors, 1):
                print(f"  {i}. {error}")
        
        if result.warnings:
            print("\nADVERTENCIAS:")
            for i, warning in enumerate(result.warnings, 1):
                print(f"  {i}. {warning}")
        
        print("-" * 80)
        
        if result.status == "completed":
            print("\n SUCCESS - Pipeline completado")
            return 0
        else:
            print(f"\n FAILED - Pipeline termino con status: {result.status}")
            return 1
            
    except Exception as e:
        print(f"\nEXCEPCION: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
