"""
MuhammedAI Local Developer - Web Arayüzü
FastAPI tabanlı web arayüzü.
"""

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.ai.ollama_client import OllamaClient
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.tools.tool_registry import ToolRegistry
from app.core.config import OLLAMA_HOST, DEFAULT_MODEL, PROJECT_ROOT
from app.editor.syntax_highlighting import SyntaxHighlighter, Theme
from app.editor.multiple_tabs import TabManager, TabGroup
from app.editor.terminal_integration import TerminalManager, TerminalConfig, TerminalType
from app.editor.git_status import GitStatusEngine
from app.editor.auto_completion import AutoCompleter
from app.editor.debugging import DebuggingEngine, DebugConfig
from app.editor.collaboration import CollaborationEngine
from app.editor.cloud_sync import CloudSyncEngine, CloudSyncConfig
from app.editor.plugin_system import PluginEngine
from app.editor.real_debugger import RealDebugger
from app.editor.real_git import RealGit

app = FastAPI(title="MuhammedAI Local Developer")

# Static files ve templates - PyInstaller uyumlu
if getattr(sys, 'frozen', False):
    # EXE çalıştırılıyor - _MEIPASS kullan
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(sys.executable).parent / "_internal"
    templates_dir = base_path / "app" / "ui" / "templates"
    static_dir = base_path / "app" / "ui" / "static"
else:
    # Normal Python çalıştırması - base_path zaten app/ui
    base_path = Path(__file__).parent
    templates_dir = base_path / "templates"
    static_dir = base_path / "static"

# Dizinleri oluştur (normal modda gerekli)
if not getattr(sys, 'frozen', False):
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Jinja2 templates
if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))
    # Cache'i temizle
    if hasattr(templates.env, 'cache'):
        templates.env.cache.clear()
else:
    # Fallback - templates bulunamazsa hata ver
    raise RuntimeError(f"Templates dizini bulunamadı: {templates_dir}")

# Global state
active_sessions = {}

# Editor global state
syntax_highlighter = SyntaxHighlighter(theme=Theme.VS_CODE_DARK)
tab_manager = TabManager()
auto_completer = AutoCompleter(project_root=str(PROJECT_ROOT))
debugging_engine = DebuggingEngine(DebugConfig())
real_debugger = RealDebugger()
collaboration_engine = CollaborationEngine()
cloud_sync_engine = CloudSyncEngine(CloudSyncConfig())
plugin_engine = PluginEngine()
terminal_manager = TerminalManager(TerminalConfig())
real_git = RealGit(str(PROJECT_ROOT))
active_sessions = {}  # WebSocket sessions for collaboration


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Ana sayfa."""
    # Template'i doğrudan oku
    template_file = templates_dir / "index.html"
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return f"Template bulunamadı: {template_file}"


@app.get("/api/status")
async def get_status():
    """Ollama ve sistem durumunu kontrol et."""
    try:
        import ollama
        client = ollama.Client(host=OLLAMA_HOST)
        models = client.list()
        model_names = [m.model for m in models.models]
        
        return JSONResponse({
            "ollama_connected": True,
            "models": model_names,
            "default_model": DEFAULT_MODEL,
            "project_root": str(PROJECT_ROOT)
        })
    except Exception as e:
        return JSONResponse({
            "ollama_connected": False,
            "error": str(e)
        })


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket bağlantısı için gerçek zamanlı sohbet."""
    await websocket.accept()
    
    session_id = id(websocket)
    active_sessions[session_id] = websocket
    
    # Onay yanıtı için sync/async köprü
    approval_future = None
    
    try:
        # Session başlat
        ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
        tool_registry = ToolRegistry()
        config = LoopConfig(max_iterations=10, enable_logging=True)
        
        # Senkron approval callback - async WebSocket ile köprü
        def approval_callback(tool_name: str, arguments: dict) -> bool:
            nonlocal approval_future
            try:
                # Event loop'u al
                loop = asyncio.get_event_loop()
                
                # Future oluştur
                approval_future = loop.create_future()
                
                # Onay isteği gönder
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json({
                        "type": "approval_request",
                        "tool_name": tool_name,
                        "arguments": arguments
                    }),
                    loop
                )
                
                # Yanıtı bekle (thread-safe)
                result = asyncio.run_coroutine_threadsafe(approval_future, loop).result(timeout=30)
                return result
            except Exception as e:
                print(f"Approval callback hatası: {e}")
                return False
        
        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )
        
        await websocket.send_json({
            "type": "system",
            "message": "Bağlantı kuruldu. Görev bekleniyor..."
        })
        
        # Mesaj döngüsü
        while True:
            data = await websocket.receive_json()
            
            # Onay yanıtı mı?
            if data.get("type") == "approval_response":
                if approval_future and not approval_future.done():
                    approval_future.set_result(data.get("approved", False))
                continue
            
            if data.get("type") == "task":
                task = data.get("task", "")
                
                await websocket.send_json({
                    "type": "status",
                    "message": "Görev çalıştırılıyor..."
                })
                
                # Görevi async çalıştır
                try:
                    result = await asyncio.to_thread(agent_loop.run, task)
                    
                    await websocket.send_json({
                        "type": "result",
                        "success": result.success,
                        "iterations": result.iterations,
                        "tool_calls_count": len(result.tool_calls),
                        "final_response": result.final_response,
                        "error": result.error
                    })
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
    
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        if session_id in active_sessions:
            del active_sessions[session_id]
    except Exception as e:
        print(f"WebSocket hatası: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass


@app.get("/api/project/structure")
async def get_project_structure():
    """Proje yapısını al."""
    try:
        from app.tools.project_structure_analyzer import ProjectStructureAnalyzer
        analyzer = ProjectStructureAnalyzer()
        structure = analyzer.analyze(str(PROJECT_ROOT))
        return JSONResponse(structure)
    except Exception as e:
        return JSONResponse({"error": str(e)})


@app.get("/api/project/files")
async def get_project_files(path: str = ""):
    """Proje dosyalarını listele."""
    # Path'i normalize et ve PROJECT_ROOT altında olduğunu doğrula
    target_path = PROJECT_ROOT / path if path else PROJECT_ROOT
    target_path = target_path.resolve()
    
    # PROJECT_ROOT'u da normalize et
    project_root_resolved = PROJECT_ROOT.resolve()
    
    # Path traversal kontrolü - hedef PROJECT_ROOT altında olmalı
    try:
        target_path.relative_to(project_root_resolved)
    except ValueError:
        raise HTTPException(status_code=403, detail="Erişim reddedildi: proje dışı path")
    
    if not target_path.exists():
        return JSONResponse({"error": "Path bulunamadı"})
    
    try:
        if target_path.is_file():
            from app.tools.file_reader import FileReader
            reader = FileReader()
            content = reader.read(str(target_path))
            return JSONResponse({"path": str(target_path.relative_to(project_root_resolved)), "content": content})
        else:
            files = []
            for item in target_path.iterdir():
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "path": str(item.relative_to(project_root_resolved)),
                        "type": "file"
                    })
                elif item.is_dir() and item.name not in [".git", ".venv", "venv", "__pycache__", "node_modules"]:
                    files.append({
                        "name": item.name,
                        "path": str(item.relative_to(project_root_resolved)),
                        "type": "directory"
                    })
            return JSONResponse({"path": str(target_path.relative_to(project_root_resolved)), "files": files})
    except Exception as e:
        return JSONResponse({"error": "Dosya erişim hatası"})


