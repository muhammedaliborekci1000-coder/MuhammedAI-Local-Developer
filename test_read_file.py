import sys
sys.path.insert(0, '.')

from app.tools.file_reader import FileReader
from app.core.config import PROJECT_ROOT

reader = FileReader(project_root=PROJECT_ROOT)
content = reader.read('app/ai/agent_loop.py')

print(f'Content length: {len(content)}')
print(f'First 200 chars: {content[:200]}')
