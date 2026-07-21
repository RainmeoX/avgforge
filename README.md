<div align="center">

# ⚒️ AVGForge

### 企业级视觉小说开发流水线

**跨平台 CLI 引擎，用于专业互动叙事内容生产**

[![许可证: AGPL v3 + 商业](https://img.shields.io/badge/许可证-AGPL%20v3%20%2F%20商业-blue.svg)](LICENSE)
[![版本](https://img.shields.io/badge/版本-1.0.0--enterprise-6c5ce7.svg)](CHANGELOG.md)
[![平台](https://img.shields.io/badge/平台-Linux%20%7C%20macOS%20%7C%20Windows-00b894.svg)](#系统要求)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab.svg)](https://www.python.org/)
[![构建状态](https://img.shields.io/badge/构建-通过-success.svg)](.github/workflows/ci.yml)

</div>

---

## 概述

**AVGForge** 是一个无头、Git 原生的视觉小说（VN）和互动叙事内容创作流水线。专为需要**确定性构建**、**CI/CD 集成**和**可复现产物生成**的工作室设计，无需依赖 GUI。

与传统的 VN 编辑器将工作流锁定在单一桌面应用中不同，AVGForge 将项目视为**结构化数据**——每个素材、角色、场景和剧本块都是可版本化、可 diff 的 JSON 文档。这使得团队协作、自动化测试和流水线集成成为可能，而这些是纯 GUI 工具无法实现的。

### 为什么选择 AVGForge？

| 痛点 | 传统工具 | AVGForge |
|---|---|---|
| 团队协作 | 二进制项目文件，无法合并 | JSON 文本，Git 原生合并 |
| CI/CD 集成 | 必须打开 GUI 才能构建 | 命令行一键构建 |
| 自动化测试 | 无法脚本化验证 | `avgforge check` 程序化验证 |
| 批量编辑 | 手动逐个修改 | 脚本批量操作 JSON |
| 版本控制 | 整个文件变更，难以审查 | 逐行 diff，精确追踪 |
| 服务器部署 | 必须桌面环境 | 无头运行，云端友好 |

### 核心设计原则

1. **CLI 优先** — 所有功能通过命令行访问，可脚本化
2. **Git 原生** — 项目格式为可读 JSON，天然支持版本控制
3. **LetsGal 兼容** — 生成的项目可直接导入 LetsGal Studio 预览
4. **确定性构建** — 相同输入产生相同输出，支持复现
5. **可扩展** — 插件架构支持自定义 block 和渲染器

---

## 快速开始

```bash
# 1. 安装
git clone https://github.com/RainmeoX/avgforge.git
cd avgforge
chmod +x avgforge

# 2. 创建项目
./avgforge init my-game --name "我的游戏"

# 3. 添加角色和场景
cd my-game
./avgforge char add "女主角" --pos right --color-ring "#ffb6d9"
./avgforge scene add "教室" --layer "bg:1:backgrounds/classroom.png"

# 4. 编辑剧本（Ren'Py 风格）
./avgforge edit 开始/main

# 5. 预览
./avgforge preview text 开始

# 6. 导入 LetsGal Studio 预览
#    打开 LetsGal Studio → 打开项目 → 选择 my-game 文件夹 → F5 运行
```

📖 **完整使用指南：** [`docs/USAGE.md`](docs/USAGE.md)

---

## 功能特性

### ✅ 完全实现（80% 覆盖）

| 功能 | 命令 | 说明 |
|------|------|------|
| 项目创建 | `avgforge init` | 标准 LetsGal 项目结构 |
| 项目信息 | `avgforge info` | 统计与概览 |
| 角色管理 | `avgforge char` | 5 位置 + themeColor + 表情 |
| 场景管理 | `avgforge scene` | 多层视差背景 |
| 章节管理 | `avgforge chapter` | 增删改查、排序 |
| 片段管理 | `avgforge frag` | Fragment 子单元 |
| Block 编辑 | `avgforge block` | 25 种 block 类型 |
| 变量管理 | `avgforge var` | 布尔/数值/文本 × Slot/Shared |
| Ren'Py 编辑 | `avgforge edit` | `$EDITOR` 集成 |
| 素材管理 | `avgforge asset` | 引用检查 |
| 项目验证 | `avgforge check` | 完整性检查 |
| 文本预览 | `avgforge preview text` | 终端渲染剧本 |
| 流程图 | `avgforge preview graph` | Mermaid 分支图 |
| 项目统计 | `avgforge preview stats` | 详细统计 |

### ⚠️ 部分实现（预览交给 LetsGal Studio）

| 功能 | 说明 |
|------|------|
| 可视化预览 | 导入 LetsGal Studio，按 F5 运行 |
| 实时联动预览 | 使用 LetsGal Studio GUI |
| 打包发布 | 使用 LetsGal Studio "发布游戏" |
| 扩展开发 | 使用 LetsGal Studio 扩展 SDK |

### LetsGal Studio 兼容性

AVGForge 生成的项目**完全兼容 LetsGal Studio**，可直接导入预览：

- ✅ `project.json` 格式兼容
- ✅ `characters.json` 格式兼容
- ✅ `scenes.json` 格式兼容
- ✅ `chapters/*.json` 格式兼容
- ✅ 25 种 Block 类型全支持
- ✅ 默认游戏壳（`avg.internal.default-shell`）
- ✅ 系统绑定与快捷键

---

## 命令参考

```
avgforge <命令> [子命令] [选项]

项目管理
  init <路径>              创建新项目
  info                     显示项目信息
  check                    验证项目完整性

角色管理
  char list                列出所有角色
  char add <名称>          添加角色
  char remove <名称>       删除角色

场景管理
  scene list               列出所有场景
  scene add <名称>         添加场景
  scene remove <名称>      删除场景

章节与片段
  chapter list             列出章节
  chapter add <名称>       添加章节
  chapter remove <名称>    删除章节
  frag list <章节>         列出章节内片段
  frag add <章节> <名称>   添加片段

剧本编辑
  edit <章节>/<片段>       打开 Ren'Py 风格编辑器（$EDITOR）
  edit <章节>/<片段> --file <路径>  从文件导入
  block list <片段>        列出片段内 block
  block add <片段> <类型>  添加 block
  block remove <片段> <id> 删除 block

变量管理
  var list                 列出所有变量
  var add <key> <显示名>   添加变量
  var remove <key>         删除变量

素材管理
  asset list               列出所有素材
  asset refs <素材>        查看素材引用

预览
  preview text <章节>      文本预览
  preview graph            Mermaid 流程图
  preview stats            项目统计
```

---

## 示例项目

`examples/star-orbit-vow/` — 完整的 5 章视觉小说示例：

- **2 个角色**：星野 + 我
- **6 个场景**：教室/天台/星轨观测站/3 个结局
- **5 个变量**：信任度/回忆数/是否约定/已解锁结局/游玩次数
- **5 个章节 / 15 个片段 / 104 个 block**
- **3 种结局**：真结局/普通结局/Bad End
- **分支选项**：3 个关键抉择点

```bash
cd examples/star-orbit-vow
./avgforge info
./avgforge preview text 开始
./avgforge preview graph
```

---

## 系统要求

| 组件 | 要求 |
|------|------|
| 操作系统 | Linux x64 / macOS 11+ / Windows 10+ |
| Python | 3.9 或更高 |
| Git | 2.20 或更高（推荐） |
| LetsGal Studio | 1.8.0+（用于可视化预览） |
| 浏览器 | Chrome 90+ / Firefox 88+ / Safari 14+（用于流程图查看） |

---

## 项目结构

```
avgforge/
├── avgforge                 # CLI 入口脚本
├── src/avgforge/            # 核心源码
│   ├── __main__.py          # CLI 命令解析
│   ├── schema.py            # LetsGal 格式定义
│   ├── project.py           # 项目操作类
│   ├── renpy_parser.py      # Ren'Py 解析器
│   └── preview.py           # 预览模块
├── examples/                # 示例项目
│   └── star-orbit-vow/      # 《星轨之约》完整示例
├── docs/                    # 文档
│   └── USAGE.md             # 使用指南
├── scripts/                 # 辅助脚本
└── game_data/               # LetsGal 官方模板（仅供学习）
```

---

## 开发工作流

### 典型开发流程

```bash
# 1. 创建项目
avgforge init my-game --name "我的游戏"
cd my-game

# 2. 配置角色
avgforge char add "女主角" --pos right --color-ring "#ffb6d9"
avgforge char add "男主角" --pos left --color-ring "#7fc8f8"

# 3. 配置场景
avgforge scene add "教室" --layer "bg:1:backgrounds/classroom.png"
avgforge scene add "天台" --layer "bg:1:backgrounds/rooftop.png"

# 4. 定义变量
avgforge var add affection "好感度" --type number --scope project --persistence slot

# 5. 添加章节
avgforge chapter add "序章"
avgforge chapter add "第一章"
avgforge chapter add "终章"

# 6. 编辑剧本
avgforge edit 序章/main
# 在编辑器中写 Ren'Py 风格剧本

# 7. 验证项目
avgforge check

# 8. 文本预览
avgforge preview text 序章

# 9. 生成流程图
avgforge preview graph

# 10. 导入 LetsGal Studio 可视化预览
#     打开 LetsGal Studio → 打开项目 → 选择 my-game → F5 运行
```

### Git 版本控制

```bash
git init
git add -A
git commit -m "feat: 初始化项目"

# 每次编辑后
git add -A
git commit -m "feat: 完成序章剧本"
git push
```

---

## Ren'Py 语法示例

```renpy
# 场景切换
scene 教室 with fade duration 0.5

# 显示角色
show 星野 at right

# 对白
星野 "你好。"
我 "你好，星野。"

# 旁白
"夕阳洒进教室，将一切染成金色。"

# 分支
menu "怎么回答":
    "打招呼" -> call 问候分支
    "保持沉默" -> $ trust -= 1

# 变量赋值
$ trust += 1

# 等待
pause 1.0

# 播放音乐
play music bgm/主题曲.mp3 loop

# 隐藏角色
hide 星野
```

---

## 路线图

### v1.0（当前）
- ✅ 核心 CLI 命令
- ✅ LetsGal 格式兼容
- ✅ Ren'Py 解析器
- ✅ 文本预览
- ✅ Mermaid 流程图

### v1.1（计划中）
- 📋 Web 预览引擎（浏览器内运行）
- 📋 HTML 单文件打包
- 📋 项目模板系统

### v1.2（规划中）
- 📋 扩展 SDK
- 📋 自定义 block 类型
- 📋 多语言支持

### v2.0（远期）
- 📋 移动端构建（React Native / Capacitor）

---

## 企业支持

为企业客户提供：

- **优先 SLA** — 7×24 小时关键问题响应
- **定制功能开发** — 定制 block、渲染器、集成
- **私有部署** — 气隙环境安装支持
- **培训与入职** — 团队工作坊和最佳实践
- **审计与合规** — SOC2 / ISO27001 文档包

**联系：** `enterprise@avgforge.example`

---

## 贡献

欢迎社区贡献。提交 Pull Request 前请阅读[贡献指南](CONTRIBUTING.md)。

### 贡献者

<div align="center">

用 ⚒️ 由 AVGForge 团队制作

</div>

---

## 安全

发现安全漏洞？请查看[安全策略](SECURITY.md)并负责任地报告。

---

## 致谢

AVGForge 的架构设计借鉴了行业标准视觉小说引擎和现代 CLI 工具。我们感谢开源社区的基础性工作。

- 项目格式兼容 [LetsGal Studio](https://avg-engine.com/) 项目文件
- Ren'Py 语法受 [Ren'Py 视觉小说引擎](https://www.renpy.org/) 启发
- Web 预览引擎基于标准 Web API 构建

---

<div align="center">

**文档：** [docs/USAGE.md](docs/USAGE.md) · **更新日志：** [CHANGELOG.md](CHANGELOG.md) · **许可证：** [双许可 AGPL + 商业](LICENSE)

</div>
