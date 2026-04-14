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
2. **性能与过滤优化**：
   - **原生 Git 支持**：优先通过 `git ls-files` 获取文件列表，原生支持所有 `.gitignore` 规则（包含父级目录中的规则）。
   - **高效遍历回退**：非 Git 环境下自动使用带“剪枝（Prune）”技术的 `os.walk` 遍历，直接跳过 `node_modules`、`.idea`、`.vscode` 等巨大干扰目录。
   - **向上查找 `.gitignore`**：回退模式下会自动向上查找并解析各层级 `.gitignore` 规则。
3. 所有候选必须带"证据"与"风险等级"
4. 输出必须包含回滚建议

## 配置驱动

所有扫描行为通过配置文件控制。脚本采用**“就近原则”**加载配置（优先级从高到低）：

1. **显式参数**：命令行传入的 `--keep-list` 等参数。
2. **项目本地配置**：目标项目根目录下的 `.code-cleanup/` 文件夹（推荐用于全局安装场景）。
3. **Cursor 集成配置**：目标项目根目录下的 `.cursor/skills/code-cleanup-skill/config/`。
4. **插件内置默认配置**：Skill 文件夹自带的 `config/` 目录。

| 配置文件 | 用途 |
|---------|------|
| `scan-dirs.txt` | 扫描哪些目录、类别名、关键词策略 |
| `ext-list.txt` | 哪些扩展名参与扫描 |
| `keep-list.txt` | 白名单，始终保留的文件 |

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

必须遵循以下严格的三阶段闭环，确保清理过程可视化、安全授权、彻底清理且成果可度量。

### Phase 1: 扫描 (Scan)
1. **执行初始扫描**：调用 `analyze_cleanup_candidates.py` 扫描当前工作空间。
   - 产出 `before.json`。
   - Agent 需提取 JSON 中的 `project_stats` 展示项目“健康分”与规模。
2. **生成可视化报告**：调用 `render_cleanup_report.py` 生成工业风报告。
   - 产出 `cleanup-report.html`。
   - **必须**提供报告的本地绝对路径，提示用户：“已生成初始报告，请在浏览器中打开进行可视化评审。”

### Phase 2: 评审与授权 (Review & Authorize)
1. **阻塞等待**：Agent **严禁**自主执行删除。必须明确等待用户查看报告后给出指令（如：“清理所有高风险”、“删除特定列表”）。
2. **确认变更范围**：在执行前，Agent 需向用户二次确认将要删除的文件总数。

### Phase 3: 执行、清扫与对比 (Execute, Purge & Diff)
1. **自动化清理**：根据授权指令，读取 JSON 执行物理删除。
2. **彻底清扫 (Purge)**：文件删除后，**必须**清理项目中因此产生的空目录。
   - 执行 `find . -type d -empty -not -path "./.git/*" -delete` (或对应平台的等价命令)。
3. **二次扫描验证**：删除完成后，**自动**再次运行扫描脚本。
   - 产出 `after.json`。
4. **生成战果报告 (Comparison)**：调用渲染脚本，使用 `--previous before.json` 参数。
   - 生成带 **“🏆 CLEANUP ACHIEVED / 清理战果”** 横幅的最终 HTML 报告。
5. **成果总结**：向用户汇报健康分提升了多少点，节省了多少空间。

## 执行边界

- **授权至上**：严禁在未获得用户明确授权的情况下执行物理删除。
- **彻底清理**：删除文件后必须顺手清理残留的空目录。
- **不凭直觉**：Agent 必须严格按照 Phase 1 产出的 JSON 路径执行，禁止猜测路径。

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
  "project_stats": {
    "total_files_scanned": 1500,
    "total_size_bytes": 1024000,
    "unused_files_count": 12,
    "unused_size_bytes": 51200,
    "health_score": 95
  },
  "candidates": [
    {
      "path": "src/page/example/example.js",
      "category": "unused_page",
      "risk_level": "high",
      "evidence": [
        "未在其他源码文件中找到对 `example` 的直接引用"
      ],
      "file_size_bytes": 4096,
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
