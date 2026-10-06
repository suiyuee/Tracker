"""监控 id10.cn 商品库存，有货↔没货切换时推送微信。"""
import re
from datetime import datetime, timedelta, timezone

from tracker import notify, state
from tracker.http import get_text

NAME = "id10_stock"
URL = "https://id10.cn/buy/82"


def fetch() -> tuple[str, int]:
    html = get_text(URL)
    title = re.search(r'<h1 class="h3 mb-3">\s*(.*?)\s*</h1>', html, re.S)
    stock = re.search(r"库存：\s*(\d+)", html)
    if not stock:
        raise RuntimeError("页面里没找到库存信息，页面结构可能变了")
    return (title.group(1) if title else URL), int(stock.group(1))


def main() -> None:
    product, stock = fetch()
    in_stock = stock > 0
    prev = state.load(NAME)
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    print(f"{now} {product} 库存={stock}")

    if prev is None or prev["in_stock"] != in_stock:
        status = f"有货（库存 {stock}）" if in_stock else "没货了"
        notify.send(f"[{status}] {product}", f"时间：{now}", url=URL)
    if prev is None or prev["in_stock"] != in_stock or prev["stock"] != stock:
        state.save(NAME, {"in_stock": in_stock, "stock": stock, "updated_at": now})


if __name__ == "__main__":
    main()
