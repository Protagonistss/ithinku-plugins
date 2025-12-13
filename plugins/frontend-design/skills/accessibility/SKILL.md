# Accessibility Design Skill

## 技能描述

专业的无障碍设计技能，创建包容性强、可访问性高的界面设计，确保所有用户都能平等地访问和使用产品。

## 核心功能

- ♿ **WCAG合规** - 遵循Web内容无障碍指南
- 🔍 **可访问性测试** - 自动化和手动测试工具
- 🎯 **键盘导航** - 完整的键盘操作支持
- 🗣️ **屏幕阅读器** - 优化屏幕阅读器体验
- 🎨 **视觉辅助** - 色彩对比度和视觉辅助

## 快速使用

```bash
# 检查无障碍合规
/frontend-design 检查网站是否符合WCAG 2.1 AA标准

# 优化键盘导航
/frontend-design 为整个应用添加完整的键盘导航支持

# 改善屏幕阅读器体验
/frontend-design 优化表单的屏幕阅读器可访问性
```

## 配置

```json
{
  "accessibility": {
    "wcag": {
      "level": "AA", // A, AA, AAA
      "version": "2.1"
    },
    "testing": {
      "automated": ["axe", "lighthouse"],
      "manual": ["keyboard", "screen-reader"]
    },
    "features": {
      "skipLinks": true,
      "focusManagement": true,
      "ariaLabels": true,
      "altText": true
    },
    "preferences": {
      "respectReducedMotion": true,
      "respectColorScheme": true,
      "highContrastMode": true
    }
  }
}
```

## WCAG 指南

### 四大原则

#### 1. 可感知 (Perceivable)
- **替代文本** - 为非文本内容提供替代
- **字幕和音频描述** - 为多媒体提供替代
- **可适配** - 以不同方式呈现内容
- **可区分** - 让内容更容易看到和听到

#### 2. 可操作 (Operable)
- **键盘可访问** - 所有功能都可通过键盘访问
- **足够时间** - 提供足够时间使用内容
- **癫痫预防** - 不要设计引发癫痫的内容
- **导航辅助** - 帮助用户导航和查找内容

#### 3. 可理解 (Understandable)
- **可读文本** - 文本内容可读且可理解
- **可预测** - 网页的呈现和操作是可预测的
- **输入辅助** - 帮助用户避免和纠正错误

#### 4. 健壮 (Robust)
- **兼容性** - 最大化与各种辅助技术的兼容性

## 键盘导航

### 焦点管理
```css
/* 清晰的焦点样式 */
.focusable:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* 跳过链接 */
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--color-primary);
  color: white;
  padding: 8px;
  z-index: 100;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 6px;
}

/* 焦点陷阱 */
.focus-trap {
  outline: none;
}

/* 隐藏元素但保持可访问性 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### JavaScript 焦点管理
```javascript
// 焦点捕获
class FocusTrap {
  constructor(element) {
    this.element = element;
    this.focusableElements = this.element.querySelectorAll(
      'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    this.firstElement = this.focusableElements[0];
    this.lastElement = this.focusableElements[this.focusableElements.length - 1];
  }

  activate() {
    this.element.addEventListener('keydown', this.handleKeydown.bind(this));
    this.firstElement.focus();
  }

  handleKeydown(e) {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === this.firstElement) {
          e.preventDefault();
          this.lastElement.focus();
        }
      } else {
        if (document.activeElement === this.lastElement) {
          e.preventDefault();
          this.firstElement.focus();
        }
      }
    }
  }
}
```

## ARIA 属性

### 语义化标记
```html
<!-- 地标角色 -->
<header role="banner">
  <nav role="navigation" aria-label="主导航">
    <ul>
      <li><a href="/" aria-current="page">首页</a></li>
      <li><a href="/about">关于</a></li>
    </ul>
  </nav>
</header>

<main role="main">
  <section aria-labelledby="section-heading">
    <h2 id="section-heading">部分标题</h2>
    <p>内容...</p>
  </section>
</main>

<aside role="complementary" aria-label="侧边栏">
  <p>补充内容</p>
</aside>

<footer role="contentinfo">
  <p>版权信息</p>
</footer>
```

### 动态内容
```html
<!-- 实时区域 -->
<div aria-live="polite" aria-atomic="true" id="status-message">
  <!-- 状态消息会在这里显示 -->
</div>

<!-- 进度条 -->
<div role="progressbar"
     aria-valuenow="33"
     aria-valuemin="0"
     aria-valuemax="100"
     aria-label="上传进度">
  33%
</div>

<!-- 折叠内容 -->
<button aria-expanded="false"
        aria-controls="collapse-content"
        id="collapse-button">
  显示更多
</button>
<div id="collapse-content" hidden>
  隐藏的内容
</div>
```

### 表单可访问性
```html
<!-- 表单标签关联 -->
<fieldset>
  <legend>用户信息</legend>

  <div>
    <label for="email">电子邮箱：</label>
    <input type="email"
           id="email"
           name="email"
           required
           aria-describedby="email-help email-error"
           aria-invalid="false">
    <div id="email-help" class="help-text">
      请输入您的邮箱地址
    </div>
    <div id="email-error" class="error-text" role="alert" hidden>
      请输入有效的邮箱地址
    </div>
  </div>

  <div>
    <label for="password">密码：</label>
    <input type="password"
           id="password"
           name="password"
           required
           aria-describedby="password-requirements">
    <div id="password-requirements" class="help-text">
      密码至少8个字符，包含字母和数字
    </div>
  </div>
