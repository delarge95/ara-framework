"""
Lista todos los modelos disponibles en GitHub Models Beta
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def list_available_models():
    """Lista todos los modelos disponibles en GitHub Models"""
    
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ ERROR: GITHUB_TOKEN no configurado en .env")
        return
    
    print("="*70)
    print("🔍 LISTANDO MODELOS DISPONIBLES EN GITHUB MODELS")
    print("="*70)
    print()
    
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=github_token,
    )
    
    try:
        # Intentar listar modelos
        models = client.models.list()
        
        print(f"✅ Total de modelos disponibles: {len(models.data)}\n")
        
        # Agrupar por familia
        familias = {}
        for model in models.data:
            # Extraer familia del nombre del modelo
            if "gpt" in model.id.lower():
                familia = "OpenAI GPT"
            elif "claude" in model.id.lower():
                familia = "Anthropic Claude"
            elif "llama" in model.id.lower():
                familia = "Meta Llama"
            elif "phi" in model.id.lower():
                familia = "Microsoft Phi"
            elif "mistral" in model.id.lower():
                familia = "Mistral AI"
            elif "command" in model.id.lower():
                familia = "Cohere Command"
            else:
                familia = "Otros"
            
            if familia not in familias:
                familias[familia] = []
            familias[familia].append(model.id)
        
        # Mostrar por familia
        for familia, modelos in sorted(familias.items()):
            print(f"📦 {familia}")
            print("-" * 70)
            for modelo in sorted(modelos):
                print(f"   • {modelo}")
            print()
        
    except Exception as e:
        print(f"❌ Error al listar modelos: {e}")
        print()
        print("🧪 Probando modelos conocidos manualmente...")
        print()
        
        # Lista de modelos conocidos para probar
        modelos_conocidos = [
            ("OpenAI GPT", [
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4",
                "gpt-4-turbo",
            ]),
            ("Anthropic Claude", [
                "claude-3-5-sonnet",
                "claude-3-sonnet",
                "claude-3-haiku",
            ]),
            ("Meta Llama", [
                "llama-3.1-70b",
                "llama-3.1-8b",
                "llama-3.2-11b",
                "llama-3.2-1b",
            ]),
            ("Microsoft Phi", [
                "phi-3-medium",
                "phi-3-small",
                "phi-3.5-mini",
            ]),
            ("Mistral AI", [
                "mistral-large",
                "mistral-nemo",
                "mistral-small",
            ]),
        ]
        
        for familia, modelos in modelos_conocidos:
            print(f"📦 {familia}")
            print("-" * 70)
            for modelo in modelos:
                try:
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": "test"}],
                        model=modelo,
                        max_tokens=5,
                    )
                    print(f"   ✅ {modelo}")
                except Exception as err:
                    if "unknown_model" in str(err).lower():
                        print(f"   ❌ {modelo} (no disponible)")
                    else:
                        print(f"   ⚠️  {modelo} (error: {str(err)[:50]})")
            print()
    
    print("="*70)
    print("💡 RECOMENDACIONES")
    print("="*70)
    print()
    print("Para tu proyecto ARA Framework, recomendamos:")
    print()
    print("🏆 MEJOR PARA ANÁLISIS DE LITERATURA:")
    print("   • gpt-4o (mejor balance calidad/velocidad)")
    print()
    print("🏆 MEJOR PARA ARQUITECTURA:")
    print("   • gpt-4o (mejor para diseño de sistemas)")
    print()
    print("🏆 MEJOR PARA CÓDIGO:")
    print("   • gpt-4o (mejor para implementación)")
    print()
    print("💰 MÁS ECONÓMICO (si hay rate limits):")
    print("   • gpt-4o-mini (más rápido y barato)")
    print()

if __name__ == "__main__":
    list_available_models()
