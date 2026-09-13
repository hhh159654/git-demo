# Security Rules

必须禁止提交：

- `sshconfig.md`
- 真实服务器 Host/IP、用户名、密码
- SSH 私钥
- API key / GitHub token
- `.env`
- `config/local/`
- `reference_papers_origin/` 中的原始 PDF
- 私有数据、受限数据集、模型权重

提交前执行：

```bash
autoresearch check-secrets .
git status
git diff --cached
```

如果任何真实凭据曾经进入 Git 历史，不要只删除文件；应同时轮换凭据，并按 Git 历史清理流程处理。
