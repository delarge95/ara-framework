"""
Test de tool calling support en GitHub Models
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from config.settings import settings

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 25°C"

# Modelos a probar
models_to_test = [
    "gpt-4o",
    "gpt-4o-mini",
    "Meta-Llama-3.1-405B-Instruct",
    "cohere-command-r-plus-08-2024",
    "Phi-4",
    "Mistral-small",
]

print("🧪 Testing tool calling support across GitHub Models\n")
print("=" * 70)

for model_name in models_to_test:
    print(f"\n🔍 Testing: {model_name}")
    print("-" * 70)
    
    try:
        llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=settings.GITHUB_TOKEN,
            base_url=settings.GITHUB_MODELS_BASE_URL,
            max_tokens=50,
        )
        
        llm_with_tools = llm.bind_tools([get_weather])
        response = llm_with_tools.invoke("What's the weather in Paris?")
        
        has_tool_calls = hasattr(response, 'tool_calls') and len(response.tool_calls) > 0
        
        if has_tool_calls:
            print(f"✅ SUPPORTS TOOL CALLING")
            print(f"   Tool called: {response.tool_calls[0]['name']}")
        else:
            print(f"❌ NO TOOL CALLING SUPPORT")
            print(f"   Response: {response.content[:100]}...")
            
    except Exception as e:
        print(f"⚠️  ERROR: {str(e)[:100]}")

print("\n" + "=" * 70)
print("\n📊 RECOMMENDATION: Use models with ✅ for agents that need tools")
