# AVGForge

一个面向视觉小说创作流程管理的 CLI 工具实验。

## 动机

传统视觉小说工具基本是 GUI，不方便版本管理。我尝试做一个 Git 友好的项目管理工具：把角色、场景、剧本都变成可 diff、可合并的 JSON 文档，而不是锁死在一个二进制工程文件里。

## 当前实现

- 项目初始化（`avgforge init`）
- 角色管理（位置 / 主题色 / 表情）
- 场景管理（多层背景）
- 章节 / 片段管理
- 剧本编辑（Ren'Py 风格，配合 `$EDITOR`）
- 项目校验（`avgforge check`）
- 文本预览 / Mermaid 流程图预览
- 全部数据以 JSON 格式存储

## 与 LetsGal Studio 的关系

生成的项目格式兼容 [LetsGal Studio](https://avg-engine.com/)，可以导入做可视化预览和打包发布。这是当前"可视化"这一步的承接方案。

## 技术栈

- Python 3.9+
- 无第三方重依赖，CLI 优先，可脚本化

## 命令示例

```bash
./avgforge init my-game --name "我的游戏"
./avgforge char add "女主角" --pos right --color-ring "#ffb6d9"
./avgforge scene add "教室" --layer "bg:1:backgrounds/classroom.png"
./avgforge check
./avgforge preview text 序章
./avgforge preview graph
```

`examples/star-orbit-vow/` 里有一个完整的 5 章示例项目（2 角色 / 6 场景 / 5 章节 / 15 片段 / 104 block / 3 结局），可以直接 `avgforge info` 和 `preview` 看效果。

## 当前限制（重要，先看这个）

- **没有完整渲染引擎**：可视化预览依赖 LetsGal Studio，本工具只负责"写"和"管"
- 实时联动预览交给了第三方 GUI
- 仍处于原型阶段，命令 / 数据格式可能变动
- 没有写自动化测试

## 后续计划

- Web 预览引擎（浏览器内运行，减少对第三方 GUI 的依赖）
- 项目模板系统
- 补测试

## Reflection

做这个工具让我想清楚一件事：好的工程工具不是功能最多，而是和现有工作流（这里是 Git）契合。它现在不完美，渲染要靠外部，但"把叙事工程化、可版本化"这个方向我觉得是对的。

## License

AGPL v3。原仓库曾标注"AGPL v3 + 商业"双许可；作为个人实验仓库，这里统一以 AGPL v3 为准。如果有商业使用需求，请单独联系作者确认授权。
