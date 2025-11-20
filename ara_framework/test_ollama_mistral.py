"""
Test Ollama Mistral - Verificación de tool calling con modelo local.

Este script prueba que Mistral 7B puede:
1. Conectarse correctamente via Ollama
2. Soportar tool calling (function calling)
3. Trabajar con las herramientas del sistema (search_recent_papers, scrape_website)

Prerequisitos:
- Ollama corriendo: ollama serve
- Mistral descargado: ollama pull mistral:7b (YA COMPLETADO según tus screenshots)
- langchain-ollama instalado: pip install langchain-ollama

Uso:
    python test_ollama_mistral.py
"""

import sys
import os
import structlog
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.model_factory import create_ollama_model, verify_model_availability
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# Setup logging
logger = structlog.get_logger(__name__)


# ============================================================================
# HERRAMIENTAS DE PRUEBA
# ============================================================================

@tool("search_papers_test")
def search_papers_test(query: str, max_results: int = 5) -> str:
    """
    Search for academic papers on a given topic.
    
    Args:
        query: The search query or topic
        max_results: Maximum number of papers to return
    
    Returns:
        String with mock paper results
    """
    return f"[MOCK] Found {max_results} papers about '{query}'"


@tool("calculate_test")
def calculate_test(operation: str, numbers: List[int]) -> int:
    """
    Perform mathematical calculations.
    
    Args:
        operation: The operation to perform (add, multiply, subtract)
        numbers: List of numbers to operate on
    
    Returns:
        Result of the calculation
    """
    if operation == "add":
        return sum(numbers)
    elif operation == "multiply":
        result = 1
        for n in numbers:
            result *= n
        return result
    elif operation == "subtract":
        result = numbers[0]
        for n in numbers[1:]:
            result -= n
        return result
    return 0


# ============================================================================
# TESTS
# ============================================================================

def test_0_connection():
    """Test 0: Verificar conexión básica con Ollama"""
    print("\n" + "="*70)
    print("TEST 0: Conexión Básica con Ollama")
    print("="*70)
    
    try:
        print("\nCreando instancia de ChatOllama...")
        llm = create_ollama_model(model="mistral:7b")
        
        print("Enviando mensaje de prueba...")
        response = llm.invoke("Say 'Hello, Ollama is working!' in one sentence.")
        
        print("\n--- Respuesta ---")
        print(f"Content: {response.content}")
        print(f"Tipo: {type(response)}")
        
        if len(response.content) > 0:
            print(f"\n✅ TEST 0 PASADO: Ollama responde correctamente")
            return True
        else:
            print(f"\n❌ TEST 0 FALLADO: Respuesta vacía")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 0: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        print("\nVerifica:")
        print("  1. Ollama está corriendo: ollama serve")
        print("  2. Mistral descargado: ollama list (debe mostrar mistral:7b)")
        print("  3. Puerto 11434 disponible")
        return False


def test_1_tool_recognition():
    """Test 1: Verificar que reconoce y llama una herramienta simple"""
    print("\n" + "="*70)
    print("TEST 1: Reconocimiento Básico de Herramientas")
    print("="*70)
    
    try:
        llm = create_ollama_model(model="mistral:7b")
        llm_with_tools = llm.bind_tools([search_papers_test])
        
        prompt = "Search for papers about deep learning, get 10 results"
        print(f"\nPrompt: {prompt}")
        print("\nInvocando modelo con tool binding...")
        
        result = llm_with_tools.invoke(prompt)
        
        # Verificaciones
        print("\n--- Resultados ---")
        print(f"Tipo de resultado: {type(result)}")
        print(f"¿Tiene tool_calls?: {hasattr(result, 'tool_calls')}")
        
        if hasattr(result, 'tool_calls') and result.tool_calls:
            print(f"✅ Tool calls detectados: {len(result.tool_calls)}")
            for i, call in enumerate(result.tool_calls):
                print(f"\nTool Call #{i+1}:")
                print(f"  - Nombre: {call.get('name', 'N/A')}")
                print(f"  - Argumentos: {call.get('args', 'N/A')}")
                print(f"  - ID: {call.get('id', 'N/A')}")
            
            # Validación específica
            expected_tool = "search_papers_test"
            actual_tool = result.tool_calls[0].get('name', '')
            if actual_tool == expected_tool:
                print(f"\n✅ TEST 1 PASADO: Herramienta correcta llamada ({expected_tool})")
                return True
            else:
                print(f"\n⚠️ TEST 1 PARCIAL: Esperaba '{expected_tool}', obtuvo '{actual_tool}'")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print(f"Content (primeros 200 chars): {result.content[:200] if hasattr(result, 'content') else 'N/A'}")
            print("\n⚠️ POSIBLE CAUSA: Mistral puede responder en texto sin usar tool")
            print("   Esto es común en modelos locales sin fine-tuning específico para tools")
            print("\n❌ TEST 1 FALLADO: No hay tool calling")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 1: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


