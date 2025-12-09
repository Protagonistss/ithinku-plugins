# 测试插件集成技能

这个技能负责检测和集成 unit-test-generator 插件，让 dev-tools 能够调用专业的测试生成功能。

## 技能能力

### 1. 插件检测
- 检查 unit-test-generator 插件是否已安装
- 获取插件版本和支持的功能
- 验证插件兼容性

### 2. 功能代理
- 将测试生成请求转发给专业插件
- 传递命令参数和选项
- 处理插件返回的结果

### 3. 降级处理
- 在专业插件未安装时提供基础测试生成
- 给出安装专业插件的提示
- 记录用户偏好

## 使用方式

### 插件检测

```typescript
// 检查测试插件是否可用
const hasTestPlugin = await checkUnitTestGeneratorPlugin();
if (hasTestPlugin) {
  // 使用专业模式
  return await callTestPlugin(target, options);
} else {
  // 使用基础模式
  return generateBasicTest(target, options);
}
```

### 调用专业插件

```typescript
// 代理调用测试插件
async function callTestPlugin(target: string, options: TestOptions) {
  const skillArgs = {
    plugin: 'unit-test-generator',
    skill: 'unit-test-generation',
    params: {
      target,
      framework: options.framework || 'jest',
      outputDir: options.outputDir,
      includeMocks: options.mock || false,
      coverage: options.coverage || false
    }
  };

  return await callPluginSkill(skillArgs);
}
```

## 实现逻辑

### 1. 插件检测逻辑

```typescript
async function checkUnitTestGeneratorPlugin(): Promise<boolean> {
  try {
    // 检查插件目录是否存在
    const pluginPath = path.join(process.cwd(), 'plugins', 'unit-test-generator');
    const exists = await fs.pathExists(pluginPath);

    if (!exists) {
      return false;
    }

    // 检查插件配置
    const configPath = path.join(pluginPath, '.claude-plugin', 'plugin.json');
    const config = await fs.readJson(configPath);

    // 验证插件名称和版本
    return config.name === 'unit-test-generator' &&
           semver.gte(config.version, '1.0.0');
  } catch (error) {
    console.error('Failed to check unit-test-generator plugin:', error);
    return false;
  }
}
```

### 2. 用户交互提示

```typescript
async function promptUserForTestMode(): Promise<boolean> {
  const response = await promptUser({
    type: 'confirm',
    message: '检测到 unit-test-generator 插件，是否使用专业测试生成模式？',
    default: true,
    choices: [
      { name: '是 - 使用专业测试插件', value: true },
      { name: '否 - 使用基础测试生成', value: false }
    ]
  });

  // 记录用户选择
  await setUserPreference('use-professional-test', response);

  return response;
}
```

### 3. 命令参数转换

```typescript
function convertGenOptionsToTestOptions(genOptions: GenOptions): TestOptions {
  return {
    target: genOptions.target,
    framework: genOptions.framework || detectFrameworkFromProject(),
    outputDir: genOptions.output || getDefaultTestDir(),
    includeMocks: genOptions.mock || false,
    coverage: genOptions.coverage || false,
    update: genOptions.update || false,
    skipSetup: genOptions.skipSetup || false
  };
}

function detectFrameworkFromProject(): string {
  // 检测项目使用的测试框架
  if (hasPackage('vitest')) return 'vitest';
  if (hasPackage('jest')) return 'jest';
  if (hasPackage('pytest')) return 'pytest';
  if (hasPackage('junit')) return 'junit';

  return 'vitest'; // 默认框架
}
```

## 降级方案

### 基础测试生成

```typescript
async function generateBasicTest(target: string, options: GenOptions): Promise<TestResult> {
  const testTemplate = await loadTestTemplate(options.framework || 'jest');

  // 基础代码分析
  const codeInfo = await analyzeCode(target);

  // 生成基础测试
  const testCode = await fillTemplate(testTemplate, {
    target: codeInfo.name,
    functions: codeInfo.functions,
    className: codeInfo.className,
    imports: codeInfo.imports
  });

  // 写入测试文件
  const testPath = getTestPath(target);
  await writeFile(testPath, testCode);

  return {
    success: true,
    testPath,
    message: `基础测试已生成: ${testPath}\n提示：安装 unit-test-generator 插件以获得更强大的测试生成功能`
  };
}
```

