"""
Script para corregir nombres de herramientas con espacios.
"""
import re
from pathlib import Path

def fix_tool_names(file_path: Path):
    """Reemplaza nombres de herramientas con espacios por snake_case."""
    content = file_path.read_text(encoding='utf-8')
    
    # Reemplazar @tool("Name With Spaces") por @tool("name_with_spaces")
    def replace_tool_name(match):
        name = match.group(1)
        snake_case = name.lower().replace(' ', '_')
        return f'@tool("{snake_case}")'
    
    new_content = re.sub(r'@tool\("([^"]+)"\)', replace_tool_name, content)
    
    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        return True
    return False

if __name__ == "__main__":
    tools_dir = Path("tools")
    fixed = 0
    
    for file in tools_dir.glob("*.py"):
        if fix_tool_names(file):
            fixed += 1
            print(f"✅ {file.name}")
    
    print(f"\n🎉 Corregidos {fixed} archivos")
