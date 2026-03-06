---
name: security
description: 专门进行代码安全审查，识别潜在的安全漏洞和风险。
skills:
  - security-review
---

# Command: /security

专门进行代码安全审查，识别潜在的安全漏洞和风险。

## 描述

/security 命令使用专业的安全审查代理，深度分析代码中的安全问题，包括SQL注入、XSS、CSRF、认证授权等常见安全漏洞。

## 用法

```
/security [target] [options]
```

### 参数

- `target` - 审查目标（文件路径、目录或代码片段）
- `--owasp` - 按OWASP Top 10标准进行审查
- `--scan-type` - 扫描类型（quick, comprehensive, deep）
- `--compliance` - 合规标准（gdpr, pci, hipaa）

## 安全检查清单

### 注入攻击
- [ ] SQL注入
- [ ] NoSQL注入
- [ ] 命令注入
- [ ] LDAP注入

### 身份认证与授权
- [ ] 弱密码策略
- [ ] 会话管理
- [ ] 权限控制
- [ ] JWT安全

### 数据安全
- [ ] 敏感数据泄露
- [ ] 加密实现
- [ ] 数据传输安全
- [ ] 日志安全

### 输入验证
- [ ] XSS防护
- [ ] CSRF防护
- [ ] 文件上传安全
- [ ] 输入sanitization

## 示例

```
/security --owasp src/api/
/security --compliance gdpr user-service.js
/security `
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = db.query(`SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`);
  res.json(user);
});
`
```

## 安全报告格式

```markdown
# 安全审查报告

## 风险概览
- **严重风险**: 2个
- **高风险**: 5个
- **中风险**: 8个
- **低风险**: 12个

## 🔴 严重风险 (立即修复)

### 1. SQL注入漏洞
**CWE**: CWE-89
**OWASP**: A03:2021 – Injection
**位置**: auth.js:45
**影响**: 可能导致数据库完全泄露

## 📋 合规性检查
- **GDPR**: ❌ 未发现个人数据加密
- **PCI DSS**: ❌ 信用卡信息未加密存储
```