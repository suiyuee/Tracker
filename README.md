# Tracker

基于 GitHub Actions 的定时任务集合，结果通过微信推送。

## 结构

- `tasks/`：每个任务一个模块，用 `python3 -m tasks.<name>` 运行
- `tracker/`：公共能力（HTTP、微信推送、状态存储）
- `state/`：各任务上次的结果，工作流在变化时自动提交
- `.github/workflows/`：每个任务一个工作流，各自设定频率

## 推送配置

在仓库 Secrets 里设置任意一个或多个：

- `PUSHPLUS_TOKEN`：PushPlus token
- `SERVERCHAN_SENDKEY`：Server酱 SendKey

## 任务

| 任务 | 说明 | 频率 |
| --- | --- | --- |
| `id10_stock` | 监控 https://id10.cn/buy/82 库存，有货/没货切换时推送 | 每 30 分钟 |

私有仓库每月免费 2000 分钟 Actions，每次运行按 1 分钟计，加任务或提高频率前注意总量。
