"""
Test rápido de Llama-3.1-405B con tool calling
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from config.settings import settings

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 25°C"

# Test Llama-405B
llm = ChatOpenAI(
    model="Meta-Llama-3.1-405B-Instruct",
    temperature=0.7,
    api_key=settings.GITHUB_TOKEN,
    base_url=settings.GITHUB_MODELS_BASE_URL,
)

tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

print("🧪 Testing Llama-3.1-405B with tool calling...")
print(f"Model: Meta-Llama-3.1-405B-Instruct")
print(f"Base URL: {settings.GITHUB_MODELS_BASE_URL}")

try:
    response = llm_with_tools.invoke("What's the weather in Paris?")
    print("\n✅ Response:")
    print(response)
    print(f"\n📊 Tool calls: {response.tool_calls if hasattr(response, 'tool_calls') else 'None'}")
except Exception as e:
    print(f"\n❌ Error: {e}")