</fieldset>
```

## 色彩和对比度

### 对比度要求
```css
/* WCAG AA级别 */
- 普通文本：至少 4.5:1
- 大文本（18pt+ 或 14pt粗体+）：至少 3:1
- 图形元素：至少 3:1

/* WCAG AAA级别 */
- 普通文本：至少 7:1
- 大文本：至少 4.5:1
```

### 色彩使用原则
```css
:root {
  /* 确保足够的对比度 */
  --text-primary: #000000; /* 对白色背景对比度 21:1 */
  --text-secondary: #333333; /* 对白色背景对比度 12.6:1 */
  --text-disabled: #666666; /* 对白色背景对比度 7:1 */

  /* 避免仅用颜色传达信息 */
  --error-color: #d32f2f;
  --success-color: #388e3c;

  /* 提供额外的视觉提示 */
  --error-border: 2px solid var(--error-color);
  --success-border: 2px solid var(--success-color);
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  :root {
    --text-primary: #000000;
    --background-color: #ffffff;
    --border-color: #000000;
  }
}

/* 强制色彩模式支持 */
@media (forced-colors: active) {
  button {
    border: 2px solid ButtonText;
    background-color: ButtonFace;
    color: ButtonText;
  }
}
```

## 语义化 HTML

### 正确使用标签
```html
<!-- 标题层级 -->
<h1>主标题</h1>
  <h2>二级标题</h2>
    <h3>三级标题</h3>
  <h2>另一个二级标题</h2>

<!-- 列表 -->
<ul>
  <li>无序列表项</li>
  <li>另一个列表项</li>
</ul>

<ol>
  <li>有序列表项</li>
  <li>另一个有序列表项</li>
</ol>

<!-- 表格 -->
<table>
  <caption>月度销售数据</caption>
  <thead>
    <tr>
      <th scope="col">月份</th>
      <th scope="col">销售额</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">一月</th>
      <td>$10,000</td>
    </tr>
  </tbody>
</table>
```

## 测试工具

### 自动化测试
```javascript
// 使用 axe-core 进行自动化测试
import axe from 'axe-core';

const runAccessibilityTests = async () => {
  const results = await axe.run(document.body);

  if (results.violations.length) {
    console.log('发现无障碍问题：', results.violations);
    results.violations.forEach(violation => {
      console.log('问题：', violation.description);
      console.log('影响：', violation.impact);
      console.log('元素：', violation.nodes.map(node => node.target));
    });
  }

  return results;
};

// 在测试环境中运行
describe('无障碍测试', () => {
  it('页面应该没有严重的无障碍问题', async () => {
    const results = await runAccessibilityTests();
    const criticalIssues = results.violations.filter(
      v => v.impact === 'critical'
    );
    expect(criticalIssues).toHaveLength(0);
  });
});
```

### 浏览器扩展
- **Axe DevTools** - Chrome扩展，实时测试
- **WAVE** - WebAIM的评估工具
- **Accessibility Insights** - 微软的工具套件
- **Lighthouse** - 包含可访问性审计

## 手动测试清单

### 键盘导航测试
- [ ] Tab键可以访问所有交互元素
- [ ] Shift+Tab可以反向导航
- [ ] Enter和Space激活按钮和链接
- [ ] 方向键操作菜单和列表
- [ ] Escape关闭弹窗和菜单
- [ ] 焦点始终可见且合理

### 屏幕阅读器测试
- [ ] 所有图片有alt文本
- [ ] 表单字段有标签
- [ ] 页面结构清晰（标题、地标）
- [ ] 动态内容被宣布
- [ ] 错误消息被朗读
- [ ] 链接文本有描述性

### 视觉测试
- [ ] 文本对比度达到标准
- [ ] 颜色不是唯一的信息传达方式
- [ ] 文本可以放大到200%
- [ ] 页面在高对比度模式下可用
- [ ] 不使用闪烁内容

## 用户体验增强

### 减少动画偏好
```css
/* 尊重用户的动画偏好 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 个人化支持
```css
/* 色彩方案偏好 */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #121212;
    --text-color: #ffffff;
  }
}

@media (prefers-color-scheme: light) {
  :root {
    --bg-color: #ffffff;
    --text-color: #000000;
  }
}

/* 自定义属性覆盖 */
[data-user-font-size="large"] {
  font-size: 1.2em;
}

[data-user-spacing="wide"] {
  --spacing-unit: 1.5em;
}
```

## 最佳实践

### 1. 设计阶段
- 考虑不同用户需求
- 使用高对比度设计
- 保持一致的交互模式
- 提供多种输入方式

### 2. 开发阶段
- 使用语义化HTML
- 添加ARIA属性
- 实现键盘导航
- 测试屏幕阅读器兼容性

### 3. 测试阶段
- 自动化测试覆盖
- 手动测试验证
- 真实用户测试
- 持续改进

## 详细信息

### WCAG速查
- A级：基础可访问性
- AA级：标准要求（推荐）
- AAA级：最高标准

### 测试工具
- axe-core - 自动化测试
- Lighthouse - 性能和可访问性
- WAVE - 可视化检测
- 屏幕阅读器测试（NVDA, VoiceOver）