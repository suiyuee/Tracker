# Tracker

在本地电脑上定时运行的监控任务集合，变化时通过 Bark 推送。

## 结构

- `tasks/`：每个任务一个模块，提供 `main()`
- `tasks.toml`：任务开关，`true` 启用、`false` 停用
- `tracker/`：公共能力（HTTP、Bark 推送、状态存储、任务调度）
- `state/`：各任务上次的结果，只存在本地（已在 `.gitignore` 中忽略）

运行一次所有启用的任务（需要 Python 3.11+）：`BARK_KEY=<你的 key> python3 -m tracker.run`。定时运行由本机负责（如 macOS 的 `launchd` 或 `crontab`）。

## 配置

运行时通过环境变量 `BARK_KEY` 提供 Bark key，不要写进仓库。凭据规则见 [AGENTS.md](AGENTS.md)。

## 任务

| 任务 | 说明 |
| --- | --- |
| `id10_stock` | 监控 id10.cn 商品（82、84）库存，有货/没货切换时推送 |
