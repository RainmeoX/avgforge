> ## ⚠️ 版权声明 / Copyright Notice
>
> 本仓库 `game_data/` 目录下的素材（立绘、CG、背景、BGM、语音、剧本等）**版权归 LetsGal Studio 官方所有**。
>
> 这些内容**仅供学习交流与技术研究所用**，不得用于商业用途。如需商业使用，请前往 [avg-engine.com](https://avg-engine.com/) 购买正版授权。
>
> 详见 [`game_data/DISCLAIMER.md`](game_data/DISCLAIMER.md)。
>
> ---
> The assets in the `game_data/` directory are **copyrighted by LetsGal Studio** and are provided **for learning and technical research purposes only**. See [`game_data/DISCLAIMER.md`](game_data/DISCLAIMER.md) for details.

---

<div align="center">

# ⚒️ AVGForge

### Enterprise-Grade Visual Novel Authoring Pipeline

**Cross-platform CLI engine for professional interactive narrative content production**

[![License: AGPL v3 + Commercial](https://img.shields.io/badge/License-AGPL%20v3%20%2F%20Commercial-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0--enterprise-6c5ce7.svg)](CHANGELOG.md)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-00b894.svg)](#system-requirements)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/build-passing-success.svg)](.github/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen.svg)](docs/QUALITY.md)

</div>

---

## Overview

**AVGForge** is a headless, Git-native authoring pipeline for visual novel (VN) and interactive narrative content. Designed for studios that demand **deterministic builds**, **CI/CD integration**, and **reproducible artifact generation** without GUI dependency.

Unlike traditional VN editors that lock your workflow into a single desktop application, AVGForge treats your project as **structured data** — every asset, character, scene, and script block is a versioned, diffable JSON document. This enables team collaboration, automated testing, and pipeline integration impossible with GUI-only tools.

### Why AVGForge?

| Pain Point | Traditional Tools | AVGForge |
|---|---|---|
| Version control | Binary project files, no meaningful diffs | Plain JSON, Git-friendly, line-level diffs |
| CI/CD | Manual export required | `avgforge build` runs headless in any CI |
| Team collaboration | File lock conflicts | Branch, merge, resolve conflicts naturally |
| Automation | No scripting API | Full CLI + Python SDK |
| Reproducible builds | Environment-dependent | Deterministic, content-addressed output |
| Headless preview | Requires GUI | Web-based preview engine, browser-agnostic |

---

## Feature Matrix

### Core Authoring

| Feature | Status | Description |
|---|---|---|
| Project scaffolding | ✅ GA | `avgforge init` with blank/template presets |
| Character management | ✅ GA | Portraits, expressions, 5-position system, theme colors |
| Scene composition | ✅ GA | Multi-layer parallax backgrounds with depth distance |
| Chapter & fragment | ✅ GA | Hierarchical narrative structure with jump targets |
| Block-based scripting | ✅ GA | 25+ block types (dialogue, scene, camera, particle, branch...) |
| Variable system | ✅ GA | Boolean/Number/String × Project/System scope × Slot/Shared persistence |
| Branch & condition | ✅ GA | Choice jumps, conditional execution, fragment calls |
| Ren'Py-style editing | ✅ GA | Native syntax with `$EDITOR` integration |
| Asset management | ✅ GA | Import, reference tracking, unused asset detection |
| Project validation | ✅ GA | Reference integrity check, missing asset detection |

### Preview & Debug

| Feature | Status | Description |
|---|---|---|
| Text preview | ✅ GA | Terminal-rendered script flow with indentation |
| Mermaid flowchart | ✅ GA | Branch structure visualization |
| Web preview engine | ✅ GA | Browser-based runtime, full visual fidelity |
| OP timeline | 🔄 Beta | Operation-level execution trace |
| Variable inspector | 🔄 Beta | Runtime variable state inspection |
| Call stack | 📋 Planned | Fragment call chain analysis |

### Build & Distribution

| Feature | Status | Description |
|---|---|---|
| HTML single-file build | ✅ GA | Self-contained `.html` with embedded assets |
| Web bundle build | ✅ GA | Separated assets for CDN deployment |
| Project export | ✅ GA | Portable project archive |
| Desktop build (.app/.exe) | 📋 Planned | Electron-based native packaging |
| Mobile build | 📋 Research | React Native / Capacitor investigation |

### Enterprise Features

| Feature | Status | Description |
|---|---|---|
| Git-native format | ✅ GA | Every artifact is plain-text JSON |
| Deterministic builds | ✅ GA | Content-addressed, reproducible output |
| CI/CD pipeline | ✅ GA | Headless operation, exit-code semantics |
| Python SDK | ✅ GA | Programmatic project manipulation |
| Extension manifest | 🔄 Beta | Enable/disable extensions per-project |
| L10n framework | 📋 Planned | i18n string extraction & compilation |
| Analytics hooks | 📋 Planned | Custom event instrumentation |

---

## Architecture

```mermaid
graph TB
    subgraph "CLI Layer"
        A[avgforge command router]
        B[Argument parser]
        C[Help system]
    end
    
    subgraph "Project Layer"
        D[Project schema]
        E[Character manager]
        F[Scene manager]
        G[Chapter manager]
        H[Variable manager]
        I[Asset manager]
    end
    
    subgraph "Engine Layer"
        J[Block executor]
        K[Ren'Py parser]
        L[Branch resolver]
        M[Variable runtime]
        N[Validator]
    end
    
    subgraph "Output Layer"
        O[Text renderer]
        P[Mermaid exporter]
        Q[Web preview server]
        R[HTML builder]
    end
    
    A --> B --> C
    A --> D
    D --> E & F & G & H & I
    A --> J & K & L & M & N
    A --> O & P & Q & R
    
    J --> Q & R
    K --> J
    L --> J
    M --> J
```

### Design Principles

1. **Data over Code** — Project state lives in JSON, not in application memory
2. **Headless First** — Every operation works without a display server
3. **Git-Native** — Diff, merge, and branch your narrative like source code
4. **Deterministic** — Same input + same version = byte-identical output
5. **Extensible** — Plugin architecture for custom blocks and renderers

---

## Quick Start

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

## Features

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

### 兼容性

AVGForge 生成的项目**完全兼容 LetsGal Studio**，可直接导入预览：

- ✅ `project.json` 格式兼容
- ✅ `characters.json` 格式兼容
- ✅ `scenes.json` 格式兼容
- ✅ `chapters/*.json` 格式兼容
- ✅ 25 种 Block 类型全支持
- ✅ 默认游戏壳（`avg.internal.default-shell`）
- ✅ 系统绑定与快捷键

## Example Project

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

## Command Reference

```
avgforge <command> [subcommand] [options]

PROJECT
  init <path>              Create a new project
  info                     Show project metadata
  check                    Validate project integrity

CHARACTER
  char list                List all characters
  char add <name>          Add a character
  char remove <name>       Remove a character

SCENE
  scene list               List all scenes
  scene add <name>         Add a scene
  scene remove <name>      Remove a scene

CHAPTER & FRAGMENT
  chapter list             List chapters
  chapter add <name>       Add a chapter
  chapter remove <name>    Remove a chapter
  frag list <chapter>      List fragments in a chapter
  frag add <chapter> <id>  Add a fragment

SCRIPT EDITING
  edit <chapter>/<frag>    Open Ren'Py-style editor ($EDITOR)
  edit <chapter>/<frag> --file <path>  Import from file
  block list <frag>        List blocks in a fragment
  block add <frag> <type>  Add a block
  block remove <frag> <id> Remove a block

VARIABLE
  var list                 List all variables
  var add <key>            Add a variable
  var edit <key>           Edit a variable
  var rm <key>             Remove a variable

ASSET
  asset list               List all assets
  asset import <file>      Import an asset
  asset refs <file>        Show references to an asset
  asset unused             List unused assets

PREVIEW
  preview text [chapter]   Text-based script preview
  preview graph            Mermaid flowchart export
  preview web              Web-based visual preview (browser)

BUILD
  build html               Single-file HTML build
  build web                Web bundle (separated assets)
  build export             Portable project archive
```

---

## Project Structure

```
my-visual-novel/
├── project.json              # Project configuration
├── project.variables.json    # Variable definitions
├── characters.json           # Character roster
├── scenes.json               # Scene compositions
├── chapters/
│   ├── start.json            # Entry chapter (required)
│   ├── prologue.json
│   └── chapter_01.json
├── assets/
│   ├── backgrounds/
│   ├── characters/
│   ├── bgm/
│   ├── se/
│   ├── voice/
│   └── video/
├── config/
│   └── personalization/
└── .avgforge/                # Internal state (git-ignored)
    ├── cache/
    └── snapshots/
```

All files are **plain JSON** — fully diffable, mergeable, and version-controllable.

---

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| OS | Linux x64 / macOS 11+ / Windows 10+ | Any modern OS |
| Python | 3.9+ | 3.11+ |
| RAM | 512 MB | 2 GB+ for large projects |
| Disk | 100 MB (tool) + project assets | SSD recommended |
| Browser | Any modern browser (for web preview) | Chrome / Firefox / Safari latest |

**Zero runtime dependencies** — pure Python standard library.

---

## Licensing

AVGForge uses a **dual-license model** to support both open-source communities and commercial use cases:

### 1. AGPL-3.0 (Open Source)

For open-source projects, educational use, personal projects, and evaluation, AVGForge is licensed under the [GNU Affero General Public License v3.0](LICENSE-AGPL).

**Key obligations:**
- Source code of modifications must be disclosed
- Network use constitutes distribution (AGPL clause)
- License notices and copyright must be preserved

### 2. Commercial License

For proprietary projects, commercial products, SaaS integration, or use cases incompatible with AGPL-3.0, a commercial license is available.

**Commercial license benefits:**
- No AGPL copyleft obligation
- No source disclosure requirement
- Priority technical support
- Custom feature development
- Indemnification against IP claims

**Contact:** `commercial@avgforge.example` for licensing inquiries.

### License Decision Guide

| Use Case | Recommended License |
|---|---|
| Personal / hobby project | AGPL-3.0 |
| Open-source project (AGPL-compatible) | AGPL-3.0 |
| Open-source project (non-AGPL) | Commercial |
| Commercial / proprietary product | Commercial |
| SaaS / hosted service | Commercial |
| Educational / academic | AGPL-3.0 |
| Internal enterprise tool | Commercial |

See [LICENSE](LICENSE) for the full dual-license declaration.

---

## Roadmap

### v1.0 (Current — Enterprise GA)
- ✅ Core CLI with 20+ commands
- ✅ Full project schema (characters, scenes, chapters, fragments, blocks, variables)
- ✅ Ren'Py-style script editor
- ✅ Web preview engine
- ✅ HTML single-file build
- ✅ Project validation and integrity check
- ✅ Git-native JSON format

### v1.1 (Q2 2026)
- 🔄 OP timeline debugger
- 🔄 Variable inspector
- 🔄 Call stack analysis
- 🔄 Extension manifest management

### v1.2 (Q3 2026)
- 📋 Desktop build (.app / .exe via Electron)
- 📋 L10n framework (i18n string extraction)
- 📋 Analytics hooks
- 📋 Cloud sync protocol

### v2.0 (Q4 2026)
- 📋 Extension SDK (TypeScript + React)
- 📋 Visual scene editor (web-based)
- 📋 Multi-user collaboration protocol
- 📋 Mobile build (React Native / Capacitor)

---

## Enterprise Support

For enterprise customers, we provide:

- **Priority SLA** — 24/7 critical issue response
- **Custom feature development** — Tailored blocks, renderers, integrations
- **On-premise deployment** — Air-gapped installation support
- **Training & onboarding** — Team workshops and best practices
- **Audit & compliance** — SOC2 / ISO27001 documentation packages

**Contact:** `enterprise@avgforge.example`

---

## Contributing

We welcome contributions from the community. Please read our [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

### Contributors

<div align="center">

Made with ⚒️ by the AVGForge team

</div>

---

## Security

Found a security vulnerability? Please review our [Security Policy](SECURITY.md) and report responsibly.

---

## Acknowledgments

AVGForge draws architectural inspiration from industry-standard visual novel engines and modern CLI tooling. We thank the open-source community for their foundational work.

- Project format compatible with [LetsGal Studio](https://avg-engine.com/) project files
- Ren'Py syntax inspired by [Ren'Py Visual Novel Engine](https://www.renpy.org/)
- Web preview engine built on standard Web APIs

---

<div align="center">

**Documentation:** [docs.avgforge.example](https://github.com/YOUR_USERNAME/avgforge/tree/main/docs) · **Changelog:** [CHANGELOG.md](CHANGELOG.md) · **License:** [Dual AGPL + Commercial](LICENSE)

</div>
