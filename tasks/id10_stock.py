"""监控 id10.cn 商品库存，每个商品有货↔没货切换时推送。"""
import re
from datetime import datetime, timedelta, timezone

from tracker import notify, state
from tracker.http import get_text

NAME = "id10_stock"
PRODUCT_IDS = [82, 84]


def fetch(url: str) -> tuple[str, int]:
    html = get_text(url)
    title = re.search(r'<h1 class="h3 mb-3">\s*(.*?)\s*</h1>', html, re.S)
    stock = re.search(r"库存：\s*(\d+)", html)
    if not stock:
        raise RuntimeError(f"{url} 没找到库存信息，页面结构可能变了")
    return (title.group(1) if title else url), int(stock.group(1))


def main() -> None:
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    saved = state.load(NAME) or {}
    errors = []
    for pid in PRODUCT_IDS:
        url = f"https://id10.cn/buy/{pid}"
        try:
            product, stock = fetch(url)
        except Exception as exc:
            errors.append(f"{pid}: {exc}")
            continue
        in_stock = stock > 0
        prev = saved.get(str(pid))
        print(f"{now} [{pid}] {product} 库存={stock}")

        if prev is None or prev["in_stock"] != in_stock:
            status = f"有货（库存 {stock}）" if in_stock else "没货了"
            notify.send(f"[{status}] {product}", f"时间：{now}", url=url)
        if prev is None or prev["in_stock"] != in_stock or prev["stock"] != stock:
            saved[str(pid)] = {"in_stock": in_stock, "stock": stock, "updated_at": now}
    state.save(NAME, saved)
    if errors:
        raise RuntimeError("; ".join(errors))


if __name__ == "__main__":
    main()
