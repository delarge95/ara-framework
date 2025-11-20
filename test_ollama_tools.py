"""
Script de Prueba: Tool Calling con Ollama
Objetivo: Verificar que Mistral 7B soporta tool calling con LangChain

Prerequisitos:
1. Ollama instalado y corriendo: ollama serve
2. Modelo descargado: ollama pull mistral:7b
3. Paquetes: pip install langchain-ollama langchain-core
"""

import sys
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import AIMessage


# ============================================================================
# DEFINICIÓN DE HERRAMIENTAS DE PRUEBA
# ============================================================================

@tool("search_papers")
def search_papers(query: str, max_results: int = 5) -> str:
    """
    Search for academic papers on a given topic.
    
    Args:
        query: The search query or topic
        max_results: Maximum number of papers to return
    
    Returns:
        String with mock paper results
    """
    return f"Found {max_results} papers about '{query}'"


@tool("calculate")
def calculate(operation: str, numbers: List[int]) -> int:
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

def test_1_basic_tool_recognition():
    """Test 1: Verificar que el modelo reconoce y llama una herramienta simple"""
    print("\n" + "="*70)
    print("TEST 1: Reconocimiento Básico de Herramientas")
    print("="*70)
    
    try:
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0
        ).bind_tools([search_papers])
        
        prompt = "Search for papers about deep learning, get 10 results"
        print(f"\nPrompt: {prompt}")
        print("\nInvocando modelo...")
        
        result = llm.invoke(prompt)
        
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
            expected_tool = "search_papers"
            actual_tool = result.tool_calls[0].get('name', '')
            if actual_tool == expected_tool:
                print(f"\n✅ TEST 1 PASADO: Herramienta correcta llamada ({expected_tool})")
                return True
            else:
                print(f"\n❌ TEST 1 FALLADO: Esperaba '{expected_tool}', obtuvo '{actual_tool}'")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print(f"Content: {result.content if hasattr(result, 'content') else 'N/A'}")
            print("\n❌ TEST 1 FALLADO: No hay tool calling")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 1: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        return False


def test_2_multiple_tools():
    """Test 2: Verificar que puede elegir entre múltiples herramientas"""
    print("\n" + "="*70)
    print("TEST 2: Selección Entre Múltiples Herramientas")
    print("="*70)
    
    try:
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0
        ).bind_tools([search_papers, calculate])
        
        # Prompt que claramente requiere la herramienta de cálculo
        prompt = "Calculate the sum of 10, 20, and 30"
        print(f"\nPrompt: {prompt}")
        print("\nInvocando modelo...")
        
        result = llm.invoke(prompt)
        
        print("\n--- Resultados ---")
        if hasattr(result, 'tool_calls') and result.tool_calls:
            print(f"✅ Tool calls detectados: {len(result.tool_calls)}")
            tool_name = result.tool_calls[0].get('name', '')
            print(f"Herramienta seleccionada: {tool_name}")
            print(f"Argumentos: {result.tool_calls[0].get('args', {})}")
            
            if tool_name == "calculate":
                print(f"\n✅ TEST 2 PASADO: Seleccionó herramienta correcta (calculate)")
                return True
            else:
                print(f"\n⚠️ TEST 2 PARCIAL: Llamó '{tool_name}' en vez de 'calculate'")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print(f"Content: {result.content if hasattr(result, 'content') else 'N/A'}")
            print("\n❌ TEST 2 FALLADO")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 2: {str(e)}")
        return False


def test_3_complex_arguments():
    """Test 3: Verificar que puede extraer argumentos complejos"""
    print("\n" + "="*70)
    print("TEST 3: Extracción de Argumentos Complejos")
    print("="*70)
    
    try:
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0
        ).bind_tools([search_papers])
        
        prompt = "I need to find 15 papers about transformers in natural language processing"
        print(f"\nPrompt: {prompt}")
        print("\nInvocando modelo...")
        
        result = llm.invoke(prompt)
        
        print("\n--- Resultados ---")
        if hasattr(result, 'tool_calls') and result.tool_calls:
            args = result.tool_calls[0].get('args', {})
            print(f"Argumentos extraídos: {args}")
            
            # Verificar que extrajo el query y max_results
            has_query = 'query' in args
            has_max = 'max_results' in args
            max_value = args.get('max_results', 0)
            
            print(f"¿Tiene 'query'?: {has_query}")
            print(f"¿Tiene 'max_results'?: {has_max}")
            print(f"Valor de max_results: {max_value}")
            
            if has_query and has_max and max_value == 15:
                print(f"\n✅ TEST 3 PASADO: Argumentos extraídos correctamente")
                return True
            else:
                print(f"\n⚠️ TEST 3 PARCIAL: Algunos argumentos incorrectos")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print("\n❌ TEST 3 FALLADO")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 3: {str(e)}")
        return False


