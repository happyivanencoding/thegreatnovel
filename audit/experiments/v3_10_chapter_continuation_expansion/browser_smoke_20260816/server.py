import sys
from pathlib import Path

sys.path.insert(0, r"C:\dev\小说续写系统\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\dev\小说续写系统\src")

from novel_authoring.db.database import Database
from novel_authoring.web.app import serve


ROOT = Path(__file__).resolve().parent
serve(
    Database(ROOT / ".auto-workbench.sqlite3"),
    host="127.0.0.1",
    port=8065,
    library_root=ROOT / "library",
    discovery_root=ROOT / "book",
)
