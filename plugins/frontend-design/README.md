# Frontend Design Plugin

---
name: frontend-design
description: 前端设计专家代理，专注于UI/UX设计、响应式布局、色彩方案和无障碍设计
color: purple
icon: 🎨
---

专业的Web前端设计插件，提供核心的设计解决方案，帮助你创建美观、易用的界面。

## 🎨 核心功能

- 🎨 **UI/UX设计** - 界面设计和用户体验
- 📱 **响应式设计** - 多设备自适应布局
- 🌈 **色彩搭配** - 配色方案和视觉设计
- ♿ **无障碍设计** - 包容性访问支持

## 🔍 触发关键词

- 设计、UI、界面、视觉、样式
- UX、用户体验、交互设计
- 响应式、移动端、适配、布局
- 颜色、配色、主题、色彩方案
- 无障碍、可访问性、a11y、WCAG

## ⚙️ 配置选项

在项目根目录创建 `claude-plugins.config.json`:

```json
{
  "frontend-design": {
    "designSystem": {
      "theme": "material", // material, antd, bootstrap, custom
      "colorScheme": "light", // light, dark, auto
      "primaryColor": "#1976d2"
    },
    "accessibility": {
      "wcagLevel": "AA", // A, AA, AAA
      "autoCheck": true
    },
    "responsive": {
      "breakpoints": {
        "mobile": "768px",
        "tablet": "1024px",
        "desktop": "1200px"
      }
    },
    "animation": {
      "duration": {
        "fast": "200ms",
        "normal": "300ms",
        "slow": "500ms"
      },
      "easing": "ease-out"
    }
  }
}
```

## 🚀 使用方式

插件已配置好触发关键词，可以直接使用：

```
设计一个登录页面的UI布局
创建一个响应式的卡片组件
检查这个界面的无障碍设计
```

## 📁 目录结构

```
frontend-design/
├── README.md                    # 插件说明文档
├── skills/                      # 核心设计技能
│   ├── ui-ux/                   # UI/UX设计
│   │   └── SKILL.md
│   ├── responsive/              # 响应式设计
│   │   └── SKILL.md
│   ├── color/                   # 色彩搭配
│   │   └── SKILL.md
│   └── accessibility/           # 无障碍设计
│       └── SKILL.md
```

## 💡 使用场景

### 1. 界面设计

```
设计一个登录页面的UI布局
创建一个响应式的卡片组件
设计一个数据仪表板的布局
```

### 2. 样式实现

```
使用CSS Grid创建响应式布局
设计一个现代化的导航栏
实现深色/浅色主题切换
```

### 3. 设计审查

```
检查这个页面的WCAG可访问性
优化这个表单的用户体验
审查配色方案的对比度
```

## 🛠 技能详解

### UI/UX设计
- 界面布局和视觉设计
- 用户体验流程优化
- 交互模式设计
- 可用性最佳实践

### 响应式设计
- 多设备适配策略
- 弹性布局实现
- 断点和媒体查询
- 移动优先设计

### 色彩搭配
- 配色方案设计
- 对比度优化
- 主题系统实现
- 视觉层次建立

### 无障碍设计
- WCAG标准遵循
- 键盘导航支持
- 屏幕阅读器优化
- 包容性设计实践

## 🎯 最佳实践

1. **简洁设计** - 保持界面清晰、直观
2. **响应式优先** - 确保多设备良好体验
3. **可访问性** - 遵循WCAG标准
4. **一致性** - 统一的设计风格
5. **用户友好** - 关注用户体验

## 🔗 相关插件

- [component-generator](../component-generator/) - 组件代码生成
- [code-review](../code-review/) - 代码审查