def test_4_realistic_scenario():
    """Test 4: Escenario realista similar al uso en research_graph"""
    print("\n" + "="*70)
    print("TEST 4: Escenario Realista (Similar a Agent 1)")
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
            return f"[Mock] Searching Semantic Scholar for '{query}' (max: {max_results})"
        
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0,
            num_ctx=32768  # Contexto completo
        ).bind_tools([search_recent_papers])
        
        # Prompt similar al que usa Agent 1
        prompt = """You are a niche identification specialist. 
        Your task is to find recent research papers about 'deep learning for drug discovery'.
        Search for at most 10 recent papers on this topic."""
        
        print(f"\nPrompt: {prompt[:100]}...")
        print("\nInvocando modelo...")
        
        result = llm.invoke(prompt)
        
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
                if 'query' in args and 'drug' in args['query'].lower():
                    print(f"\n✅ TEST 4 PASADO: Comportamiento realista correcto")
                    return True
                else:
                    print(f"\n⚠️ TEST 4 PARCIAL: Herramienta correcta pero query impreciso")
                    return False
            else:
                print(f"\n❌ TEST 4 FALLADO: Herramienta incorrecta")
                return False
        else:
            print("❌ No se detectaron tool_calls")
            print(f"Content (primeros 200 chars): {result.content[:200] if hasattr(result, 'content') else 'N/A'}")
            print("\n❌ TEST 4 FALLADO")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR en Test 4: {str(e)}")
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
    print(" SUITE DE PRUEBAS: OLLAMA TOOL CALLING")
    print(" Modelo: Mistral 7B v0.3")
    print("="*70)
    
    # Verificar que Ollama está disponible
    print("\n[Pre-check] Verificando que Ollama está disponible...")
    try:
        test_llm = ChatOllama(model="mistral:7b", temperature=0)
        test_result = test_llm.invoke("Hello")
        print("✅ Ollama está funcionando correctamente")
        print(f"   Respuesta de prueba: {test_result.content[:50]}...")
    except Exception as e:
        print(f"❌ ERROR: No se puede conectar con Ollama")
        print(f"   Error: {str(e)}")
        print("\nAsegúrate de:")
        print("  1. Ejecutar: ollama serve")
        print("  2. Descargar modelo: ollama pull mistral:7b")
        sys.exit(1)
    
    # Ejecutar tests
    results = []
    results.append(("Test 1: Reconocimiento básico", test_1_basic_tool_recognition()))
    results.append(("Test 2: Múltiples herramientas", test_2_multiple_tools()))
    results.append(("Test 3: Argumentos complejos", test_3_complex_arguments()))
    results.append(("Test 4: Escenario realista", test_4_realistic_scenario()))
    
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
    print(" CONCLUSIÓN")
    print("="*70)
    
    if passed == total:
        print("\n✅✅✅ EXCELENTE: Mistral 7B soporta tool calling completamente")
        print("\nPróximo paso: Integrar con research_graph.py")
        print("  1. Modificar config/settings.py para agregar opción Ollama")
        print("  2. Crear función create_ollama_model() similar a create_openai_model()")
        print("  3. Probar con Agent 1 usando query simple")
    elif passed >= 2:
        print("\n⚠️ PARCIAL: Tool calling funciona pero con limitaciones")
        print(f"\nTests pasados: {passed}/{total}")
        print("\nRecomendación:")
        print("  - Probar con queries más simples en producción")
        print("  - O considerar Qwen2.5:8b como alternativa")
    else:
        print("\n❌ FALLIDO: Mistral 7B NO soporta tool calling adecuadamente")
        print("\nAlternativas:")
        print("  1. Probar Qwen2.5:8b (ollama pull qwen2.5:8b)")
        print("  2. Investigar otros modelos con tag 'tools' en Ollama")
        print("  3. Mantener GitHub Models como única opción")
    
    print("\n" + "="*70 + "\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrumpidos por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
