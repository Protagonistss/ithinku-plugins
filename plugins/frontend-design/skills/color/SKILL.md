# Color Theory Skill

## 技能描述

专业的色彩理论和配色方案设计技能，帮助创建视觉吸引力强、品牌一致且符合无障碍标准的配色方案。

## 核心功能

- 🎨 **配色方案** - 生成和谐的色彩搭配
- 🌈 **色彩心理** - 理解颜色对情绪和行为的影响
- 🔆 **明暗主题** - 设计亮色和暗色主题
- ♿ **对比度检查** - 确保无障碍设计标准
- 📊 **色彩系统** - 建立统一的色彩语言

## 快速使用

```bash
# 创建配色方案
/frontend-design 为品牌设计一个以蓝色为主的专业配色方案

# 检查对比度
/frontend-design 检查这个配色的WCAG对比度是否符合标准

# 设计主题切换
/frontend-design 创建支持亮色/暗色模式切换的配色系统
```

## 配置

```json
{
  "colorTheory": {
    "primaryColor": "#1976d2",
    "colorSystem": {
      "model": "HSL", // RGB, HSL, HEX
      "notation": "CSS Custom Properties"
    },
    "accessibility": {
      "wcagLevel": "AA",
      "contrastRatio": {
        "normal": 4.5,
        "large": 3.0
      }
    },
    "themeSupport": {
      "light": true,
      "dark": true,
      "system": true
    },
    "colorPalette": {
      "type": "tetradic", // monochromatic, analogous, complementary, triadic, tetradic
      "saturation": 0.8,
      "lightness": 0.5
    }
  }
}
```

## 色彩基础

### 色彩三要素
- **色相(Hue)** - 颜色的基本属性（红、黄、蓝等）
- **饱和度(Saturation)** - 颜色的纯度和强度
- **明度(Lightness)** - 颜色的明暗程度

### 色彩模型
- **RGB** - 光的三原色（屏幕显示）
- **HSL** - 更直观的色彩表示
- **HSV** - 适用于色彩选择器
- **CMYK** - 印刷四色模式

## 配色方案

### 1. 单色配色
基于单一色相的明暗变化
```
主色: #1976d2
浅色: #42a5f5
深色: #1565c0
辅助: #0d47a1
```

### 2. 类似色配色
色轮上相邻的颜色
```
主色: #1976d2 (蓝)
辅助1: #1565c0 (深蓝)
辅助2: #1e88e5 (浅蓝)
强调: #00897b (青绿)
```

### 3. 互补色配色
色轮上相对的颜色
```
主色: #1976d2 (蓝)
互补: #d32f2f (红橙)
```

### 4. 三角色配色
色轮上等距的三个颜色
```
主色: #1976d2 (蓝)
辅助1: #388e3c (绿)
辅助2: #f57c00 (橙)
```

## 语义化色彩

### 功能色彩
```css
:root {
  /* 成功 */
  --color-success: #4caf50;
  --color-success-light: #81c784;
  --color-success-dark: #388e3c;

  /* 警告 */
  --color-warning: #ff9800;
  --color-warning-light: #ffb74d;
  --color-warning-dark: #f57c00;

  /* 错误 */
  --color-error: #f44336;
  --color-error-light: #e57373;
  --color-error-dark: #d32f2f;

  /* 信息 */
  --color-info: #2196f3;
  --color-info-light: #64b5f6;
  --color-info-dark: #1976d2;
}
```

### 中性色彩
```css
:root {
  /* 文字颜色 */
  --color-text-primary: rgba(0, 0, 0, 0.87);
  --color-text-secondary: rgba(0, 0, 0, 0.6);
  --color-text-disabled: rgba(0, 0, 0, 0.38);

  /* 背景颜色 */
  --color-background: #ffffff;
  --color-surface: #fafafa;
  --color-overlay: rgba(0, 0, 0, 0.5);

  /* 边框颜色 */
  --color-border: rgba(0, 0, 0, 0.12);
  --color-divider: rgba(0, 0, 0, 0.08);
}
```

## 主题系统

### 亮色主题
```css
[data-theme="light"] {
  --color-background: #ffffff;
  --color-surface: #f5f5f5;
  --color-text: #000000;
  --color-text-secondary: rgba(0, 0, 0, 0.7);
}
```

### 暗色主题
```css
[data-theme="dark"] {
  --color-background: #121212;
  --color-surface: #1e1e1e;
  --color-text: #ffffff;
  --color-text-secondary: rgba(255, 255, 255, 0.7);
}
```

### 主题切换
```javascript
// JavaScript 主题切换
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}
```

## 无障碍设计

### 对比度标准
- **WCAG AA级** - 普通文本 4.5:1，大文本 3:1
- **WCAG AAA级** - 普通文本 7:1，大文本 4.5:1

### 对比度检查工具
- WebAIM Contrast Checker
- Adobe Color Accessibility Tools
- Contrast Ratio
- Stark Plugin

### 额外提示
- 不要仅依靠颜色传达信息
- 为色盲用户提供足够的对比度
- 测试不同类型色盲的效果

## 色彩工具

### 在线工具
- Adobe Color
- Coolors.co
- ColorSpace
- Paletton
- ColorHunt

### 设计软件集成
- Figma 色彩插件
- Sketch 色彩管理
- Adobe Color 集成

## 实践建议

### 1. 限制颜色数量
- 主要颜色：1-2个
- 辅助颜色：2-3个
- 中性颜色：3-5个
- 功能颜色：按需定义

### 2. 保持一致性
- 使用设计令牌管理
- 建立清晰的命名规范
- 文档化使用规则

### 3. 考虑上下文
- 品牌识别度
- 目标用户群体
- 文化差异
- 使用场景

## 详细信息

### 色彩工具
- Adobe Color - 配色方案生成
- Coolors - 色彩灵感
- Contrast Checker - 对比度检测

### 色彩技巧
- 60-30-10规则（主色-辅色-点缀色）
- 限制颜色数量（3-5种）
- 考虑文化差异和情感影响