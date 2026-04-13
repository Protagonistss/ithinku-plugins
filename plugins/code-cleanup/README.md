# Code Cleanup Plugin

面向任意项目的安全清理插件，支持多语言（JS/TS/Python/Go/Java/PHP/Ruby/Rust/C++），用于识别未引用模块、未使用组件和历史死代码，并生成"可执行但默认不自动删除"的候选报告。

## 核心能力

- 未引用模块识别（页面、组件、服务、工具类等，通过 `config/scan-dirs.txt` 配置）
- 历史备份/死代码识别（`*-copy.*`, `*-bf.*`, `*-old.*` 等）
- 风险分级输出（`high` / `medium` / `low`）
- 生成清理报告与回滚友好的补丁计划

## 配置文件

| 文件 | 用途 |
|------|------|
| `config/scan-dirs.txt` | 扫描目录、类别名、关键词策略 |
| `config/ext-list.txt` | 参与扫描的文件扩展名 |
| `config/keep-list.txt` | 白名单，始终保留的文件路径 |

配置文件均不存在时使用内置默认值。

## 目录结构

```text
plugins/code-cleanup/
├─ README.md
└─ skills/
   └─ code-cleanup-skill/
      ├─ SKILL.md
      ├─ config/
      │  ├─ scan-dirs.txt
      │  ├─ ext-list.txt
      │  └─ keep-list.txt
      ├─ evals/
      │  └─ evals.json
      └─ scripts/
         ├─ analyze_cleanup_candidates.py
         └─ render_cleanup_report.py
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
