"""微信推送：配置了哪个渠道的环境变量就发哪个，可同时配置多个。

PUSHPLUS_TOKEN       PushPlus token
SERVERCHAN_SENDKEY   Server酱 SendKey（兼容 Turbo 版和 Server酱³ 的 sctp 开头 key）
"""
import json
import os
import re
import urllib.parse

from tracker.http import post


def _pushplus(token: str, title: str, content: str) -> None:
    body = json.dumps({"token": token, "title": title, "content": content, "template": "txt"}).encode()
    resp = json.loads(post("https://www.pushplus.plus/send", body, "application/json"))
    if resp.get("code") != 200:
        raise RuntimeError(f"PushPlus 推送失败: {resp}")


def _serverchan(key: str, title: str, content: str) -> None:
    m = re.match(r"sctp(\d+)t", key)
    url = f"https://{m.group(1)}.push.ft07.com/send/{key}.send" if m else f"https://sctapi.ftqq.com/{key}.send"
    body = urllib.parse.urlencode({"title": title, "desp": content}).encode()
    resp = json.loads(post(url, body, "application/x-www-form-urlencoded"))
    if resp.get("code") != 0:
        raise RuntimeError(f"Server酱推送失败: {resp}")


def send(title: str, content: str) -> None:
    channels = [
        (os.environ.get("PUSHPLUS_TOKEN"), _pushplus),
        (os.environ.get("SERVERCHAN_SENDKEY"), _serverchan),
    ]
    configured = [(key, fn) for key, fn in channels if key]
    if not configured:
        raise RuntimeError("未配置推送渠道：请设置 PUSHPLUS_TOKEN 或 SERVERCHAN_SENDKEY")
    for key, fn in configured:
        fn(key, title, content)
