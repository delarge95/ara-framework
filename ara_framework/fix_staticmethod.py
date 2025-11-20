"""Script para agregar @staticmethod antes de @tool decorators."""
import re
from pathlib import Path

def add_staticmethod(file_path):
    """Agrega @staticmethod antes de cada @tool() decorator."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: busca @tool("...") que NO esté precedido por @staticmethod
    # Reemplaza con @staticmethod\n    @tool("...")
    pattern = r'(\n    )(@tool\(")'
    
    def replace_func(match):
        indent = match.group(1)
        tool_decorator = match.group(2)
        # Solo agregar si no hay @staticmethod antes
        return f'{indent}@staticmethod\n    {tool_decorator}'
    
    # Primero verificar si ya tiene @staticmethod
    # Solo reemplazar donde NO haya @staticmethod antes
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('@tool(') and i > 0:
            # Verificar línea anterior
            prev_line = lines[i-1].strip()
            if prev_line != '@staticmethod':
                # Agregar @staticmethod
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + '@staticmethod')
        new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

# Archivos a procesar
files_to_fix = [
    'tools/search_tool.py',
    'tools/pdf_tool.py',
    'tools/database_tool.py',
]

print("🔧 Agregando @staticmethod a tools...")
for file_path in files_to_fix:
    full_path = Path(file_path)
    if full_path.exists():
        add_staticmethod(full_path)
        print(f"✅ {file_path}")
    else:
        print(f"⚠️  {file_path} - No encontrado")

print("\n🎉 Completado!")
