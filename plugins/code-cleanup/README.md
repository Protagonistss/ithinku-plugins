# Code Cleanup Plugin

面向 Vue2 + webpack 项目的安全清理插件，用于识别未引用页面、未使用组件和历史死代码，并生成“可执行但默认不自动删除”的候选报告。

## 核心能力

- 未引用页面识别（`src/page/**`）
- 未使用组件识别（`src/components/**`）
- 历史备份/死代码识别（`*-copy.*`, `*-bf.*`, `*-old.*` 等）
- 风险分级输出（`high` / `medium` / `low`）
- 生成清理报告与回滚友好的补丁计划

## 目录结构

```text
plugins/code-cleanup/
├─ README.md
└─ skills/
   └─ code-cleanup-skill/
      ├─ SKILL.md
      ├─ config/
      │  └─ keep-list.txt
      ├─ evals/
      │  └─ evals.json
      └─ scripts/
         ├─ analyze_cleanup_candidates.py
         └─ render_cleanup_report.py
```

## 发布与分发

### 1) Claude 仓库插件发布（推荐）

直接分发本仓库中的 `plugins/code-cleanup` 目录，团队成员在仓库内引用：

```bash
python plugins/code-cleanup/skills/code-cleanup-skill/scripts/analyze_cleanup_candidates.py \
  --project-root . \
  --keep-list plugins/code-cleanup/skills/code-cleanup-skill/config/keep-list.txt \
  --output .skill-workspace/code-cleanup/latest/deletion-candidates.json
```

## 附录：Cursor 本地 Skill 兼容用法（可选）

以下仅用于已有 Cursor 本地 Skill 习惯的个人环境，不是 Claude 插件发布必需步骤。

将 `plugins/code-cleanup/skills/code-cleanup-skill` 同步到本地：

- Windows: `%USERPROFILE%\.cursor\skills\code-cleanup-skill`
- macOS/Linux: `~/.cursor/skills/code-cleanup-skill`

然后在项目根目录执行：

```bash
python .cursor/skills/code-cleanup-skill/scripts/analyze_cleanup_candidates.py \
  --project-root . \
  --keep-list .cursor/skills/code-cleanup-skill/config/keep-list.txt \
  --output .cursor/skills/code-cleanup-skill-workspace/latest/deletion-candidates.json
```

## 标准执行流程

```bash
python plugins/code-cleanup/skills/code-cleanup-skill/scripts/analyze_cleanup_candidates.py \
  --project-root . \
  --output .skill-workspace/code-cleanup/latest/deletion-candidates.json

python plugins/code-cleanup/skills/code-cleanup-skill/scripts/render_cleanup_report.py \
  --input .skill-workspace/code-cleanup/latest/deletion-candidates.json \
  --output-dir .skill-workspace/code-cleanup/latest
```

产物：

- `cleanup-report.md`
- `deletion-candidates.json`
- `patch-plan.md`

## 安全边界

- 默认只生成候选，不直接删除
- 动态加载、运行时注册、字符串路径命中时，降级为 `medium`
- 建议按小批次清理并执行最小回归测试
