# Tracker

基于 GitHub Actions 的定时监控任务集合，变化时通过 Bark 推送。

## 结构

- `tasks/`：每个任务一个模块，提供 `main()`
- `tasks.toml`：任务开关，`true` 启用、`false` 停用
- `tracker/`：公共能力（HTTP、Bark 推送、状态存储、任务调度）
- `state/`：各任务上次的结果，工作流在变化时自动提交

工作流 `Tracker` 每 5 分钟运行一次所有启用的任务（GitHub 定时任务可能延迟）；本地运行：`python3 -m tracker.run`。

## 配置

仓库 Secrets 设置 `BARK_KEY`。凭据规则见 [AGENTS.md](AGENTS.md)。

## 任务

| 任务 | 说明 |
| --- | --- |
| `id10_stock` | 监控 https://id10.cn/buy/82 库存，有货/没货切换时推送 |
