"""Bark 推送，key 取自环境变量 BARK_KEY。"""
import json
import os
import urllib.parse

from tracker.http import post

GROUP = "Tracker"


def send(title: str, body: str, url: str | None = None) -> None:
    key = os.environ.get("BARK_KEY", "").strip()
    if not key:
        raise RuntimeError("未配置 BARK_KEY")
    payload = {"title": title, "body": body, "group": GROUP}
    if url:
        payload["url"] = url
    try:
        resp = json.loads(post(f"https://api.day.app/{urllib.parse.quote(key)}", json.dumps(payload).encode(), "application/json; charset=utf-8"))
    except Exception:
        # 异常信息里可能带含 key 的 URL，不往外抛原文
        raise RuntimeError("Bark 请求失败") from None
    if resp.get("code") != 200:
        raise RuntimeError(f"Bark 未确认送达: code={resp.get('code')}")