# ==================== VS Code Entegrasyonu Endpoint'leri ====================

@app.post("/api/editor/syntax-highlight")
async def syntax_highlight(request: Request):
    """Kod için syntax highlighting."""
    try:
        data = await request.json()
        code = data.get("code", "")
        language = data.get("language", "python")
        theme_name = data.get("theme", "vs_code_dark")
        
        # Theme'i al
        theme_map = {
            "vs_code_dark": Theme.VS_CODE_DARK,
            "monokai": Theme.MONOKAI,
            "dracula": Theme.DRACULA,
            "github_light": Theme.GITHUB_LIGHT,
            "github_dark": Theme.GITHUB_DARK,
            "solarized_dark": Theme.SOLARIZED_DARK,
            "solarized_light": Theme.SOLARIZED_LIGHT
        }
        theme = theme_map.get(theme_name, Theme.VS_CODE_DARK)
        
        # Highlighter'ı güncelle
        global syntax_highlighter
        syntax_highlighter = SyntaxHighlighter(theme=theme)
        
        # Highlight et
        result = syntax_highlighter.highlight(code, language)
        
        return JSONResponse({
            "success": result.success,
            "html": result.html,
            "lines_count": len(result.lines),
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/create")
async def create_tab(request: Request):
    """Yeni tab oluştur."""
    try:
        data = await request.json()
        title = data.get("title", "Untitled")
        content = data.get("content", "")
        file_path = data.get("file_path")
        language = data.get("language", "python")
        group_name = data.get("group", "ungrouped")
        
        group_map = {
            "ungrouped": TabGroup.UNGROUPED,
            "editors": TabGroup.EDITORS,
            "terminals": TabGroup.TERMINALS,
            "preview": TabGroup.PREVIEW,
            "debug": TabGroup.DEBUG
        }
        group = group_map.get(group_name, TabGroup.UNGROUPED)
        
        result = tab_manager.create_tab(title, content, file_path, language, group)
        
        return JSONResponse({
            "success": result.success,
            "tab_id": result.active_tab.id if result.active_tab else None,
            "tabs_count": result.total_tabs,
            "active_tab": {
                "id": result.active_tab.id,
                "title": result.active_tab.title,
                "language": result.active_tab.language
            } if result.active_tab else None,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/close")
async def close_tab(request: Request):
    """Tab kapat."""
    try:
        data = await request.json()
        tab_id = data.get("tab_id")
        
        if not tab_id:
            return JSONResponse({"success": False, "error": "tab_id required"})
        
        result = tab_manager.close_tab(tab_id)
        
        return JSONResponse({
            "success": result.success,
            "tabs_count": result.total_tabs,
            "active_tab": {
                "id": result.active_tab.id,
                "title": result.active_tab.title
            } if result.active_tab else None,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/switch")
async def switch_tab(request: Request):
    """Tab'a geç."""
    try:
        data = await request.json()
        tab_id = data.get("tab_id")
        
        if not tab_id:
            return JSONResponse({"success": False, "error": "tab_id required"})
        
        result = tab_manager.switch_tab(tab_id)
        
        return JSONResponse({
            "success": result.success,
            "active_tab": {
                "id": result.active_tab.id,
                "title": result.active_tab.title,
                "content": result.active_tab.content
            } if result.active_tab else None,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/tabs")
async def get_tabs():
    """Tüm tab'ları al."""
    try:
        tabs = tab_manager.get_all_tabs()
        active_tab = tab_manager.get_active_tab()
        
        tabs_data = [
            {
                "id": tab.id,
                "title": tab.title,
                "language": tab.language,
                "state": tab.state.value,
                "is_modified": tab.is_modified,
                "is_pinned": tab.is_pinned,
                "is_read_only": tab.is_read_only,
                "group": tab.group.value
            }
            for tab in tabs
        ]
        
        return JSONResponse({
            "success": True,
            "tabs": tabs_data,
            "active_tab_id": active_tab.id if active_tab else None,
            "total_tabs": len(tabs)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/update")
async def update_tab(request: Request):
    """Tab içeriğini güncelle."""
    try:
        data = await request.json()
        tab_id = data.get("tab_id")
        content = data.get("content", "")
        
        if not tab_id:
            return JSONResponse({"success": False, "error": "tab_id required"})
        
        result = tab_manager.update_tab_content(tab_id, content)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/pin")
async def pin_tab(request: Request):
    """Tab'ı sabitle."""
    try:
        data = await request.json()
        tab_id = data.get("tab_id")
        
        if not tab_id:
            return JSONResponse({"success": False, "error": "tab_id required"})
        
        result = tab_manager.pin_tab(tab_id)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/unpin")
async def unpin_tab(request: Request):
    """Tab sabitlemesini kaldır."""
    try:
        data = await request.json()
        tab_id = data.get("tab_id")
        
        if not tab_id:
            return JSONResponse({"success": False, "error": "tab_id required"})
        
        result = tab_manager.unpin_tab(tab_id)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/tabs/read-only")
async def set_read_only(request: Request):
    """Tab'ı read-only yap."""
    try:
        data = await request.json()
        tab_id = data.get("tab_id")
        read_only = data.get("read_only", True)
        
        if not tab_id:
            return JSONResponse({"success": False, "error": "tab_id required"})
        
        result = tab_manager.set_read_only(tab_id, read_only)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/terminal/create")
async def create_terminal(request: Request):
    """Terminal oturumu oluştur."""
    try:
        data = await request.json()
        name = data.get("name", "Terminal")
        terminal_type_name = data.get("type", "command")
        working_directory = data.get("working_directory")
        
        type_map = {
            "command": TerminalType.COMMAND,
            "powershell": TerminalType.POWERSHELL,
            "bash": TerminalType.BASH,
            "zsh": TerminalType.ZSH,
            "fish": TerminalType.FISH,
            "python": TerminalType.PYTHON,
            "node": TerminalType.NODE
        }
        terminal_type = type_map.get(terminal_type_name, TerminalType.COMMAND)
        
        result = terminal_manager.create_session(name, terminal_type, working_directory)
        
        return JSONResponse({
            "success": result.success,
            "session_id": result.session.id if result.session else None,
            "session": {
                "id": result.session.id,
                "name": result.session.name,
                "type": result.session.terminal_type.value,
                "state": result.session.state.value
            } if result.session else None,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/terminal/execute")
async def execute_terminal_command(request: Request):
    """Terminal'de komut çalıştır."""
    try:
        data = await request.json()
        command = data.get("command")
        session_id = data.get("session_id")
        
        if not command:
            return JSONResponse({"success": False, "error": "command required"})
        
        result = terminal_manager.execute_command(command, session_id)
        
        return JSONResponse({
            "success": result.success,
            "output": result.session.output if result.session else [],
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/terminal/sessions")
async def get_terminal_sessions():
    """Tüm terminal oturumlarını al."""
    try:
        sessions = terminal_manager.get_all_sessions()
        active_session = terminal_manager.get_active_session()
        
        sessions_data = [
            {
                "id": session.id,
                "name": session.name,
                "type": session.terminal_type.value,
                "state": session.state.value,
                "working_directory": session.working_directory,
                "is_visible": session.is_visible
            }
            for session in sessions
        ]
        
        return JSONResponse({
            "success": True,
            "sessions": sessions_data,
            "active_session_id": active_session.id if active_session else None
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/start")
async def lsp_start():
    """LSP manager'ı başlat."""
    try:
        project_key = str(PROJECT_ROOT)
        
        if project_key in lsp_managers:
            manager = lsp_managers[project_key]
            if manager.is_alive():
                return JSONResponse({"success": True, "message": "LSP already running"})
        
        config = LSPManagerConfig(project_root=str(PROJECT_ROOT))
        manager = LSPManager(config)
        
        # Sync start'ı async context'te çalıştır
        success = await asyncio.to_thread(manager.start)
        
        if success:
            lsp_managers[project_key] = manager
            return JSONResponse({"success": True, "message": "LSP started"})
        else:
            return JSONResponse({"success": False, "error": "Failed to start LSP"})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/stop")
async def lsp_stop():
    """LSP manager'ı durdur."""
    try:
        project_key = str(PROJECT_ROOT)
        
        if project_key in lsp_managers:
            manager = lsp_managers[project_key]
            await asyncio.to_thread(manager.stop)
            del lsp_managers[project_key]
            return JSONResponse({"success": True, "message": "LSP stopped"})
        else:
            return JSONResponse({"success": False, "error": "LSP not running"})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/document/open")
async def lsp_open_document(request: Request):
    """Dokümanı aç."""
    try:
        data = await request.json()
        uri = data.get("uri")
        language_id = data.get("language_id", "python")
        text = data.get("text", "")
        
        if not uri:
            return JSONResponse({"success": False, "error": "uri required"})
        
        project_key = str(PROJECT_ROOT)
        if project_key not in lsp_managers:
            return JSONResponse({"success": False, "error": "LSP not running"})
        
        manager = lsp_managers[project_key]
        success = await asyncio.to_thread(manager.open_document, uri, language_id, text)
        
        return JSONResponse({
            "success": success,
            "message": "Document opened" if success else "Failed to open document"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/completion")
async def auto_completion(request: Request):
    """Auto completion isteği (AI tabanlı değil)."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        line = data.get("line", 0)
        column = data.get("column", 0)
        prefix = data.get("prefix", "")
        
        if not file_path:
            return JSONResponse({"success": False, "error": "file_path required"})
        
        result = auto_completer.complete(file_path, line, column, prefix)
        
        return JSONResponse({
            "success": result.success,
            "items": [
                {
                    "label": item.label,
                    "type": item.type.value,
                    "detail": item.detail,
                    "documentation": item.documentation,
                    "insert_text": item.insert_text or item.label,
                    "score": item.score
                }
                for item in result.items
            ],
            "context": result.context.value if result.context else None,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debug/start")
async def debug_start(request: Request):
    """Debug session başlat."""
    try:
        data = await request.json()
        uri = data.get("uri")
        
        if not uri:
            return JSONResponse({"success": False, "error": "uri required"})
        
        session = debugging_engine.start_session(uri)
        
        return JSONResponse({
            "success": True,
            "session_id": session.id,
            "state": session.state.value,
            "uri": session.uri
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debug/stop")
async def debug_stop(request: Request):
    """Debug session durdur."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        
        if not session_id:
            return JSONResponse({"success": False, "error": "session_id required"})
        
        debugging_engine.stop_session(session_id)
        
        return JSONResponse({
            "success": True,
            "message": f"Session {session_id} stopped"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debug/breakpoint")
async def debug_add_breakpoint(request: Request):
    """Breakpoint ekle."""
    try:
        data = await request.json()
        uri = data.get("uri")
        line = data.get("line")
        condition = data.get("condition")
        kind = data.get("kind", "line")
        
        if not uri or line is None:
            return JSONResponse({"success": False, "error": "uri and line required"})
        
        from app.editor.debugging import BreakpointKind
        kind_map = {
            "line": BreakpointKind.LINE,
            "function": BreakpointKind.FUNCTION,
            "conditional": BreakpointKind.CONDITIONAL,
            "logpoint": BreakpointKind.LOGPOINT
        }
        bp_kind = kind_map.get(kind, BreakpointKind.LINE)
        
        breakpoint = debugging_engine.add_breakpoint(uri, line, condition, bp_kind)
        
        return JSONResponse({
            "success": True,
            "breakpoint_id": breakpoint.id,
            "kind": breakpoint.kind.value,
            "line": breakpoint.line,
            "condition": breakpoint.condition
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.delete("/api/editor/debug/breakpoint")
async def debug_remove_breakpoint(request: Request):
    """Breakpoint kaldır."""
    try:
        data = await request.json()
        breakpoint_id = data.get("breakpoint_id")
        
        if not breakpoint_id:
            return JSONResponse({"success": False, "error": "breakpoint_id required"})
        
        debugging_engine.remove_breakpoint(breakpoint_id)
        
        return JSONResponse({
            "success": True,
            "message": f"Breakpoint {breakpoint_id} removed"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/debug/breakpoints")
async def debug_get_breakpoints():
    """Tüm breakpoint'leri al."""
    try:
        session = debugging_engine.get_current_session()
        if not session:
            return JSONResponse({"success": False, "error": "No active session"})
        
        breakpoints = [
            {
                "id": bp.id,
                "kind": bp.kind.value,
                "uri": bp.uri,
                "line": bp.line,
                "condition": bp.condition,
                "enabled": bp.enabled
            }
            for bp in session.breakpoints
        ]
        
        return JSONResponse({
            "success": True,
            "breakpoints": breakpoints,
            "total": len(breakpoints)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debug/step")
async def debug_step(request: Request):
    """Step (over/into/out)."""
    try:
        data = await request.json()
        step_kind = data.get("kind", "over")
        
        from app.editor.debugging import StepKind
        step_map = {
            "over": StepKind.OVER,
            "into": StepKind.INTO,
            "out": StepKind.OUT,
            "continue": StepKind.CONTINUE
        }
        kind = step_map.get(step_kind, StepKind.OVER)
        
        session = debugging_engine.get_current_session()
        if not session:
            return JSONResponse({"success": False, "error": "No active session"})
        
        session.state = session.state.STEPPING
        
        return JSONResponse({
            "success": True,
            "message": f"Step {step_kind}",
            "state": session.state.value
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/debug/variables")
async def debug_get_variables():
    """Değişkenleri al."""
    try:
        session = debugging_engine.get_current_session()
        if not session:
            return JSONResponse({"success": False, "error": "No active session"})
        
        variables = [
            {
                "name": var.name,
                "value": str(var.value),
                "type": var.type,
                "scope": var.scope.value
            }
            for var in session.variables
        ]
        
        return JSONResponse({
            "success": True,
            "variables": variables,
            "total": len(variables)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/debug/stack")
async def debug_get_stack():
    """Call stack'i al."""
    try:
        session = debugging_engine.get_current_session()
        if not session:
            return JSONResponse({"success": False, "error": "No active session"})
        
        stack_frames = [
            {
                "id": frame.id,
                "name": frame.name,
                "uri": frame.uri,
                "line": frame.line,
                "column": frame.column
            }
            for frame in session.stack_frames
        ]
        
        return JSONResponse({
            "success": True,
            "stack_frames": stack_frames,
            "total": len(stack_frames)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/collaboration/session")
async def create_collaboration_session(request: Request):
    """Collaboration session oluştur."""
    try:
        data = await request.json()
        name = data.get("name", "Untitled Session")
        owner_id = data.get("owner_id", "user_1")
        
        result = collaboration_engine.create_session(name, owner_id)
        
        return JSONResponse({
            "success": result.success,
            "session_id": result.session.id if result.session else None,
            "session_name": result.session.name if result.session else None,
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "role": u.role.value,
                    "is_online": u.is_online
                }
                for u in result.users
            ],
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/collaboration/join")
async def join_collaboration_session(request: Request):
    """Collaboration session'a katıl."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        user_id = data.get("user_id")
        user_name = data.get("user_name", "Anonymous")
        
        if not session_id or not user_id:
            return JSONResponse({"success": False, "error": "session_id and user_id required"})
        
        result = collaboration_engine.join_session(session_id, user_id, user_name)
        
        return JSONResponse({
            "success": result.success,
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "role": u.role.value,
                    "is_online": u.is_online
                }
                for u in result.users
            ],
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/collaboration/leave")
async def leave_collaboration_session(request: Request):
    """Collaboration session'dan ayrıl."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        user_id = data.get("user_id")
        
        if not session_id or not user_id:
            return JSONResponse({"success": False, "error": "session_id and user_id required"})
        
        result = collaboration_engine.leave_session(session_id, user_id)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/collaboration/comment")
async def add_collaboration_comment(request: Request):
    """Comment ekle."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        user_id = data.get("user_id")
        user_name = data.get("user_name", "Anonymous")
        content = data.get("content")
        file_path = data.get("file_path")
        line = data.get("line")
        
        if not session_id or not user_id or not content:
            return JSONResponse({"success": False, "error": "session_id, user_id and content required"})
        
        result = collaboration_engine.add_comment(session_id, user_id, user_name, content, file_path, line)
        
        return JSONResponse({
            "success": result.success,
            "comments": [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "user_name": c.user_name,
                    "content": c.content,
                    "file_path": c.file_path,
                    "line": c.line,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "resolved": c.resolved
                }
                for c in result.comments
            ],
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/collaboration/session")
async def get_collaboration_session():
    """Collaboration session bilgilerini al."""
    try:
        result = collaboration_engine.get_current_session()
        
        if not result.session:
            return JSONResponse({"success": False, "error": "No active session"})
        
        return JSONResponse({
            "success": result.success,
            "session_id": result.session.id,
            "session_name": result.session.name,
            "owner_id": result.session.owner_id,
            "status": result.session.status.value,
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "role": u.role.value,
                    "is_online": u.is_online
                }
                for u in result.users
            ],
            "comments": [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "user_name": c.user_name,
                    "content": c.content,
                    "file_path": c.file_path,
                    "line": c.line,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "resolved": c.resolved
                }
                for c in result.comments
            ]
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/collaboration/role")
async def update_collaboration_role(request: Request):
    """Kullanıcı rolünü güncelle."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        user_id = data.get("user_id")
        role_name = data.get("role", "viewer")
        
        if not session_id or not user_id:
            return JSONResponse({"success": False, "error": "session_id and user_id required"})
        
        from app.editor.collaboration import CollaborationRole
        role_map = {
            "owner": CollaborationRole.OWNER,
            "editor": CollaborationRole.EDITOR,
            "viewer": CollaborationRole.VIEWER,
            "commenter": CollaborationRole.COMMENTER
        }
        role = role_map.get(role_name, CollaborationRole.VIEWER)
        
        result = collaboration_engine.update_user_role(session_id, user_id, role)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/cloud-sync/sync")
async def cloud_sync(request: Request):
    """Cloud sync."""
    try:
        data = await request.json()
        direction_name = data.get("direction", "bidirectional")
        
        from app.editor.cloud_sync import SyncDirection
        direction_map = {
            "upload": SyncDirection.UPLOAD,
            "download": SyncDirection.DOWNLOAD,
            "bidirectional": SyncDirection.BIDIRECTIONAL
        }
        direction = direction_map.get(direction_name, SyncDirection.BIDIRECTIONAL)
        
        result = cloud_sync_engine.sync(direction)
        
        return JSONResponse({
            "success": result.success,
            "files_synced": result.files_synced,
            "files_failed": result.files_failed,
            "conflicts": result.conflicts,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/cloud-sync/file")
async def add_cloud_sync_file(request: Request):
    """Dosyayı sync'e ekle."""
    try:
        data = await request.json()
        path = data.get("path")
        local_hash = data.get("local_hash")
        
        if not path:
            return JSONResponse({"success": False, "error": "path required"})
        
        sync_file = cloud_sync_engine.add_file(path, local_hash)
        
        return JSONResponse({
            "success": True,
            "path": sync_file.path,
            "status": sync_file.status.value,
            "last_synced": sync_file.last_synced.isoformat() if sync_file.last_synced else None
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.delete("/api/editor/cloud-sync/file")
async def remove_cloud_sync_file(request: Request):
    """Dosyayı sync'ten kaldır."""
    try:
        data = await request.json()
        path = data.get("path")
        
        if not path:
            return JSONResponse({"success": False, "error": "path required"})
        
        success = cloud_sync_engine.remove_file(path)
        
        return JSONResponse({
            "success": success,
            "message": f"File {path} removed from sync" if success else f"File {path} not found"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/cloud-sync/status")
async def get_cloud_sync_status():
    """Cloud sync durumunu al."""
    try:
        status = cloud_sync_engine.get_sync_status()
        return JSONResponse({
            "success": True,
            "status": status
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/cloud-sync/files")
async def get_cloud_sync_files():
    """Tüm sync dosyalarını al."""
    try:
        files = cloud_sync_engine.get_all_files()
        
        return JSONResponse({
            "success": True,
            "files": [
                {
                    "path": f.path,
                    "status": f.status.value,
                    "last_synced": f.last_synced.isoformat() if f.last_synced else None,
                    "conflict": f.conflict
                }
                for f in files
            ],
            "total": len(files)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/cloud-sync/resolve")
async def resolve_cloud_sync_conflict(request: Request):
    """Sync conflict çöz."""
    try:
        data = await request.json()
        path = data.get("path")
        resolution = data.get("resolution", "local")
        
        if not path:
            return JSONResponse({"success": False, "error": "path required"})
        
        result = cloud_sync_engine.resolve_conflict(path, resolution)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/cloud-sync/configure")
async def configure_cloud_provider(request: Request):
    """Cloud provider yapılandır."""
    try:
        data = await request.json()
        provider_name = data.get("provider", "none")
        config = data.get("config", {})
        
        from app.editor.cloud_sync import CloudProvider
        provider_map = {
            "none": CloudProvider.NONE,
            "github": CloudProvider.GITHUB,
            "gitlab": CloudProvider.GITLAB,
            "dropbox": CloudProvider.DROPBOX,
            "google_drive": CloudProvider.GOOGLE_DRIVE,
            "one_drive": CloudProvider.ONE_DRIVE
        }
        provider = provider_map.get(provider_name, CloudProvider.NONE)
        
        result = cloud_sync_engine.configure_provider(provider, config)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/cloud-sync/history")
async def get_cloud_sync_history():
    """Sync geçmişini al."""
    try:
        history = cloud_sync_engine.get_sync_history()
        
        return JSONResponse({
            "success": True,
            "history": history,
            "total": len(history)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/plugins")
async def get_plugins():
    """Tüm plugin'leri al."""
    try:
        plugins = plugin_engine.get_all_plugins()
        
        return JSONResponse({
            "success": True,
            "plugins": [
                {
                    "id": p.id,
                    "name": p.name,
                    "version": p.version,
                    "description": p.description,
                    "author": p.author,
                    "type": p.plugin_type.value,
                    "status": p.status.value,
                    "enabled": p.enabled,
                    "installed_at": p.installed_at.isoformat() if p.installed_at else None
                }
                for p in plugins
            ],
            "total": len(plugins)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/plugins/install")
async def install_plugin(request: Request):
    """Plugin yükle."""
    try:
        data = await request.json()
        plugin_id = data.get("plugin_id")
        plugin_data = data.get("plugin_data", {})
        
        if not plugin_id:
            return JSONResponse({"success": False, "error": "plugin_id required"})
        
        result = plugin_engine.install_plugin(plugin_id, plugin_data)
        
        return JSONResponse({
            "success": result.success,
            "plugin": {
                "id": result.plugin.id,
                "name": result.plugin.name,
                "version": result.plugin.version
            } if result.plugin else None,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.delete("/api/editor/plugins/uninstall")
async def uninstall_plugin(request: Request):
    """Plugin kaldır."""
    try:
        data = await request.json()
        plugin_id = data.get("plugin_id")
        
        if not plugin_id:
            return JSONResponse({"success": False, "error": "plugin_id required"})
        
        result = plugin_engine.uninstall_plugin(plugin_id)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/plugins/enable")
async def enable_plugin(request: Request):
    """Plugin aktifleştir."""
    try:
        data = await request.json()
        plugin_id = data.get("plugin_id")
        
        if not plugin_id:
            return JSONResponse({"success": False, "error": "plugin_id required"})
        
        result = plugin_engine.enable_plugin(plugin_id)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/plugins/disable")
async def disable_plugin(request: Request):
    """Plugin devre dışı bırak."""
    try:
        data = await request.json()
        plugin_id = data.get("plugin_id")
        
        if not plugin_id:
            return JSONResponse({"success": False, "error": "plugin_id required"})
        
        result = plugin_engine.disable_plugin(plugin_id)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/plugins/configure")
async def configure_plugin(request: Request):
    """Plugin yapılandır."""
    try:
        data = await request.json()
        plugin_id = data.get("plugin_id")
        config = data.get("config", {})
        
        if not plugin_id:
            return JSONResponse({"success": False, "error": "plugin_id required"})
        
        result = plugin_engine.configure_plugin(plugin_id, config)
        
        return JSONResponse({
            "success": result.success,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/plugins/search")
async def search_plugins():
    """Plugin ara."""
    try:
        # Mock search - tüm plugin'leri döndür
        plugins = plugin_engine.get_all_plugins()
        
        return JSONResponse({
            "success": True,
            "plugins": [
                {
                    "id": p.id,
                    "name": p.name,
                    "version": p.version,
                    "description": p.description,
                    "author": p.author,
                    "type": p.plugin_type.value
                }
                for p in plugins
            ],
            "total": len(plugins)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/files")
async def get_files(path: str = ""):
    """Gerçek dosya sisteminden dosya listesini al."""
    try:
        from pathlib import Path
        
        if path:
            target_path = Path(path)
        else:
            target_path = PROJECT_ROOT
        
        if not target_path.exists():
            return JSONResponse({"success": False, "error": "Path not found"})
        
        if not target_path.is_dir():
            return JSONResponse({"success": False, "error": "Not a directory"})
        
        items = []
        for item in target_path.iterdir():
            # .git, __pycache__, node_modules gibi dizinleri atla
            if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules', 'dist', 'build']:
                continue
            
            items.append({
                "name": item.name,
                "path": str(item),
                "type": "folder" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0
            })
        
        # Sırala: klasörler önce, sonra dosyalar
        items.sort(key=lambda x: (x["type"] != "folder", x["name"].lower()))
        
        return JSONResponse({
            "success": True,
            "path": str(target_path),
            "items": items,
            "total": len(items)
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/terminal/command")
async def execute_terminal_command(request: Request):
    """Terminal komutu çalıştır (gerçek subprocess)."""
    try:
        import subprocess
        import shlex
        
        data = await request.json()
        command = data.get("command", "")
        cwd = data.get("cwd", str(PROJECT_ROOT))
        
        if not command:
            return JSONResponse({"success": False, "error": "Command required"})
        
        # Komutu çalıştır
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate(timeout=30)
        
        return JSONResponse({
            "success": True,
            "exit_code": process.returncode,
            "stdout": stdout,
            "stderr": stderr
        })
    except subprocess.TimeoutExpired:
        return JSONResponse({"success": False, "error": "Command timeout"})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/git/status")
async def get_git_status():
    """Gerçek git status al."""
    try:
        import subprocess
        
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return JSONResponse({
                "success": True,
                "branch": "main",
                "changed": 0,
                "staged": 0,
                "untracked": 0
            })
        
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        changed = 0
        staged = 0
        untracked = 0
        
        for line in lines:
            if line:
                status = line[:2]
                if 'M' in status or 'D' in status or 'R' in status:
                    changed += 1
                if status[0] in ['M', 'A', 'D', 'R']:
                    staged += 1
                if status[1] == '?':
                    untracked += 1
        
        # Branch al
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "main"
        
        return JSONResponse({
            "success": True,
            "branch": branch,
            "changed": changed,
            "staged": staged,
            "untracked": untracked
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debugger/start")
async def debugger_start(request: Request):
    """Debugger session başlat (gerçek pdb)."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        
        if not file_path:
            return JSONResponse({"success": False, "error": "file_path required"})
        
        result = real_debugger.start(file_path)
        
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debugger/breakpoint")
async def debugger_breakpoint(request: Request):
    """Breakpoint ekle/kaldır."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        file_path = data.get("file_path")
        line = data.get("line")
        action = data.get("action", "add")  # add or remove
        
        if action == "add":
            result = real_debugger.add_breakpoint(file_path, line)
        else:
            result = real_debugger.remove_breakpoint(file_path, line)
        
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debugger/step")
async def debugger_step(request: Request):
    """Debugger step (into, over, out)."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        action = data.get("action", "over")  # into, over, out, continue
        
        result = real_debugger.step(action)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/debugger/variables")
async def debugger_variables(session_id: str):
    """Değişkenleri al."""
    try:
        result = real_debugger.get_variables()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/debugger/stack")
async def debugger_stack(session_id: str):
    """Stack trace al."""
    try:
        result = real_debugger.get_stack()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debugger/stop")
async def debugger_stop(request: Request):
    """Debugger session durdur."""
    try:
        data = await request.json()
        session_id = data.get("session_id")
        
        result = real_debugger.stop()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/intellisense/complete")
async def intellisense_complete(request: Request):
    """AI-powered code completion."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        line = data.get("line", 0)
        column = data.get("column", 0)
        
        # Basit AI completion - Ollama kullanarak
        # Not: Gerçek implementasyon için daha karmaşık prompt gerekli
        prompt = f"""Complete the following Python code at line {line}, column {column}:

```python
{code}
```

Provide only the completion, no explanation."""
        
        try:
            ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
            response = ollama_client.chat(prompt)
            completion = response["content"]
            
            return JSONResponse({
                "success": True,
                "completions": [
                    {
                        "label": completion.strip(),
                        "type": "ai",
                        "detail": "AI-powered suggestion"
                    }
                ]
            })
        except Exception as e:
            # Fallback to static completion
            result = auto_completer.complete(file_path, line, column, "")
            return JSONResponse({
                "success": True,
                "completions": [
                    {
                        "label": item.label,
                        "type": item.type.value,
                        "detail": item.detail
                    }
                    for item in result.items[:5]
                ]
            })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/intellisense/explain")
async def intellisense_explain(request: Request):
    """AI-powered code explanation."""
    try:
        data = await request.json()
        code = data.get("code", "")
        
        prompt = f"""Explain the following Python code:

```python
{code}
```

Provide a clear, concise explanation."""
        
        ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
        response = ollama_client.chat(prompt)
        explanation = response["content"]
        
        return JSONResponse({
            "success": True,
            "explanation": explanation
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/intellisense/suggest")
async def intellisense_suggest(request: Request):
    """AI-powered code suggestions."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        
        prompt = f"""Suggest improvements for the following Python code:

```python
{code}
```

Provide specific suggestions for improvement."""
        
        ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
        suggestions = ollama_client.generate(prompt, max_tokens=300)
        
        return JSONResponse({
            "success": True,
            "suggestions": suggestions
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/completion")
async def lsp_completion(request: Request):
    """LSP completion request (mock implementation)."""
    try:
        data = await request.json()
        
        # Simple mock completions
        completions = [
            {"label": "print", "kind": 3, "detail": "Built-in function"},
            {"label": "def", "kind": 14, "detail": "Keyword"},
            {"label": "class", "kind": 5, "detail": "Keyword"},
            {"label": "import", "kind": 14, "detail": "Keyword"},
            {"label": "if", "kind": 14, "detail": "Keyword"},
            {"label": "return", "kind": 14, "detail": "Keyword"},
            {"label": "for", "kind": 14, "detail": "Keyword"},
            {"label": "while", "kind": 14, "detail": "Keyword"},
        ]
        
        return JSONResponse({
            "success": True,
            "completions": completions
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/hover")
async def lsp_hover(request: Request):
    """LSP hover request."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        line = data.get("line", 0)
        column = data.get("column", 0)
        
        # Mock hover information
        return JSONResponse({
            "success": True,
            "hover": {
                "contents": "Hover information (mock)",
                "range": {"start": {"line": line, "character": column}, "end": {"line": line, "character": column + 1}}
            }
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/definition")
async def lsp_definition(request: Request):
    """LSP go-to-definition request."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        line = data.get("line", 0)
        column = data.get("column", 0)
        
        # Mock definition
        return JSONResponse({
            "success": True,
            "definition": {
                "uri": file_path,
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 10}}
            }
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/diagnostics")
async def lsp_diagnostics(request: Request):
    """LSP diagnostics request."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        
        # Mock diagnostics
        return JSONResponse({
            "success": True,
            "diagnostics": []
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/intellisense/context-complete")
async def context_aware_completion(request: Request):
    """Context-aware AI completion."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        line = data.get("line", 0)
        column = data.get("column", 0)
        context = data.get("context", "")
        
        # Advanced AI completion with context
        prompt = f"""You are an expert Python code completion AI. Complete the code at line {line}, column {column} with the best possible completion.

Context:
{context}

Code:
```python
{code}
```

Provide the completion only, no explanation. Keep it concise and accurate."""
        
        try:
            ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
            response = ollama_client.chat(prompt)
            completion = response["content"]
            
            # Parse completion to extract the actual code
            completion_text = completion.strip()
            
            return JSONResponse({
                "success": True,
                "completions": [
                    {
                        "label": completion_text,
                        "type": "ai-context",
                        "detail": "AI-powered context-aware suggestion"
                    }
                ]
            })
        except Exception as e:
            # Fallback to static completion
            result = auto_completer.complete(file_path, line, column, "")
            return JSONResponse({
                "success": True,
                "completions": [
                    {
                        "label": item.label,
                        "type": item.type.value,
                        "detail": item.detail
                    }
                    for item in result.items[:5]
                ]
            })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/intellisense/ai-suggestions")
async def ai_suggestions(request: Request):
    """Advanced AI code suggestions."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        code = data.get("code", "")
        selection = data.get("selection", "")
        
        prompt = f"""You are an expert Python code reviewer. Analyze the following code and provide specific, actionable suggestions for improvement:

```python
{code}
```

Selected code:
```python
{selection}
```

Provide suggestions in the following format:
1. [Category] Description
2. [Category] Description

Categories: Performance, Readability, Security, Best Practices"""
        
        ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
        response = ollama_client.chat(prompt)
        suggestions = response["content"]
        
        return JSONResponse({
            "success": True,
            "suggestions": suggestions
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/debugger/state")
async def debugger_state():
    """Debugger durumunu al."""
    try:
        return JSONResponse({
            "success": True,
            "state": real_debugger.state.value,
            "current_frame": {
                "file": real_debugger.current_frame.file if real_debugger.current_frame else None,
                "line": real_debugger.current_frame.line if real_debugger.current_frame else None,
                "function": real_debugger.current_frame.function if real_debugger.current_frame else None
            } if real_debugger.current_frame else None,
            "breakpoints": [
                {"file": bp.file, "line": bp.line, "enabled": bp.enabled}
                for bp in real_debugger.breakpoints
            ]
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/plugins/{plugin_id}/status")
async def get_plugin_status(plugin_id: str):
    """Plugin durumunu al."""
    try:
        status = plugin_engine.get_plugin_status(plugin_id)
        
        return JSONResponse({
            "success": True,
            "status": status
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/lsp/diagnostics")
async def lsp_diagnostics(request: Request):
    """LSP diagnostics request (mock)."""
    try:
        return JSONResponse({
            "success": True,
            "diagnostics": []
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/git/status")
async def git_status():
    """Git durumunu al (gerçek Git)."""
    try:
        result = real_git.status()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/add")
async def git_add(request: Request):
    """Dosyaları stage'e ekle."""
    try:
        data = await request.json()
        files = data.get("files")
        result = real_git.add(files)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/commit")
async def git_commit(request: Request):
    """Commit yap (gerçek Git)."""
    try:
        data = await request.json()
        message = data.get("message", "")
        result = real_git.commit(message)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/push")
async def git_push(request: Request):
    """Push yap (gerçek Git)."""
    try:
        data = await request.json()
        remote = data.get("remote", "origin")
        branch = data.get("branch")
        result = real_git.push(remote, branch)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/pull")
async def git_pull(request: Request):
    """Pull yap (gerçek Git)."""
    try:
        data = await request.json()
        remote = data.get("remote", "origin")
        branch = data.get("branch")
        result = real_git.pull(remote, branch)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/git/log")
async def git_log(limit: int = 10):
    """Commit log'u al (gerçek Git)."""
    try:
        result = real_git.log(limit)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/git/branches")
async def git_branches():
    """Branch listesini al (gerçek Git)."""
    try:
        result = real_git.branches()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/branch/create")
async def git_create_branch(request: Request):
    """Yeni branch oluştur (gerçek Git)."""
    try:
        data = await request.json()
        name = data.get("name")
        checkout = data.get("checkout", True)
        result = real_git.create_branch(name, checkout)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/branch/switch")
async def git_switch_branch(request: Request):
    """Branch'e geçiş yap (gerçek Git)."""
    try:
        data = await request.json()
        name = data.get("name")
        result = real_git.switch_branch(name)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/branch/delete")
async def git_delete_branch(request: Request):
    """Branch sil (gerçek Git)."""
    try:
        data = await request.json()
        name = data.get("name")
        force = data.get("force", False)
        result = real_git.delete_branch(name, force)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/diff")
async def git_diff(request: Request):
    """Diff al (gerçek Git)."""
    try:
        data = await request.json()
        file = data.get("file")
        result = real_git.diff(file)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debug/start")
async def debug_start(request: Request):
    """Debug session başlat."""
    try:
        data = await request.json()
        uri = data.get("uri")
        
        if not uri:
            return JSONResponse({"success": False, "error": "uri required"})
        
        session = debugging_engine.start_session(uri)
        
        return JSONResponse({
            "success": True,
            "session_id": session.session_id,
            "uri": uri,
            "status": "started"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/debug/breakpoint")
async def debug_breakpoint(request: Request):
    """Debug breakpoint."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        
        if not file_path:
            return JSONResponse({"success": False, "error": "file_path required"})
        
        from app.editor.debug_breakpoint import DebugBreakpointEngine
        debug_breakpoint_engine = DebugBreakpointEngine()
        result = debug_breakpoint_engine.set_breakpoint(file_path)
        
        return JSONResponse({
            "success": result.success,
            "breakpoint_id": result.breakpoint_id,
            "file_path": result.file_path,
            "line": result.line,
            "message": result.message,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/stage")
async def git_stage(request: Request):
    """Git stage (gerçek Git)."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        files = [file_path] if file_path else None
        result = real_git.add(files)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.post("/api/editor/git/unstage")
async def git_unstage(request: Request):
    """Git unstage (gerçek Git)."""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        # Git reset HEAD <file>
        result = subprocess.run(
            ["git", "reset", "HEAD", file_path],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False
        )
        return JSONResponse({
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.websocket("/ws/collaboration/{session_id}")
async def websocket_collaboration(websocket: WebSocket, session_id: str):
    """Real-time collaboration WebSocket."""
    await websocket.accept()
    
    # Session'a kullanıcıyı ekle
    if session_id not in active_sessions:
        active_sessions[session_id] = {"users": [], "cursors": {}, "edits": []}
    
    active_sessions[session_id]["users"].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Broadcast to other users in session
            for user in active_sessions[session_id]["users"]:
                if user != websocket:
                    await user.send_json(data)
                    
    except WebSocketDisconnect:
        active_sessions[session_id]["users"].remove(websocket)
        if not active_sessions[session_id]["users"]:
            del active_sessions[session_id]


@app.post("/api/editor/git/stash")
async def git_stash(request: Request):
    """Git stash."""
    try:
        data = await request.json()
        message = data.get("message", "WIP")
        
        from app.editor.git_stash import GitStashEngine
        git_stash_engine = GitStashEngine(str(PROJECT_ROOT))
        result = git_stash_engine.create_stash(message)
        
        return JSONResponse({
            "success": result.success,
            "stash_id": result.stash_id,
            "message": result.message,
            "stashed_files": result.stashed_files,
            "total_files": result.total_files,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


@app.get("/api/editor/git/stash/list")
async def git_stash_list():
    """Git stash list."""
    try:
        from app.editor.git_stash import GitStashEngine
        git_stash_engine = GitStashEngine(str(PROJECT_ROOT))
        result = git_stash_engine.list_stashes()
        
        return JSONResponse({
            "success": result.success,
            "stash_entries": [
                {
                    "id": s.id,
                    "message": s.message,
                    "branch": s.branch,
                    "author": s.author,
                    "date": s.date.isoformat() if s.date else None
                }
                for s in result.stash_entries
            ],
            "total_stashes": result.total_stashes,
            "errors": result.errors
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
