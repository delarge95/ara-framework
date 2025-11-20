"""
Test Perplexity para investigar modelos recientes y GitHub Copilot Pro
"""
import asyncio
from openai import AsyncOpenAI
from config.settings import settings

async def research_latest_models():
    """Investigar modelos más recientes usando Perplexity"""
    
    client = AsyncOpenAI(
        api_key=settings.PERPLEXITY_API_KEY,
        base_url="https://api.perplexity.ai",
    )
    
    queries = [
        {
            "title": "🔍 MODELOS MÁS RECIENTES (Nov 2025)",
            "query": """Latest AI language models November 2025:
            - Claude Sonnet 4.5 release date and availability
            - Claude Opus 4.1 release date and availability  
            - GPT-5 and GPT-5 mini public release
            - Llama 4 release
            - Gemini 2.5 Pro availability
            Provide release dates, pricing, API access details""",
            "recency": "day"
        },
        {
            "title": "🚀 GITHUB COPILOT PRO - ACCESO REAL",
            "query": """GitHub Copilot Pro November 2025:
            - What AI models does Copilot Pro actually use?
            - Is there a public API for GitHub Copilot Pro?
            - Can developers access Copilot Pro models via API?
            - What is the difference between Copilot Free, Pro, and Pro+?
            - GitHub Copilot Enterprise API access
            Provide official documentation and real capabilities""",
            "recency": "week"
        },
        {
            "title": "🎓 GITHUB STUDENTS - BENEFICIOS 2025",
            "query": """GitHub Student Developer Pack November 2025:
            - Does GitHub Students get free Copilot Pro or Pro+?
            - What AI models can students access?
            - GitHub Students API access benefits
            - GitHub Models beta access for students
            - Complete list of free tools and credits
            Provide official current benefits""",
            "recency": "week"
        },
        {
            "title": "🔑 ACCESO A MODELOS PREMIUM",
            "query": """Access to premium AI models November 2025:
            - GitHub Models beta: which models are free?
            - Azure AI Inference API with GitHub token
            - OpenAI compatible endpoints for Claude, GPT-4o
            - Free alternatives to OpenAI/Anthropic APIs
            - Academic/student API programs
            Provide working endpoints and authentication methods""",
            "recency": "week"
        }
    ]
    
    for i, query_info in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"{query_info['title']}")
        print(f"{'='*80}\n")
        
        try:
            response = await client.chat.completions.create(
                model="sonar",  # Modelo actual de Perplexity
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical researcher. Provide accurate, up-to-date information with sources. Include specific dates, pricing, and official documentation links."
                    },
                    {
                        "role": "user",
                        "content": query_info["query"]
                    }
                ],
                max_tokens=2000,
                temperature=0.2,
            )
            
            # Respuesta principal
            answer = response.choices[0].message.content
            print(answer)
            
            # Citaciones
            if hasattr(response, 'citations') and response.citations:
                print(f"\n📚 FUENTES ({len(response.citations)}):")
                for idx, citation in enumerate(response.citations[:5], 1):
                    print(f"  {idx}. {citation}")
            
            # Preguntas relacionadas
            if hasattr(response, 'related_questions') and response.related_questions:
                print(f"\n🔗 PREGUNTAS RELACIONADAS:")
                for question in response.related_questions[:3]:
                    print(f"  • {question}")
            
            print(f"\n{'─'*80}\n")
            
            # Pequeña pausa entre queries
            if i < len(queries):
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    print("\n" + "="*80)
    print("✅ INVESTIGACIÓN COMPLETADA")
    print("="*80)

if __name__ == "__main__":
    print("🔬 INVESTIGACIÓN: MODELOS RECIENTES Y GITHUB COPILOT PRO")
    print("="*80)
    asyncio.run(research_latest_models())
