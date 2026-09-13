# A800 Local Setup

本仓库故意不保存真实 A800 地址、用户名、密码或私钥。

## 1. 本地 SSH alias

在你自己的 `~/.ssh/config` 配置，例如：

```sshconfig
Host a800-lab
    HostName <SERVER_ADDRESS>
    User <USERNAME>
    Port <PORT>
```

如实验室仍只允许密码登录，密码只在 SSH 交互提示中输入；不要放进仓库脚本、命令行参数或 `.env`。

## 2. 本地配置

```bash
mkdir -p config/local
cp config/a800.env.example config/local/a800.env
```

`config/local/` 已被 `.gitignore` 忽略。

## 3. 状态检查

```bash
set -a
source config/local/a800.env
set +a

bash tools/a800_status.sh
```

检查至少包括：

- GPU 型号 / 显存 / 利用率；
- GPU 计算进程；
- 进程所属用户；
- CPU / RAM / load；
- `~/whr` 或授权目录磁盘空间；
- Slurm 是否存在；
- Python / Conda 环境。

## 4. 环境

平台优先使用独立的 `auto_research` Python 3.12 环境，不修改服务器已有业务环境。

## 5. 无调度器场景

`tools/a800_wait_candidate.sh` 只等待出现候选卡并退出。它不会自动启动训练。真正占用前需要确认该卡没有被其他成员预留。