def test_2_multiple_tools():
    """Test 2: Verificar que puede elegir entre múltiples herramientas"""
    print("\n" + "="*70)
    print("TEST 2: Selección Entre Múltiples Herramientas")
    print("="*70)
    
    try:
        llm = create_ollama_model(model="mistral:7b")
        llm_with_tools = llm.bind_tools([search_papers_test, calculate_test])
        
        # Prompt que claramente requiere la herramienta de cálculo
        prompt = "Calculate the sum of 10, 20, and 30"
        print(f"\nPrompt: {prompt}")
        print("\nInvocando modelo...")
        
        result = llm_with_tools.invoke(prompt)
        
        print("\n--- Resultados ---")
        if hasattr(result, 'tool_calls') and result.tool_calls:
            print(f"✅ Tool calls detectados: {len(result.tool_calls)}")
            tool_name = result.tool_calls[0].get('name', '')
            print(f"Herramienta seleccionada: {tool_name}")
            print(f"Argumentos: {result.tool_calls[0].get('args', {})}")
            
            if tool_name == "calculate_test":
                print(f"\n✅ TEST 2 PASADO: Seleccionó herramienta correcta (calculate_test)")
                return True
            else:
                print(f"\n⚠️ TEST 2 PARCIAL: Llamó '{tool_name}' en vez de 'calculate_test'")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print(f"Content: {result.content if hasattr(result, 'content') else 'N/A'}")
            print("\n❌ TEST 2 FALLADO")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 2: {str(e)}")
        return False


def test_3_realistic_scenario():
    """Test 3: Escenario realista similar al uso en research_graph"""
    print("\n" + "="*70)
    print("TEST 3: Escenario Realista (Similar a Agent 1)")
    print("="*70)
    
    try:
        # Simular herramienta real del sistema
        @tool("search_recent_papers")
        def search_recent_papers(query: str, max_results: int = 15) -> str:
            """
            Search Semantic Scholar for recent papers on a given topic.
            
            Args:
                query: Search query or topic
                max_results: Maximum number of papers to return (default: 15)
            
            Returns:
                JSON string with paper information
            """
            return f"[MOCK] Searching Semantic Scholar for '{query}' (max: {max_results})"
        
        llm = create_ollama_model(model="mistral:7b", num_ctx=32768)
        llm_with_tools = llm.bind_tools([search_recent_papers])
        
        # Prompt similar al que usa Agent 1
        prompt = """You are a niche identification specialist. 
Your task is to find recent research papers about 'deep learning for drug discovery'.
Search for at most 10 recent papers on this topic."""
        
        print(f"\nPrompt: {prompt[:100]}...")
        print("\nInvocando modelo...")
        
        result = llm_with_tools.invoke(prompt)
        
        print("\n--- Resultados ---")
        if hasattr(result, 'tool_calls') and result.tool_calls:
            print(f"✅ Tool calls: {len(result.tool_calls)}")
            
            for call in result.tool_calls:
                print(f"\nTool: {call.get('name')}")
                print(f"Args: {call.get('args')}")
            
            # Verificar que llamó la herramienta correcta
            tool_name = result.tool_calls[0].get('name')
            args = result.tool_calls[0].get('args', {})
            
            if tool_name == "search_recent_papers":
                if 'query' in args:
                    print(f"\n✅ TEST 3 PASADO: Comportamiento realista correcto")
                    return True
                else:
                    print(f"\n⚠️ TEST 3 PARCIAL: Herramienta correcta pero query incorrecto")
                    return False
            else:
                print(f"\n❌ TEST 3 FALLADO: Herramienta incorrecta")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print(f"Content (primeros 300 chars): {result.content[:300] if hasattr(result, 'content') else 'N/A'}")
            print("\n❌ TEST 3 FALLADO")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 3: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# RUNNER
