"""按 tasks.toml 依次运行启用的任务；单个任务失败不影响其他任务，最后整体以失败退出。"""
import importlib
import sys
import tomllib
import traceback
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "tasks.toml"


def main() -> int:
    enabled = [name for name, on in tomllib.loads(CONFIG.read_text()).items() if on]
    failed = []
    for name in enabled:
        print(f"== {name}")
        try:
            importlib.import_module(f"tasks.{name}").main()
        except Exception as exc:
            # 只输出异常类型和消息，不输出调用栈里的局部变量
            print("".join(traceback.format_exception_only(exc)).strip())
            failed.append(name)
    if failed:
        print(f"失败任务: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
