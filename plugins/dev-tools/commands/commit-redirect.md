# Command: /commit (迁移提示)

## ⚠️ 重要提示

commit 功能已迁移到独立的 **git-tools** 插件，以提供更好的功能和性能。

## 🚀 快速迁移

### 安装 git-tools 插件

```bash
# 方法1：手动安装（推荐）
cp -r plugins/git-plugins ~/.config/claude/plugins/

# 方法2：使用包管理器
claude plugin install git-tools
```

### 迁移优势

- ✅ **更好的模块化**：独立插件，更新更灵活
- ✅ **增强的功能**：更多Git工具和工作流支持
- ✅ **插件集成**：与code-review和unit-test-generator插件深度集成
- ✅ **持续更新**：独立维护，快速响应需求

## 📋 功能对比

| 功能 | dev-tools (旧) | git-tools (新) |
|------|----------------|----------------|
| 智能提交 | ✅ | ✅ (增强) |
| 分支管理 | ⚠️ 基础 | ✅ 完整 |
| 插件集成 | ❌ | ✅ 完整支持 |
| 配置选项 | ⚠️ 有限 | ✅ 丰富 |
| 错误处理 | ⚠️ 基础 | ✅ 完善 |

## 🔧 使用方法

安装 git-tools 后，使用方法完全相同：

```bash
# 所有原有的参数都支持
/commit
/commit --auto
/commit --type feat --scope auth
/commit --check
/commit --push
/commit --create-branch
```

## ⏳ 过渡期

当前版本保留此重定向作为兼容层，**将在 dev-tools 2.0.0 中移除**。

建议尽快迁移到 git-tools 以获得更好的体验。

## 🆘 需要帮助？

- 查看 [git-tools 文档](../git-tools/README.md)
- 使用 `@GitExpert` 获取帮助
- 提交 Issue 反馈问题

---

*让 Git 操作更简单、更强大！* 🚀