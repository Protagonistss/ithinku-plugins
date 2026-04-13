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

## 工作流

### Step 1: 收集入口与引用关系

- 扫描路由入口、模块入口、全局注册
- 扫描各语言的 import/require/include 语法
- 扫描字符串引用（如路由跳转 `push('/x')`、路径拼接）

### Step 2: 识别候选清理对象

根据 `config/scan-dirs.txt` 配置扫描各目录：
- 未引用页面（`src/page/**`、`src/pages/**`）
- 未使用组件（`src/components/**`）
- 未使用模块（`src/services/**`、`src/utils/**`、`src/controllers/**` 等）
- 死代码/历史文件（`*-copy.*`、`*-bf.*`、`*-old.*`）

### Step 3: 风险分级

- `high`: 多轮检查均未发现引用，且不在入口白名单
- `medium`: 命中部分弱引用线索（字符串、动态路径），需人工确认
- `low`: 仅命中命名模式（如 old/copy/bf），证据较弱

> 若命中"字符串路径/动态引用"弱引用线索，优先降级为 `medium`，避免误删。

### Step 4: 生成结果

必须输出三个文件：

1. `cleanup-report.md`
   - 高/中/低风险分组
   - 每个候选包含路径、类型、证据、建议动作
2. `deletion-candidates.json`
   - 机器可读候选列表，含 `risk_level` 与 `evidence`
3. `patch-plan.md`
   - 删除/替换步骤、依赖影响、回滚命令

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
