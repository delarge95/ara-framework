"""
Script para descubrir TODOS los modelos disponibles en GitHub Models
probando directamente con la API
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

def test_model(client, model_id, familia):
    """Prueba si un modelo está disponible"""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "test"}],
            model=model_id,
            max_tokens=5,
            timeout=10,
        )
        return True, "✅"
    except Exception as e:
        error_str = str(e).lower()
        if "unknown_model" in error_str or "model_not_found" in error_str:
            return False, "❌ No disponible"
        elif "rate_limit" in error_str:
            return None, "⏱️ Rate limit"
        else:
            return None, f"⚠️ {str(e)[:50]}"

def discover_all_models():
    """Descubre todos los modelos disponibles"""
    
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ ERROR: GITHUB_TOKEN no configurado")
        return
    
    print("="*80)
    print("🔍 DESCUBRIENDO TODOS LOS MODELOS EN GITHUB MODELS (NOV 2025)")
    print("="*80)
    print()
    
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=github_token,
    )
    
    # Lista completa de modelos para probar basada en docs de Nov 2025
    modelos_a_probar = {
        "🤖 OpenAI": [
            "gpt-4o",
            "gpt-4o-mini",
            "o1-preview",
            "o1-mini",
        ],
        "🧠 Anthropic Claude": [
            "claude-3-5-sonnet",
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku",
        ],
        "🦙 Meta Llama": [
            "Llama-3.3-70B-Instruct",
            "Meta-Llama-3.1-405B-Instruct",
            "Meta-Llama-3.1-70B-Instruct",
            "Meta-Llama-3.1-8B-Instruct",
            "Meta-Llama-3-70B-Instruct",
            "Meta-Llama-3-8B-Instruct",
        ],
        "🔬 Microsoft Phi": [
            "Phi-4",
            "Phi-3.5-MoE-instruct",
            "Phi-3.5-mini-instruct",
            "Phi-3.5-vision-instruct",
            "Phi-3-medium-128k-instruct",
            "Phi-3-medium-4k-instruct",
            "Phi-3-mini-128k-instruct",
            "Phi-3-mini-4k-instruct",
            "Phi-3-small-128k-instruct",
            "Phi-3-small-8k-instruct",
        ],
        "🌟 Mistral AI": [
            "Mistral-large",
            "Mistral-large-2407",
            "Mistral-Nemo",
            "Mistral-small",
        ],
        "🔷 Cohere": [
            "cohere-command-r",
            "cohere-command-r-08-2024",
            "cohere-command-r-plus",
            "cohere-command-r-plus-08-2024",
        ],
        "🎯 AI21 Labs": [
            "jamba-1.5-large",
            "jamba-1.5-mini",
        ],
        "🚀 Otras Opciones": [
            "ministral-3b",
            "Ministral-3B-2410",
        ],
    }
    
    disponibles = {}
    no_disponibles = {}
    errores = {}
    
    total = sum(len(modelos) for modelos in modelos_a_probar.values())
    actual = 0
    
    for familia, modelos in modelos_a_probar.items():
        print(f"\n{familia}")
        print("-" * 80)
        
        for modelo in modelos:
            actual += 1
            print(f"[{actual}/{total}] Probando {modelo}... ", end="", flush=True)
            
            disponible, estado = test_model(client, modelo, familia)
            print(estado)
            
            if disponible == True:
                if familia not in disponibles:
                    disponibles[familia] = []
                disponibles[familia].append(modelo)
            elif disponible == False:
                if familia not in no_disponibles:
                    no_disponibles[familia] = []
                no_disponibles[familia].append(modelo)
            else:
                if familia not in errores:
                    errores[familia] = []
                errores[familia].append((modelo, estado))
            
            time.sleep(0.5)  # Rate limiting
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN DE MODELOS DISPONIBLES")
    print("="*80)
    
    total_disponibles = sum(len(m) for m in disponibles.values())
    print(f"\n✅ Total de modelos disponibles: {total_disponibles}\n")
    
    if disponibles:
        for familia, modelos in disponibles.items():
            print(f"{familia}")
            print("-" * 80)
            for modelo in modelos:
                print(f"   ✅ {modelo}")
            print()
    
    if errores:
        print("\n" + "="*80)
        print("⚠️ MODELOS CON ERRORES (pueden estar disponibles)")
        print("="*80)
        for familia, items in errores.items():
            print(f"\n{familia}")
            print("-" * 80)
            for modelo, error in items:
                print(f"   {error} {modelo}")
    
    # Guardar resultados
    with open("GITHUB_MODELS_DISPONIBLES.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("MODELOS DISPONIBLES EN GITHUB MODELS (Nov 2025)\n")
        f.write("="*80 + "\n\n")
        
        for familia, modelos in disponibles.items():
            f.write(f"{familia}\n")
            f.write("-" * 80 + "\n")
            for modelo in modelos:
                f.write(f"   ✅ {modelo}\n")
            f.write("\n")
    
    print("\n✅ Resultados guardados en: GITHUB_MODELS_DISPONIBLES.txt")
    print("="*80)

if __name__ == "__main__":
    discover_all_models()
