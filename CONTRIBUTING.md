# 贡献指南

首先感谢您考虑为 AVGForge 贡献代码！🎉

本文档概述了我们的贡献流程和标准。

## 行为准则

参与本项目即表示您同意遵守我们的[行为准则](CODE_OF_CONDUCT.md)。请在所有互动中保持尊重和专业。

## 入门

### 前置要求

- Python 3.9 或更高
- Git 2.20 或更高
- 现代网页浏览器（用于测试 Web 预览）
- 支持 JSON 的文本编辑器（推荐 VS Code）

### 开发环境搭建

```bash
# Fork 并克隆仓库
git clone https://github.com/YOUR_USERNAME/avgforge.git
cd avgforge

# 创建虚拟环境（可选但推荐）
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或：.venv\Scripts\activate  # Windows

# 验证安装
python3 src/avgforge/__main__.py --version

# 运行测试
python3 -m pytest tests/  # （测试套件可用时）
```

## 如何贡献

### 报告 Bug

创建 Bug 报告前，请：
1. 检查[现有 issue](https://github.com/RainmeoX/avgforge/issues)避免重复
2. 验证 Bug 在最新 `main` 分支存在
3. 收集以下信息：
   - 操作系统和版本
   - Python 版本
   - AVGForge 版本（`avgforge --version`）
   - 最小复现步骤
   - 预期与实际行为

使用 [Bug 报告模板](.github/ISSUE_TEMPLATE/bug_report.md)。

### 建议新功能

功能建议应包含：
- 功能摘要
- 解决的问题
- 提议的解决方案
- 替代方案
- 使用场景

使用 [功能请求模板](.github/ISSUE_TEMPLATE/feature_request.md)。

### 提交代码

1. **Fork 仓库**
2. **创建功能分支**：`git checkout -b feat/your-feature`
3. **编写代码**，遵循项目风格
4. **测试**：确保 `avgforge check` 通过
5. **提交**：使用规范的提交信息
6. **推送**：`git push origin feat/your-feature`
7. **创建 Pull Request**

### 提交信息规范

```
<类型>: <描述>

[可选正文]

[可选脚注]
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `style`: 代码风格（不影响功能）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具变更

示例：
```
feat: 添加角色表情管理命令
fix: 修复场景切换时的内存泄漏
docs: 更新 Ren'Py 语法文档
```

## 代码风格

### Python 代码

- 遵循 PEP 8
- 行宽限制 100 字符
- 使用 4 空格缩进
- 函数和类添加 docstring
- 类型注解（Python 3.9+ 语法）

### 项目结构

```
src/avgforge/
├── __init__.py
├── __main__.py        # CLI 入口
├── schema.py          # 数据 schema
├── project.py         # 项目操作
├── renpy_parser.py    # Ren'Py 解析器
├── preview.py         # 预览功能
└── commands/          # 命令实现（未来拆分）
```

## 测试

### 手动测试清单

提交 PR 前，验证：

- [ ] `avgforge --version` 正常
- [ ] `avgforge init test-project` 创建有效项目
- [ ] `avgforge char add` / `scene add` / `chapter add` 正常
- [ ] `avgforge edit` 打开 `$EDITOR`
- [ ] `avgforge preview text` 正确渲染
- [ ] `avgforge check` 在有效项目上无错误

### 测试项目

使用 `examples/` 目录的测试项目：
- `examples/star-orbit-vow/` — 完整功能演示项目

## 许可证

贡献即表示您同意您的贡献将以[AGPL-3.0 + 商业双许可](LICENSE)授权。详见[贡献者许可协议](LICENSE)部分。

## 有问题？

- 💬 [GitHub Discussions](https://github.com/RainmeoX/avgforge/discussions)
- 📧 邮箱：`community@avgforge.example`

感谢您的贡献！⚒️
