"""Script para REMOVER @staticmethod decorators."""
from pathlib import Path

def remove_staticmethod(file_path):
    """Remueve líneas con @staticmethod."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Skip lines that are just @staticmethod
        if line.strip() == '@staticmethod':
            continue
        new_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return True

# Archivos a procesar
files_to_fix = [
    'tools/scraping_tool.py',
    'tools/search_tool.py',
    'tools/pdf_tool.py',
    'tools/database_tool.py',
]

print("🔧 Removiendo @staticmethod...")
for file_path in files_to_fix:
    full_path = Path(file_path)
    if full_path.exists():
        remove_staticmethod(full_path)
        print(f"✅ {file_path}")
    else:
        print(f"⚠️  {file_path} - No encontrado")

print("\n🎉 Completado!")