# ============================================================================

def run_all_tests():
    """Ejecutar todos los tests y mostrar resumen"""
    print("\n")
    print("="*70)
    print(" SUITE DE PRUEBAS: OLLAMA MISTRAL 7B")
    print(" Objetivo: Verificar tool calling para desarrollo local")
    print("="*70)
    
    # Pre-check: Verificar disponibilidad
    print("\n[Pre-check] Verificando disponibilidad de Ollama Mistral...")
    if verify_model_availability("ollama", "mistral:7b"):
        print("✅ Ollama Mistral está disponible")
    else:
        print("❌ No se puede conectar con Ollama Mistral")
        print("\nAsegúrate de:")
        print("  1. Ejecutar: ollama serve")
        print("  2. Verificar: ollama list (debe mostrar mistral:7b)")
        print("  3. Directorio configurado: E:\\modelos_ollama")
        sys.exit(1)
    
    # Ejecutar tests
    results = []
    results.append(("Test 0: Conexión básica", test_0_connection()))
    results.append(("Test 1: Reconocimiento de herramientas", test_1_tool_recognition()))
    results.append(("Test 2: Múltiples herramientas", test_2_multiple_tools()))
    results.append(("Test 3: Escenario realista", test_3_realistic_scenario()))
    
    # Resumen
    print("\n")
    print("="*70)
    print(" RESUMEN DE RESULTADOS")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASADO" if result else "❌ FALLADO"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} tests pasados ({(passed/total)*100:.1f}%)")
    print("-"*70)
    
    # Conclusión
    print("\n" + "="*70)
    print(" CONCLUSIÓN Y PRÓXIMOS PASOS")
    print("="*70)
    
    if passed == total:
        print("\n✅✅✅ EXCELENTE: Mistral 7B soporta tool calling completamente")
        print("\n📋 Próximos pasos:")
        print("  1. [RECOMENDADO] Usar Mistral para desarrollo intensivo")
        print("  2. Modificar test_single_agent.py para usar Ollama")
        print("  3. Comparar calidad: GitHub Models vs Mistral")
        print("  4. Documentar configuración en OPTIMIZACIONES_MODELOS.md")
    elif passed >= 2:
        print("\n⚠️ PARCIAL: Tool calling funciona con limitaciones")
        print(f"\nTests pasados: {passed}/{total}")
        print("\n📋 Recomendación:")
        print("  - Mistral puede usar tool calling pero con menor precisión")
        print("  - Usar para desarrollo, GitHub Models para producción")
        print("  - Considerar Qwen2.5:8b como alternativa")
    else:
        print("\n❌ CRÍTICO: Mistral 7B NO soporta tool calling adecuadamente")
        print("\n📋 Alternativas:")
        print("  1. Probar Qwen2.5:8b (ollama pull qwen2.5:8b)")
        print("  2. Investigar otros modelos con tag 'tools'")
        print("  3. Mantener GitHub Models como única opción")
        print("  4. Esperar reset de rate limit (50 req/día)")
    
    print("\n" + "="*70 + "\n")
    
    return passed, total


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        passed, total = run_all_tests()
        
        # Exit code para CI/CD
        if passed == total:
            sys.exit(0)  # Success
        elif passed >= 2:
            sys.exit(1)  # Partial
        else:
            sys.exit(2)  # Failed
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrumpidos por usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(3)
