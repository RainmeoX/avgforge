---
name: Pull Request 模板
about: 向 AVGForge 提交变更
---

## 描述

简要描述此 PR 的变更内容和原因。

## 变更类型

- [ ] Bug 修复（非破坏性变更，修复问题）
- [ ] 新功能（非破坏性变更，添加功能）
- [ ] 破坏性变更（修复或功能会导致现有功能不按预期工作）
- [ ] 文档更新
- [ ] 重构（无功能变更）
- [ ] 性能改进
- [ ] 测试覆盖改进

## 相关 Issue

Closes #(issue 编号)
Refs #(issue 编号)

## 变更内容

- 变更 1
- 变更 2
- 变更 3

## 测试

- [ ] 所有现有测试通过
- [ ] 为新功能添加了新测试
- [ ] 完成手动测试
- [ ] 测试平台：[Linux / macOS / Windows]

### 运行的测试命令

```bash
python3 src/avgforge/__main__.py --version
python3 src/avgforge/__main__.py init test-pr --template blank
python3 src/avgforge/__main__.py check test-pr
```

## 检查清单

- [ ] 我的代码遵循项目风格指南
- [ ] 我已对代码进行自审
- [ ] 我已为代码添加注释，特别是难以理解的部分
- [ ] 我已对文档进行相应更新
- [ ] 我的变更未产生新警告
- [ ] 我已添加证明修复有效或功能正常的测试
- [ ] 新增和现有单元测试在本地通过
- [ ] 任何依赖变更已合并并发布

## 许可证

提交此 Pull Request 即表示我确认我的贡献以 [AVGForge 双许可（AGPL-3.0 + 商业）](LICENSE)授权。

## 截图/输出

（如适用，添加截图或命令输出以帮助解释变更）
