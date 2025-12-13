# Responsive Design Skill

## 技能描述

专业的响应式设计技能，创建适配各种设备和屏幕尺寸的网页设计，确保最佳的用户体验。

## 核心功能

- 📱 **多端适配** - 手机、平板、桌面全设备覆盖
- 📐 **弹性布局** - 灵活的网格和布局系统
- 🖼️ **响应式媒体** - 图片、视频的自适应显示
- 🔧 **断点管理** - 科学的断点设置和管理
- ⚡ **性能优化** - 移动端加载性能优化

## 快速使用

```bash
# 创建响应式布局
/frontend-design 创建一个三栏响应式布局，移动端单栏显示

# 优化移动端体验
/frontend-design 优化这个网站在移动设备上的显示效果

# 设计断点策略
/frontend-design 为电商网站设计合适的响应式断点
```

## 配置

```json
{
  "responsiveDesign": {
    "breakpoints": {
      "mobile": "320-767px",
      "tablet": "768-1023px",
      "desktop": "1024-1439px",
      "wide": "1440px+"
    },
    "containerMaxWidths": {
      "mobile": "100%",
      "tablet": "720px",
      "desktop": "1140px",
      "wide": "1320px"
    },
    "gutters": {
      "mobile": "16px",
      "tablet": "24px",
      "desktop": "32px"
    },
    "strategies": {
      "mobileFirst": true,
      "progressiveEnhancement": true
    }
  }
}
```

## 响应式设计原则

### 1. Mobile First
- 优先设计移动端体验
- 渐进增强到更大屏幕
- 关注核心功能和内容

### 2. 内容优先
- 确保内容在任何设备都可读
- 重要信息优先显示
- 保持内容的一致性

### 3. 触摸友好
- 最小点击区域 44px
- 适当的间距避免误触
- 支持手势操作

### 4. 性能优先
- 优化移动端加载速度
- 延迟加载非关键内容
- 压缩和优化资源

## 布局策略

### 流式布局
```css
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

### 弹性盒布局
```css
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.flex-item {
  flex: 1;
  min-width: 250px;
}
```

## 媒体查询

### 断点设置
```css
/* 移动设备 */
@media (max-width: 767px) {
  /* 移动端样式 */
}

/* 平板设备 */
@media (min-width: 768px) and (max-width: 1023px) {
  /* 平板端样式 */
}

/* 桌面设备 */
@media (min-width: 1024px) {
  /* 桌面端样式 */
}
```

### 容器查询
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
    align-items: center;
  }
}
```

## 响应式图片

### 图片优化
```html
<!-- 响应式图片 -->
<img srcset="small.jpg 480w, medium.jpg 768w, large.jpg 1024w"
     sizes="(max-width: 600px) 480px, (max-width: 900px) 768px, 1024px"
     src="medium.jpg"
     alt="描述文字">

<!-- 艺术指导 -->
<picture>
  <source media="(min-width: 768px)" srcset="large.jpg">
  <source media="(min-width: 480px)" srcset="medium.jpg">
  <img src="small.jpg" alt="描述文字">
</picture>
```

### 图片技术
- WebP格式支持
- 懒加载实现
- 响应式内嵌图片
- CSS图像优化

## 常见响应式模式

### 1. 导航适配
- 汉堡菜单（移动端）
- 折叠菜单
- 底部标签栏
- 顶部图标导航

### 2. 卡片布局
- 单列（移动端）
- 双列（小平板）
- 三列（大平板）
- 网格（桌面端）

### 3. 表格处理
- 水平滚动
- 卡片式转换
- 关键列固定
- 详情页跳转

### 4. 表单布局
- 垂直堆叠
- 分组显示
- 步骤引导
- 弹窗优化

## 测试方法

### 设备测试
- 真实设备测试
- 浏览器开发者工具
- 响应式测试工具
- 远程调试

### 测试工具
- Chrome DevTools
- Firefox Responsive Design Mode
- BrowserStack
- LambdaTest

## 详细信息

### 常见断点
- 移动端：320px - 768px
- 平板端：768px - 1024px
- 桌面端：1024px+

### 布局技术
- CSS Grid - 复杂布局
- Flexbox - 一维布局
- 容器查询 - 基于容器的响应式