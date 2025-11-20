"""
Script para extraer funciones @tool de clases y convertirlas en funciones módulo.
"""
import re
from pathlib import Path

def extract_tool_functions(file_path):
    """Extrae funciones @tool de una clase y las convierte en funciones módulo."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @tool functions within the class
    # Pattern: captura desde @tool hasta el final de la función
    tool_pattern = r'(\n    @tool\([^)]+\)\n    async def [^(]+\([^)]+\)[^:]*:(?:\n(?:        .*|$))+?)(?=\n    (?:@|async def|def|class)|$)'
    
    tools = re.findall(tool_pattern, content)
    
    if not tools:
        return content
    
    print(f"  Encontradas {len(tools)} funciones @tool")
    
    # Remove tools from class (replace with pass or keep only init methods)
    for tool_func in tools:
        content = content.replace(tool_func, '')
    
    # Dedent tools (remove 4 spaces from each line)
    module_tools = []
    for tool_func in tools:
        lines = tool_func.split('\n')
        dedented = []
        for line in lines:
            if line.startswith('    '):
                dedented.append(line[4:])  # Remove 4 spaces
            else:
                dedented.append(line)
        module_tools.append('\n'.join(dedented))
    
    # Find the end of global instance section
    instance_pattern = r'(def get_\w+_tool\([^)]*\)[^:]*:.*?\n    return _get_\w+_tool_instance\([^)]*\)\n)'
    
    match = re.search(instance_pattern, content, re.DOTALL)
    if match:
        insert_pos = match.end()
        
        # Insert module-level tool functions
        tools_section = '\n\n# ============================================================\n'
        tools_section += '# Module-level tool functions (extracted from class)\n'
        tools_section += '# These use the singleton instance internally\n'
        tools_section += '# ============================================================\n'
        tools_section += '\n'.join(module_tools)
        
        content = content[:insert_pos] + tools_section + content[insert_pos:]
    
    return content

# Files to process
files_to_process = [
    'tools/scraping_tool.py',
    'tools/search_tool.py',
    'tools/pdf_tool.py',
    'tools/database_tool.py',
]

print("🔧 Extrayendo funciones @tool de clases...\n")

for file_path in files_to_process:
    full_path = Path(file_path)
    if not full_path.exists():
        print(f"⚠️  {file_path} - No encontrado")
        continue
    
    print(f"📝 Procesando {file_path}...")
    
    new_content = extract_tool_functions(full_path)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {file_path} - Completado\n")

print("🎉 ¡Refactorización completada!")
