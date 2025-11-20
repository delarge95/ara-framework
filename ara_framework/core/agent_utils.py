"""
Utilidades para crear y ejecutar agentes con mejor manejo de errores.
"""
import structlog
from typing import List, Dict, Any, Optional, Union
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

logger = structlog.get_logger(__name__)


async def safe_agent_invoke(
    llm: Union[ChatGroq, ChatOpenAI],
    tools: List[BaseTool],
    messages: List[BaseMessage],
    max_iterations: int = 5,
) -> Dict[str, Any]:
    """
    Ejecuta un agente con manejo robusto de errores de tool calling.
    
    Args:
        llm: LLM configurado
        tools: Lista de herramientas disponibles
        messages: Mensajes del contexto
        max_iterations: Máximo de iteraciones tool-calling
    
    Returns:
        Dict con 'output' y 'tool_calls'
    """
    # Bind tools al LLM
    llm_with_tools = llm.bind_tools(tools) if tools else llm
    
    current_messages = messages.copy()
    tool_calls_made = []
    
    for iteration in range(max_iterations):
        try:
            # Invocar LLM
            response = await llm_with_tools.ainvoke(current_messages)
            
            # Si no hay tool calls, terminamos
            if not hasattr(response, 'tool_calls') or not response.tool_calls:
                return {
                    "output": response.content,
                    "tool_calls": tool_calls_made,
                }
            
            # Procesar tool calls
            current_messages.append(response)
            
            for tool_call in response.tool_calls:
                tool_calls_made.append({
                    "name": tool_call["name"],
                    "args": tool_call["args"],
                })
                
                # Buscar la tool
                tool = next((t for t in tools if t.name == tool_call["name"]), None)
                
                if not tool:
                    logger.error(
                        "tool_not_found",
                        tool_name=tool_call["name"],
                        available_tools=[t.name for t in tools],
                    )
                    # Agregar mensaje de error
                    current_messages.append(
                        ToolMessage(
                            content=f"Error: Tool '{tool_call['name']}' not found",
                            tool_call_id=tool_call.get("id", "unknown"),
                        )
                    )
                    continue
                
                try:
                    # Ejecutar tool
                    logger.info(
                        "executing_tool",
                        tool_name=tool.name,
                        args=tool_call["args"],
                    )
                    
                    result = await tool.ainvoke(tool_call["args"])
                    
                    # Convertir resultado a string si es necesario
                    if isinstance(result, dict):
                        result_str = str(result)
                    elif isinstance(result, list):
                        result_str = str(result)
                    else:
                        result_str = str(result)
                    
                    # Agregar resultado
                    current_messages.append(
                        ToolMessage(
                            content=result_str,
                            tool_call_id=tool_call.get("id", "unknown"),
                        )
                    )
                    
                    logger.info(
                        "tool_executed_successfully",
                        tool_name=tool.name,
                        result_length=len(result_str),
                    )
                    
                except Exception as tool_error:
                    logger.error(
                        "tool_execution_failed",
                        tool_name=tool.name,
                        error=str(tool_error),
                    )
                    # Agregar mensaje de error pero continuar
                    current_messages.append(
                        ToolMessage(
                            content=f"Error executing {tool.name}: {str(tool_error)}",
                            tool_call_id=tool_call.get("id", "unknown"),
                        )
                    )
        
        except Exception as e:
            error_msg = str(e)
            logger.error(
                "agent_iteration_failed",
                iteration=iteration,
                error=error_msg,
            )
            
            # Si es error de formato de tool calling, devolver respuesta sin tools
            if "tool" in error_msg.lower() or "function" in error_msg.lower():
                # Reintentar sin tools
                try:
                    response = await llm.ainvoke(current_messages)
                    return {
                        "output": response.content,
                        "tool_calls": tool_calls_made,
                        "error": f"Tool calling failed, completed without tools: {error_msg}",
                    }
                except Exception as retry_error:
                    return {
                        "output": f"[Agent failed after {iteration} iterations]",
                        "tool_calls": tool_calls_made,
                        "error": str(retry_error),
                    }
            
            # Otro tipo de error
            return {
                "output": f"[Agent failed: {error_msg}]",
                "tool_calls": tool_calls_made,
                "error": error_msg,
            }
    
    # Max iterations alcanzadas
    logger.warning(
        "max_iterations_reached",
        max_iterations=max_iterations,
        tool_calls=len(tool_calls_made),
    )
    
    # Hacer una última llamada sin tools para obtener respuesta
    try:
        final_response = await llm.ainvoke(current_messages)
        return {
            "output": final_response.content,
            "tool_calls": tool_calls_made,
            "warning": f"Max iterations ({max_iterations}) reached",
        }
    except Exception as e:
        return {
            "output": "[Max iterations reached, no final response]",
            "tool_calls": tool_calls_made,
            "error": str(e),
        }
