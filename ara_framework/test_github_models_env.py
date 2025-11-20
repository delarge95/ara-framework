"""
Test mejorado para GitHub Models - Con lectura desde .env
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()

def test_github_models():
    """Test de GitHub Models con diferentes modelos"""
    
    # Obtener token desde .env
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ ERROR: No se encontró GITHUB_TOKEN en .env")
        print("\n📝 Pasos para configurar:")
        print("1. Crea un token Classic en: https://github.com/settings/tokens")
        print("2. Marca el scope: read:packages")
        print("3. Agrega a .env: GITHUB_TOKEN=ghp_tu_token")
        print("\n⚠️  IMPORTANTE: Debe ser un token CLASSIC, no fine-grained")
        return
    
    # Verificar tipo de token
    if not github_token.startswith("ghp_"):
        print("⚠️  ADVERTENCIA: Tu token no parece ser un Classic token")
        print("   Los Classic tokens empiezan con 'ghp_'")
        print("   Fine-grained tokens empiezan con 'github_pat_'")
        print("\n❌ GitHub Models NO funciona con fine-grained tokens")
        print("   Necesitas crear un token Classic con read:packages")
        return
    
    print("✅ Token encontrado en .env")
    print(f"   Formato: {github_token[:8]}...{github_token[-4:]}")
    print("\n🔄 Probando acceso a GitHub Models...\n")
    
    # Configurar cliente
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=github_token,
    )
    
    # Modelos a probar
    modelos = [
        ("gpt-4o-mini", "GPT-4o Mini"),
        ("gpt-4o", "GPT-4o"),
        ("claude-3-5-sonnet", "Claude 3.5 Sonnet"),
    ]
    
    resultados = []
    
    for model_id, model_name in modelos:
        print(f"🧪 Probando {model_name}...")
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Di 'OK' si puedes leerme",
                    }
                ],
                temperature=0.1,
                max_tokens=10,
                model=model_id,
            )
            
            respuesta = response.choices[0].message.content
            print(f"   ✅ {model_name}: {respuesta}")
            resultados.append((model_name, True, respuesta))
            
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ {model_name}: {error_msg[:100]}")
            resultados.append((model_name, False, error_msg))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    exitosos = sum(1 for _, success, _ in resultados if success)
    total = len(resultados)
    
    print(f"\n✅ Exitosos: {exitosos}/{total}")
    
    if exitosos == 0:
        print("\n❌ NINGÚN MODELO FUNCIONÓ")
        print("\n🔍 Posibles causas:")
        print("1. Token fine-grained (por repositorio) - NO funciona con GitHub Models")
        print("2. Token sin scope 'read:packages'")
        print("3. Token expirado o inválido")
        print("\n✅ Solución:")
        print("1. Ir a: https://github.com/settings/tokens")
        print("2. Crear 'Generate new token (classic)' ← IMPORTANTE: CLASSIC")
        print("3. Marcar scope: read:packages")
        print("4. Copiar token y actualizar .env")
        print("\n⚠️  NO uses 'Fine-grained token' - solo funciona con repositorios")
    elif exitosos < total:
        print(f"\n⚠️  Algunos modelos fallaron ({total - exitosos}/{total})")
        print("   Esto puede ser normal durante la beta")
    else:
        print("\n🎉 TODOS LOS MODELOS FUNCIONAN CORRECTAMENTE")
        print("   Tu token está configurado correctamente")
        print("   Puedes integrar GitHub Models en tus agentes")
    
    # Detalles de errores
    errores = [r for r in resultados if not r[1]]
    if errores:
        print("\n" + "="*60)
        print("❌ DETALLES DE ERRORES")
        print("="*60)
        for model_name, _, error_msg in errores:
            print(f"\n{model_name}:")
            print(f"   {error_msg[:200]}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST DE GITHUB MODELS")
    print("="*60)
    print()
    
    test_github_models()