### 安装提示

```typescript
function generateInstallPrompt(): string {
  return `
⚡ 提升您的测试体验！

安装 unit-test-generator 插件以获得：
✨ 支持更多测试框架 (Jest, Vitest, Pytest, JUnit等)
🎭 自动生成Mock数据和Stub函数
🎯 智能边界值和错误场景测试
📊 测试覆盖率分析和优化建议
🤖 测试专家代理 (@TestExpert)

安装方法：
1. 下载插件: https://github.com/Protagonisths/claude-plugins
2. 复制到插件目录
3. 重启 Claude Code

或者使用 dev-tools 安装：
/install-plugin unit-test-generator
  `;
}
```

## 集成示例

### 在 gen 命令中使用

```typescript
// 处理 /gen test 命令
if (command === 'test') {
  const target = args[0];
  const options = parseOptions(args.slice(1));

  // 检测专业插件
  const hasPlugin = await checkUnitTestGeneratorPlugin();

  if (hasPlugin) {
    // 检查用户偏好或提示选择
    const useProfessional = await getUserPreference('use-professional-test') ??
                            await promptUserForTestMode();

    if (useProfessional) {
      return await callTestPlugin(target, options);
    }
  }

  // 使用基础测试生成
  const result = await generateBasicTest(target, options);

  // 显示安装提示
  if (!hasPlugin) {
    console.log(generateInstallPrompt());
  }

  return result;
}
```

### 技能调用接口

```typescript
// 调用测试插件技能的标准接口
interface TestPluginSkillCall {
  plugin: 'unit-test-generator';
  skill: string;
  params: {
    target: string;
    framework?: string;
    outputDir?: string;
    includeMocks?: boolean;
    coverage?: boolean;
    update?: boolean;
    [key: string]: any;
  };
}

// 执行调用
async function executeTestPluginSkill(skillCall: TestPluginSkillCall): Promise<any> {
  try {
    // 通过 Claude Code 的技能调用机制执行
    const result = await callSkill(skillCall.plugin, skillCall.skill, skillCall.params);

    // 处理返回结果
    if (result.success) {
      // 触发钩子事件
      await triggerHook('onTestGenerated', {
        target: skillCall.params.target,
        outputPath: result.testPath,
        framework: skillCall.params.framework
      });
    }

    return result;
  } catch (error) {
    console.error('Failed to execute test plugin skill:', error);
    throw error;
  }
}
```

## 配置和偏好

### 用户偏好设置

```typescript
// 用户偏好存储
interface UserPreferences {
  useProfessionalTest?: boolean;
  defaultTestFramework?: string;
  autoGenerateMocks?: boolean;
  promptForPluginInstall?: boolean;
}

// 获取用户偏好
async function getUserPreference(key: keyof UserPreferences): Promise<any> {
  const prefs = await loadUserPreferences();
  return prefs[key];
}

// 设置用户偏好
async function setUserPreference(key: keyof UserPreferences, value: any): Promise<void> {
  const prefs = await loadUserPreferences();
  prefs[key] = value;
  await saveUserPreferences(prefs);
}
```

### 项目级配置

```typescript
// 项目配置 (test-integration.config.json)
interface ProjectConfig {
  testPlugin?: {
    enabled: boolean;
    framework?: string;
    outputDir?: string;
    autoMock?: boolean;
    coverageThreshold?: number;
  };
  fallback?: {
    framework?: string;
    template?: string;
  };
}

// 读取项目配置
async function loadProjectConfig(): Promise<ProjectConfig> {
  const configPath = path.join(process.cwd(), 'test-integration.config.json');

  if (await fs.pathExists(configPath)) {
    return await fs.readJson(configPath);
  }

  return {};
}
```

## 最佳实践

### 1. 无缝集成
- 自动检测插件安装状态
- 提供清晰的降级方案
- 记住用户选择偏好

### 2. 错误处理
- 优雅处理插件调用失败
- 提供有用的错误信息
- 自动回退到基础功能

### 3. 性能优化
- 缓存插件检测结果
- 避免重复的用户提示
- 并行处理插件调用

### 4. 用户体验
- 提供清晰的提示信息
- 支持快捷操作
- 给出安装指导