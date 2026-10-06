"""每个任务的上次结果存在 state/<name>.json，由工作流在变化时提交回仓库。"""
import json
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"


def load(name: str) -> dict | None:
    path = STATE_DIR / f"{name}.json"
    return json.loads(path.read_text()) if path.exists() else None


def save(name: str, data: dict) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    (STATE_DIR / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
