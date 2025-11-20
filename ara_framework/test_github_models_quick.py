"""
Test rápido para GitHub Models
"""
from openai import OpenAI

# Configuración
GITHUB_TOKEN = input("Ingresa tu GitHub Token (ghp_xxxxx): ").strip()

if not GITHUB_TOKEN or not GITHUB_TOKEN.startswith("ghp_"):
    print("❌ Token inválido. Debe empezar con 'ghp_'")
    exit(1)

print("\n🔬 PROBANDO GITHUB MODELS...")
print("="*80)

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
)

# Test 1: GPT-4o
print("\n📝 Test 1: GPT-4o")
print("-"*80)
try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Explain Rust WebAssembly in 50 words"}
        ],
        max_tokens=100,
    )
    print(f"✅ GPT-4o funciona!")
    print(f"Respuesta: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error con GPT-4o: {e}")

# Test 2: Claude 3.5 Sonnet
print("\n📝 Test 2: Claude 3.5 Sonnet")
print("-"*80)
try:
    response = client.chat.completions.create(
        model="claude-3-5-sonnet",
        messages=[
            {"role": "user", "content": "Analyze the importance of type safety in 30 words"}
        ],
        max_tokens=100,
    )
    print(f"✅ Claude 3.5 Sonnet funciona!")
    print(f"Respuesta: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error con Claude: {e}")

# Test 3: Llama 3.1
print("\n📝 Test 3: Llama 3.1 70B")
print("-"*80)
try:
    response = client.chat.completions.create(
        model="llama-3.1-70b",
        messages=[
            {"role": "user", "content": "What is functional programming in 25 words?"}
        ],
        max_tokens=100,
    )
    print(f"✅ Llama 3.1 funciona!")
    print(f"Respuesta: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error con Llama: {e}")

print("\n" + "="*80)
print("✅ PRUEBA COMPLETADA")
print("\nSi todos los modelos funcionan, puedes agregar el token a .env:")
print(f"GITHUB_TOKEN={GITHUB_TOKEN}")
