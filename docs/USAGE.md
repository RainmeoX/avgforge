# AVGForge 使用指南

> 完整的 galgame 开发工作流：从项目创建到导入 LetsGal Studio 预览

## 目录

1. [安装](#安装)
2. [快速开始](#快速开始)
3. [完整开发流程](#完整开发流程)
4. [命令参考](#命令参考)
5. [Ren'Py 语法](#renpy-语法)
6. [导入 LetsGal Studio 预览](#导入-letsgal-studio-预览)
7. [常见问题](#常见问题)

---

## 安装

### 系统要求

- Python 3.9+
- LetsGal Studio 1.8.0+（用于预览）

### 安装 AVGForge

```bash
git clone https://github.com/RainmeoX/avgforge.git
cd avgforge
chmod +x avgforge

# 验证安装
./avgforge --version
```

### 设置环境变量（可选）

```bash
# 添加到 PATH
export PATH="$PATH:$(pwd)"

# 设置默认编辑器（用于 edit 命令）
export EDITOR=vim  # 或 code, nano 等
```

---

## 快速开始

5 分钟创建一个可运行的 galgame 项目：

```bash
# 1. 创建项目
avgforge init my-game --name "我的游戏"

# 2. 添加角色
cd my-game
avgforge char add "女主角" --pos right --color-ring "#ffb6d9"
avgforge char add "我" --pos left --color-ring "#7fc8f8"

# 3. 添加场景
avgforge scene add "教室" --layer "bg:1:backgrounds/classroom.png"

# 4. 编辑剧本
avgforge edit 开始/main
# 在编辑器中写：
# scene 教室 with fade
# show 女主角 at right
# 女主角 "你好！"
# 我 "你好。"

# 5. 预览
avgforge preview text 开始

# 6. 导入 LetsGal Studio 预览（见下文）
```

---

## 完整开发流程

### 第 1 步：创建项目

```bash
avgforge init my-game \
    --name "游戏名称" \
    --author "作者名" \
    --description "游戏描述"
```

生成标准项目结构：

```
my-game/
├── project.json              # 项目配置
├── project.variables.json    # 变量定义
├── characters.json           # 角色配置
├── scenes.json               # 场景配置
├── chapters/
│   └── 开始.json             # 入口章节
├── assets/                   # 素材目录
│   ├── backgrounds/
│   ├── characters/
│   ├── bgm/
│   ├── se/
│   ├── voice/
│   └── video/
├── extensions/
│   └── avg.internal.default-shell/
└── config/
    └── personalization/
```

### 第 2 步：添加角色

```bash
# 添加女主角（右侧位置，粉色主题）
avgforge char add "星野" \
    --pos right \
    --color-ring "#ffb6d9" \
    --color-bg "#ffe4e6" \
    --color-fg "#9f1239"

# 添加男主角（左侧位置，蓝色主题）
avgforge char add "我" \
    --pos left \
    --color-ring "#7fc8f8" \
    --color-bg "#dbeafe" \
    --color-fg "#1e40af"

# 查看角色列表
avgforge char list
```

**5 个位置可选**：`left` / `center-left` / `center` / `center-right` / `right`

### 第 3 步：添加场景

```bash
# 单层场景
avgforge scene add "教室" \
    --layer "bg:1:backgrounds/classroom.png"

# 多层视差场景（推荐）
avgforge scene add "天台" \
    --layer "天空:14:backgrounds/rooftop/sky.png" \
    --layer "城市:7:backgrounds/rooftop/city.png" \
    --layer "天台:2:backgrounds/rooftop/floor.png"

# 查看场景列表
avgforge scene list
```

**图层格式**：`<名称>:<distance>:<素材路径>`
- `distance` 越大越远（视差效果越慢）
- 典型值：天空 14 / 远景 7 / 中景 3.5 / 近景 2

### 第 4 步：添加变量

```bash
# 数值变量（存档绑定）
avgforge var add trust "信任度" \
    --type number \
    --scope project \
    --persistence slot \
    --default 0 \
    --description "角色信任度"

# 布尔变量
avgforge var add promised "是否约定" \
    --type boolean \
    --scope project \
    --persistence slot \
    --default false

# 跨周目共享变量（成就系统）
avgforge var add endings_unlocked "已解锁结局" \
    --type string \
    --scope project \
    --persistence shared \
    --default ""

# 查看变量列表
avgforge var list
```

**变量维度**：
- 类型：`boolean` / `number` / `string`
- 作用域：`project`（自定义）/ `system`（引擎注入）
- 持久化：`slot`（跟存档）/ `shared`（跨存档）

### 第 5 步：添加章节

```bash
# 添加章节
avgforge chapter add "序章"
avgforge chapter add "第一章"
avgforge chapter add "终章"

# 查看章节列表
avgforge chapter list
```

**注意**：`开始` 章节是固定入口，不能删除。

### 第 6 步：添加分支片段

```bash
# 在章节中添加片段
avgforge frag add "第一章" "选项A"
avgforge frag add "第一章" "选项B"
avgforge frag add "终章" "真结局"
avgforge frag add "终章" "普通结局"
avgforge frag add "终章" "Bad_End"

# 查看片段列表
avgforge frag list
```

### 第 7 步：编辑剧本

#### 方式 A：用 $EDITOR 编辑（推荐）

```bash
# 设置编辑器
export EDITOR=code  # VS Code

# 编辑片段
avgforge edit 开始/main
avgforge edit "第一章/选项A"
```

#### 方式 B：从文件导入

```bash
# 写剧本到文件
cat > script.rpy << 'EOF'
scene 教室 with fade
show 星野 at right
星野 "你好。"
我 "你好，星野。"
menu "怎么回答":
    "好啊" -> call 选项A
    "不要" -> call 选项B
EOF

# 导入到片段
avgforge edit 开始/main --file script.rpy
```

### 第 8 步：预览

#### 文本预览（快速检查）

```bash
avgforge preview text 开始
```

输出示例：
```
============================================================
  📖 开始
============================================================

  ── 片段: main ──

  🎬 [场景切换] → 教室
  【星野】你好。
  【我】你好，星野。

  🔀 [分支] 怎么回答
     1. 好啊
     2. 不要
```

#### Mermaid 流程图（检查分支结构）

```bash
avgforge preview graph
# 生成 project_graph.mmd
# 用 VS Code Mermaid 插件或 https://mermaid.live 查看
```

#### 项目统计

```bash
avgforge preview stats
```

### 第 9 步：项目验证

```bash
avgforge check
```

检查：
- JSON 格式正确性
- 章节引用完整性
- Fragment 引用解析
- 素材文件存在性
- 变量引用一致性

### 第 10 步：导入 LetsGal Studio 预览

这是**最关键的一步**——用 LetsGal Studio 的完整 GUI 预览你用 CUI 创建的项目。

1. **打开 LetsGal Studio**
2. **选择"打开项目"**
3. **导航到你的项目文件夹**（包含 `project.json` 的目录）
4. **点击打开**

LetsGal Studio 会自动识别项目并加载：
- ✅ 角色和立绘
- ✅ 场景和图层
- ✅ 章节和剧本
- ✅ 变量系统
- ✅ 分支结构
- ✅ 默认游戏壳 UI

然后你可以：
- 按 **F5** 运行项目预览
- 用 **OP 时间轴** 调试
- 用 **变量观察** 检查状态
- 用 **属性检查器** 微调 Block 参数
- 用 **打包功能** 导出 .app/.exe

---

## 命令参考

### 全局命令

| 命令 | 说明 |
|---|---|
| `avgforge --version` | 显示版本 |
| `avgforge --help` | 显示帮助 |

### 项目管理

| 命令 | 说明 |
|---|---|
| `avgforge init <path> [--name NAME] [--author AUTHOR] [--description DESC]` | 创建项目 |
| `avgforge info [--path PATH]` | 显示项目信息 |
| `avgforge check [--path PATH]` | 验证项目完整性 |

### 角色管理

| 命令 | 说明 |
|---|---|
| `avgforge char add <name> [--pos POS] [--color-ring HEX] [--color-bg HEX] [--color-fg HEX]` | 添加角色 |
| `avgforge char list` | 列出角色 |
| `avgforge char remove <name>` | 删除角色 |

### 场景管理

| 命令 | 说明 |
|---|---|
| `avgforge scene add <name> --layer <layer-spec> [--layer ...]` | 添加场景 |
| `avgforge scene list` | 列出场景 |
| `avgforge scene remove <name>` | 删除场景 |

**图层格式**：`<名称>:<distance>:<素材路径>`

### 章节管理

| 命令 | 说明 |
|---|---|
| `avgforge chapter add <name>` | 添加章节 |
| `avgforge chapter list` | 列出章节 |
| `avgforge chapter remove <name>` | 删除章节 |

### 片段管理

| 命令 | 说明 |
|---|---|
| `avgforge frag add <chapter> <name>` | 添加片段 |
| `avgforge frag list [--chapter CHAPTER]` | 列出片段 |
| `avgforge frag remove <chapter> <name>` | 删除片段 |

### 变量管理

| 命令 | 说明 |
|---|---|
| `avgforge var add <key> <name> [--type TYPE] [--scope SCOPE] [--persistence P] [--default V] [--description D]` | 添加变量 |
| `avgforge var list` | 列出变量 |
| `avgforge var remove <key>` | 删除变量 |

### 剧本编辑

| 命令 | 说明 |
|---|---|
| `avgforge edit <chapter/[frag]> [--file FILE]` | 编辑片段 |

### 预览

| 命令 | 说明 |
|---|---|
| `avgforge preview text <chapter>` | 文本预览 |
| `avgforge preview graph [--output FILE]` | Mermaid 流程图 |
| `avgforge preview stats` | 项目统计 |

---

## Ren'Py 语法

AVGForge 支持简化的 Ren'Py 风格语法，与官方 LetsGal Studio 兼容。

### 场景切换

```renpy
scene 教室 with fade
scene 天台 with fade duration 1.5
```

**过渡方式**：`fade` / `cover` / `dissolve`

### 角色显示

```renpy
show 星野 at right
show 星野 开心 at right
hide 星野
```

**位置**：`left` / `center-left` / `center` / `center-right` / `right`

### 对白

```renpy
星野 "你好。"
我 "你好，星野。"
```

### 旁白

```renpy
"毕业前 30 天。"
"教室里只剩下我一个人。"
```

### 音频

```renpy
play music bgm/theme.mp3
play music bgm/theme.mp3 volume 80% loop fadein 0.5
play sound se/door.mp3
stop music
```

### 等待

```renpy
pause 1.5
```

### 变量赋值

```renpy
$ trust += 5
$ trust -= 3
$ promised = true
$ memory_count += 10
```

**操作符**：`=` / `+=` / `-=` / `*=` / `/=`

### 分支

```renpy
menu "怎么回答":
    "好啊" -> call 选项A
    "不要" -> call 选项B
```

### 片段调用

```renpy
call 选项A
call 真结局
```

### 幕布

```renpy
curtain close duration 0
curtain open duration 1.5
```

### 注释

```renpy
# 这是注释
```

---

## 导入 LetsGal Studio 预览

AVGForge 生成的项目**完全兼容 LetsGal Studio 格式**，可以直接导入预览。

### 步骤

1. **用 AVGForge 创建并编辑项目**

```bash
avgforge init my-game --name "我的游戏"
cd my-game
# ... 添加角色、场景、剧本 ...
avgforge check  # 确保无错误
```

2. **打开 LetsGal Studio**

3. **选择"打开项目"**

4. **选择项目文件夹**（包含 `project.json` 的目录）

5. **LetsGal Studio 自动加载**

6. **按 F5 运行预览**

### 兼容性

| 功能 | 兼容性 |
|---|---|
| 项目配置（project.json） | ✅ 完全兼容 |
| 角色配置（characters.json） | ✅ 完全兼容 |
| 场景配置（scenes.json） | ✅ 完全兼容 |
| 章节剧本（chapters/*.json） | ✅ 完全兼容 |
| 变量系统 | ✅ 完全兼容 |
| Block 类型（25 种） | ✅ 完全兼容 |
| 默认游戏壳 | ✅ 完全兼容 |
| 系统绑定 | ✅ 完全兼容 |
| 快捷键绑定 | ✅ 完全兼容 |

### 注意事项

1. **素材文件**：AVGForge 不会生成图片/音频素材，你需要手动放入 `assets/` 目录
2. **立绘表情**：用 `avgforge char add` 添加角色后，需要手动添加立绘文件到 `assets/characters/`
3. **背景图**：场景引用的背景图需要手动准备
4. **扩展**：默认使用官方 `avg.internal.default-shell`，可在 LetsGal Studio 中替换

---

## 常见问题

### Q: 编辑器打不开？

设置 `EDITOR` 环境变量：
```bash
export EDITOR=code  # VS Code
export EDITOR=vim   # Vim
export EDITOR=nano  # Nano
```

### Q: 素材缺失警告？

`avgforge check` 报素材缺失是正常的——AVGForge 只生成项目结构，不生成素材文件。你需要手动准备图片/音频放入 `assets/` 目录。

### Q: 导入 LetsGal Studio 报错？

1. 运行 `avgforge check` 确保无错误
2. 检查 `project.json` 格式
3. 确保章节名没有特殊字符
4. 确保 `开始` 章节存在

### Q: Ren'Py 语法报错？

检查：
- 角色名是否已用 `char add` 添加
- 场景名是否已用 `scene add` 添加
- 分支跳转的片段是否已用 `frag add` 创建
- 变量是否已用 `var add` 定义

### Q: 如何打包成可运行的游戏？

用 LetsGal Studio 的"发布游戏"功能：
1. 导入项目
2. 点击"发布游戏"
3. 选择平台（macOS / Windows）
4. 点击"开始打包"

---

## 完整示例

参见 `examples/star-orbit-vow/` — 一个完整的 5 章视觉小说项目，包含：
- 2 个角色（星野 + 我）
- 6 个场景（教室/天台/星轨观测站/3 个结局）
- 5 个变量（信任度/回忆数/是否约定/已解锁结局/游玩次数）
- 5 个章节 / 15 个片段 / 104 个 block
- 3 种结局（真结局/普通结局/Bad End）

```bash
# 查看示例项目
cd examples/star-orbit-vow
avgforge info
avgforge preview text 开始
avgforge preview graph
```
