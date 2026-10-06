# Tracker

公开仓库 `suiyuee/Tracker`：GitHub Actions 定时运行的监控任务集合，通过 Bark 推送。

## 安全边界（公开仓库，任何人可见代码、提交历史和 Actions 日志）

- 密钥、密码、token、cookie、账号、私人邮箱/手机号等凭据只放在仓库 Secrets，经工作流 `env` 注入、代码用 `os.environ` 读取；不写入代码、配置、`state/`、提交信息或 README，示例一律用占位符。
- 不输出凭据：不打印环境变量、请求头、带凭据的 URL 或完整请求/响应；异常消息不带凭据，必要时吞掉原始异常另抛通用错误（参照 `tracker/notify.py`）。
- 工作流只用 `schedule` 和 `workflow_dispatch` 触发，不用 `pull_request` / `pull_request_target`；Secrets 只注入到需要它的步骤。
- `state/` 只存判断变化所需的最少公开信息。
- 不适合公开的监控对象（内部地址、需要登录的私人页面等）不放进本仓库。
- 一旦凭据进过提交（即使随后删除）就视为泄露：先到对应平台作废并更换，再处理历史。

## 约定

- 新任务：`tasks/<name>.py` 提供 `main()`，在 `tasks.toml` 加开关；公共能力放 `tracker/`。
- 只用 Python 标准库，运行环境为 GitHub `ubuntu-latest` 自带的 `python3`。
