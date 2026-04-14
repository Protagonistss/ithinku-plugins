<h1 align="center">✨ Code Review Plugin</h1>

<p align="center">
  <strong>专业的代码审查插件，提供全面的代码质量分析、安全检查和性能优化建议</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 🚀 核心特性

### 🔍 代码质量审查
- **结构分析**：深入剖析代码架构，识别不合理的模块划分。
- **复杂度评估**：量化圈复杂度，精准定位难以维护的“代码泥潭”。
- **最佳实践**：基于行业标准与社区共识（如 Clean Code）进行一致性检查。
- **可维护性**：评估代码的可读性、可测试性及未来的重构成本。

### 🔒 安全深度审计
- **漏洞检测**：覆盖 OWASP Top 10，识别 SQL 注入、XSS、CSRF 等高危漏洞。
- **认证授权**：审查权限校验逻辑，严防越权漏洞。
- **数据安全**：识别明文存储、不安全加密及敏感信息泄露风险。

### ⚡ 性能极限分析
- **算法评估**：识别 O(n²) 等低效算法，提供更优的时间复杂度建议。
- **资源监控**：发现不必要的内存分配、未关闭的连接及 CPU 密集型瓶颈。
- **并发审查**：定位竞态条件（Race Condition）与死锁隐患。

## 🤖 智能代理 (Agents)

- **`@code-reviewer`**：全方位代码审查专家，平衡质量与工程进度。
- **`@security-expert`**：专注攻防对抗的专业安全审计师。

## 🛠️ 快速安装

### macOS / Linux
```bash
# 创建符号链接（推荐开发模式）
ln -s $(pwd)/plugins/code-review ~/.config/claude/plugins/code-review
```

### Windows (PowerShell)
```powershell
# 复制插件目录
New-Item -ItemType SymbolHardLink -Path "$env:APPDATA\Claude\plugins\code-review" -Target ".\plugins\code-review"
```

## 📖 使用指南

在 Claude Code 终端中，你可以直接运行以下命令：

| 命令 | 描述 | 示例 |
|------|------|------|
| `/review` | 执行全方位质量审查 | `/review src/main.ts` |
| `/security` | 启动深度安全审计 | `/security internal/auth/` |
| `/performance` | 进行性能瓶颈分析 | `/performance api/v1/` |
