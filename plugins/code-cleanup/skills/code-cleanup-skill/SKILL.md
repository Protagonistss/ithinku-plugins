---
name: code-cleanup-skill
description: 清理项目中的未引用模块、未使用组件与死代码。支持 JS/TS、Python、Go、Java、PHP、Ruby、Rust、C/C++ 等多语言项目。只要用户提到"代码清理""未引用""未使用组件""死代码""瘦身项目""删除无用文件""清理历史备份文件（copy/bf/old）"，都应优先使用本 Skill。即使用户没有明确说"Skill"，但目标是识别或清理无用代码，也应触发。
---

# Code Cleanup Skill

用于在任何项目中执行"安全优先"的清理分析，输出可执行的候选变更而不是直接删除文件。

## 适用场景

- 用户希望清理未引用的页面、组件、模块
- 用户希望识别死代码、历史备份文件、重复实现
- 用户需要"可落地"的清理报告与补丁方案

## 支持语言

引用检测覆盖以下语言的 import 语法：

| 语言 | 扩展名 | 检测的 import 模式 |
|------|--------|-------------------|
| JS/TS | .js .ts .jsx .tsx .vue | import/require/dynamic import |
| Python | .py | import/from...import |
| Go | .go | import |
| Java | .java | import |
| PHP | .php | require/include/use |
| Ruby | .rb | require/require_relative/load |
| Rust | .rs | use/mod |
| C/C++ | .c .cpp .h .hpp | #include |

## 默认行为

1. 默认进入 `patch-candidates` 模式：生成候选，不直接删除
2. 所有候选必须带"证据"与"风险等级"
3. 输出必须包含回滚建议

## 配置驱动

所有扫描行为通过配置文件控制（位于 `config/` 目录）：

| 配置文件 | 用途 |
|---------|------|
| `scan-dirs.txt` | 扫描哪些目录、类别名、关键词策略 |
| `ext-list.txt` | 哪些扩展名参与扫描 |
| `keep-list.txt` | 白名单，始终保留的文件 |

配置文件不存在时使用内置默认值，用户无需创建即可使用。

## 输入约定

如用户未给参数，使用默认值：

```yaml
target_dirs:
  - <auto-detect from current workspace>
mode: patch-candidates
safety:
  allow_direct_delete: false
  require_confirmation: true
```

说明：若不传 `--targets`，脚本会按当前工作空间自动扫描（`--project-root` 对应目录），并自动执行模块/死代码分析。

## 工作流 (Three-Phase Loop)

必须遵循以下严格的三阶段闭环，确保清理过程可视化、可评审、可回滚。

### Phase 1: 扫描 (Scan)
1. **自动识别入口**：扫描路由、模块入口及各语言 import 语法。
2. **生成候选**：调用 `analyze_cleanup_candidates.py`。
   - 默认扫描当前工作空间。
   - 产出 `deletion-candidates.json`。
3. **简要汇报**：Agent 需提取 JSON 中的 `summary` 向用户简要汇报高/中/低风险的数量。

### Phase 2: 评审 (Review)
1. **生成可视化报告**：调用 `render_cleanup_report.py`。
   - 产出 `cleanup-report.html` (交互式 HTML)、`cleanup-report.md` 和 `patch-plan.md`。
2. **引导用户查看**：
   - **必须**提供 `cleanup-report.html` 的本地绝对路径。
   - **必须**提示用户：“已生成交互式报告，请在浏览器中打开以进行可视化确认。你可以点击路径旁边的图标快速复制代码路径。”
3. **人工确认**：等待用户阅读报告并给出清理指令（例如：“清理所有高风险项”或“删除特定列表”）。

### Phase 3: 执行 (Execute)
1. **自动化清理**：
   - 根据用户指令，读取 `deletion-candidates.json` 获取对应的文件路径。
   - 使用 `rm` 或 `git rm` 执行物理删除。
   - **禁止** Agent 凭直觉猜测路径，必须以 JSON 记录为准。
