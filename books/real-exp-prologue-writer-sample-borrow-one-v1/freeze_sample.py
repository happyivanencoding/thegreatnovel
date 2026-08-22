from pathlib import Path


root = Path(__file__).resolve().parent
response = (root / "response.md").read_text(encoding="utf-8").strip()
(root / "PROLOGUE.md").write_text(response + "\n", encoding="utf-8")