2. **后续验证**：
   - 删除后提示用户运行项目测试或进行人工回归。
   - 提供回滚建议（如 `git reset --hard` 或 `git checkout -- <file>`）。

## 生成结果规范 (Outputs)

必须输出以下四个文件到工作区（默认路径 `.skill-workspace/code-cleanup/latest/`）：

1. `cleanup-report.html` (核心)
   - 包含高置信度风险统计卡片。
   - 支持按风险等级折叠/展开的交互式表格。
   - 支持一键复制路径。
2. `cleanup-report.md`
   - 供 AI Agent 快速检索和在终端展示的摘要。
3. `deletion-candidates.json`
   - 供 AI Agent 执行 Phase 3 时读取的机器可读数据。
4. `patch-plan.md`
   - 包含回滚命令、依赖影响分析及手动操作建议。

## 输出格式规范

`deletion-candidates.json` 结构：

```json
{
  "generated_at": "ISO_DATE",
  "project_root": "ABS_PATH",
  "summary": {
    "high": 0,
    "medium": 0,
    "low": 0
  },
  "candidates": [
    {
      "path": "src/page/example/example.js",
      "category": "unused_page",
      "risk_level": "high",
      "evidence": [
        "未在其他源码文件中找到对 `example` 的直接引用"
      ],
      "suggested_action": "delete_after_confirm"
    }
  ]
}
```

## 执行边界

- 不直接执行删除操作，除非用户明确要求
- 不对不确定项给出"高风险可删"
- 遇到动态加载、后端下发路径、插件注册场景要降级为 `medium`

## 推荐实现

优先使用同目录脚本：

- `scripts/analyze_cleanup_candidates.py`
  - 生成候选 JSON
  - 支持 `--keep-list` 白名单（默认读取 `config/keep-list.txt`）
  - 支持 `--ext-list` 扩展名配置（默认读取 `config/ext-list.txt`）
  - 支持 `--scan-dirs` 目录配置（默认读取 `config/scan-dirs.txt`）
- `scripts/render_cleanup_report.py`
  - 生成 `cleanup-report.md` 与 `patch-plan.md`

## 实操命令模板

### A. 作为 Claude 仓库插件使用（推荐发布形态）

```bash
python plugins/code-cleanup/skills/code-cleanup-skill/scripts/analyze_cleanup_candidates.py \
  --project-root . \
  --keep-list plugins/code-cleanup/skills/code-cleanup-skill/config/keep-list.txt \
  --output .skill-workspace/code-cleanup/latest/deletion-candidates.json

python plugins/code-cleanup/skills/code-cleanup-skill/scripts/render_cleanup_report.py \
  --input .skill-workspace/code-cleanup/latest/deletion-candidates.json \
  --output-dir .skill-workspace/code-cleanup/latest
```

### B. 作为本地 Cursor Skill 使用（兼容模式，可选）

> 说明：此模式仅用于兼容本地 Cursor Skill 工作流，不是 Claude 插件发布必需步骤。

```bash
python .cursor/skills/code-cleanup-skill/scripts/analyze_cleanup_candidates.py \
  --project-root . \
  --keep-list .cursor/skills/code-cleanup-skill/config/keep-list.txt \
  --output .cursor/skills/code-cleanup-skill-workspace/latest/deletion-candidates.json

python .cursor/skills/code-cleanup-skill/scripts/render_cleanup_report.py \
  --input .cursor/skills/code-cleanup-skill-workspace/latest/deletion-candidates.json \
  --output-dir .cursor/skills/code-cleanup-skill-workspace/latest
```

## 与用户沟通模板

在给用户反馈时，优先给：

1. 高风险候选（最可能可删）
2. 误删风险点（动态路由/运行时注册）
3. 下一步建议（先删小批次、跑回归）

示例：

- "本次识别出 12 个高置信候选、8 个需人工确认候选。建议先处理高置信候选并执行 smoke test，再处理中风险项。"
