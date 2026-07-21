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
│   ├── video/
│   └── particles/
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

**位置说明：**

| 位置 | 说明 |
|------|------|
| `left` | 左侧 |
| `center-left` | 中左 |
| `center` | 中间 |
| `center-right` | 中右 |
| `right` | 右侧 |

### 第 3 步：添加场景

```bash
# 简单场景（单层背景）
avgforge scene add "教室" \
    --layer "bg:1:backgrounds/classroom.png"

# 多层视差场景（3 层）
avgforge scene add "天台" \
    --layer "天空:14:backgrounds/rooftop/sky.png" \
    --layer "城市:7:backgrounds/rooftop/city.png" \
    --layer "天台:2:backgrounds/rooftop/floor.png"

# 查看场景列表
avgforge scene list
```

**图层格式：** `名称:距离:素材路径`

- **距离**：控制视差速度，数值越大越远（移动越慢）
- **素材路径**：相对于 `assets/` 目录

### 第 4 步：定义变量

```bash
# 数值变量（存档绑定）
avgforge var add trust "信任度" \
    --type number \
    --scope project \
    --persistence slot \
    --default 0 \
    --description "星野对主角的信任"

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

**变量类型：**

| 类型 | 说明 | 示例 |
|------|------|------|
| `boolean` | 布尔 | true / false |
| `number` | 数值 | 0, 1, 100 |
| `string` | 文本 | "真结局" |

**作用域：**

| 作用域 | 说明 |
|--------|------|
| `project` | 项目变量（自定义） |
| `system` | 系统变量（引擎维护） |

**持久化：**

| 持久化 | 说明 |
|--------|------|
| `slot` | 跟随存档（读档恢复） |
| `shared` | 跨存档共享（成就/解锁） |

### 第 5 步：添加章节

```bash
# 添加章节
avgforge chapter add "序章"
avgforge chapter add "第一章"
avgforge chapter add "终章"

# 查看章节列表
avgforge chapter list

# 调整章节顺序
avgforge chapter reorder "开始" "序章" "第一章" "终章"
```

### 第 6 步：添加片段（Fragment）

片段是章节内的子单元，用于分支跳转。

```bash
# 在"第一章"下添加片段
avgforge frag add "第一章" "选项1_打招呼"
avgforge frag add "第一章" "选项2_沉默"

# 查看片段列表
avgforge frag list "第一章"
```

### 第 7 步：编辑剧本

#### 方式一：用 $EDITOR 编辑

```bash
# 编辑"开始"章节的 main 片段
avgforge edit 开始/main

# 编辑"第一章"的自定义片段
avgforge edit "第一章/选项1_打招呼"
```

编辑器会打开（默认 vi，可通过 `EDITOR` 环境变量修改），写入 Ren'Py 风格剧本：

```renpy
scene 教室 with fade
show 星野 at right
星野 "你好。"
我 "你好，星野。"

menu "怎么回答":
    "打招呼" -> call 选项1_打招呼
    "保持沉默" -> call 选项2_沉默
```

保存退出后自动同步到项目。

#### 方式二：从文件导入

```bash
# 先写好剧本文件
cat > script.rpy << 'EOF'
scene 教室 with fade
show 星野 at right
星野 "你好。"
EOF

# 导入到指定片段
avgforge edit 开始/main --file script.rpy
```

### 第 8 步：验证项目

```bash
avgforge check
```

检查内容：
- JSON 格式正确性
- 章节引用完整性
- Fragment 跳转有效性
- 素材文件存在性
- 变量引用一致性

### 第 9 步：预览

#### 文本预览

```bash
avgforge preview text 开始
```

在终端打印剧本流程：

```
============================================================
  📖 开始
============================================================

  ── 片段: main ──

  🎬 [场景切换] → 教室
  【星野】你好。
  【我】你好，星野。

  🔀 [分支] 怎么回答
     1. 打招呼
     2. 保持沉默
```

#### Mermaid 流程图

```bash
avgforge preview graph
```

生成 `project_graph.mmd` 文件，用 VS Code Mermaid 插件或 [mermaid.live](https://mermaid.live) 查看。

#### 项目统计

```bash
avgforge preview stats
```

---

## 命令参考

### 项目管理

| 命令 | 说明 |
|------|------|
| `avgforge init <路径>` | 创建新项目 |
| `avgforge info [路径]` | 显示项目信息 |
| `avgforge check [路径]` | 验证项目完整性 |

### 角色管理

| 命令 | 说明 |
|------|------|
| `avgforge char list` | 列出所有角色 |
| `avgforge char add <名称> [--pos 位置] [--color-ring 颜色]` | 添加角色 |
| `avgforge char remove <ID或名称>` | 删除角色 |
| `avgforge char expr add <ID或名称> <表情名> <文件>` | 添加表情 |

### 场景管理

| 命令 | 说明 |
|------|------|
| `avgforge scene list` | 列出所有场景 |
| `avgforge scene add <名称> --layer <图层>` | 添加场景 |
| `avgforge scene remove <ID或名称>` | 删除场景 |

### 章节管理

| 命令 | 说明 |
|------|------|
| `avgforge chapter list` | 列出章节 |
| `avgforge chapter add <名称>` | 添加章节 |
| `avgforge chapter remove <名称>` | 删除章节 |
| `avgforge chapter reorder <名称1> <名称2> ...` | 调整顺序 |

### 片段管理

| 命令 | 说明 |
|------|------|
| `avgforge frag list <章节>` | 列出章节内片段 |
| `avgforge frag add <章节> <名称>` | 添加片段 |

### 剧本编辑

| 命令 | 说明 |
|------|------|
| `avgforge edit <章节>/<片段>` | 用 $EDITOR 编辑 |
| `avgforge edit <章节>/<片段> --file <路径>` | 从文件导入 |
| `avgforge block list <章节>/<片段>` | 列出 block |
| `avgforge block add <章节>/<片段> <类型>` | 添加 block |
| `avgforge block remove <章节>/<片段> <block_id>` | 删除 block |

### 变量管理

| 命令 | 说明 |
|------|------|
| `avgforge var list` | 列出所有变量 |
| `avgforge var add <key> <显示名> [--type 类型] [--scope 作用域] [--persistence 持久化]` | 添加变量 |
| `avgforge var remove <key>` | 删除变量 |

### 素材管理

| 命令 | 说明 |
|------|------|
| `avgforge asset list` | 列出所有素材 |
| `avgforge asset refs <素材>` | 查看素材引用 |

### 预览

| 命令 | 说明 |
|------|------|
| `avgforge preview text <章节>` | 文本预览 |
| `avgforge preview graph` | Mermaid 流程图 |
| `avgforge preview stats` | 项目统计 |

---

## Ren'Py 语法

### 场景切换

```renpy
scene <场景名> [with <过渡>] [duration <秒>]
```

示例：
```renpy
scene 教室 with fade
scene 天台 with fade duration 1.0
```

### 角色显示

```renpy
show <角色名> [at <位置>]
hide <角色名>
```

示例：
```renpy
show 星野 at right
hide 星野
```

### 对白

```renpy
<角色名> "<台词>"
```

示例：
```renpy
星野 "你好。"
我 "你好，星野。"
```

### 旁白

```renpy
"<旁白文本>"
```

示例：
```renpy
"夕阳洒进教室，将一切染成金色。"
```

### 等待

```renpy
pause <秒>
```

示例：
```renpy
pause 1.0
```

### 音频

```renpy
play music <文件> [volume <n>%] [loop] [fadein <秒>]
play sound <文件>
play voice <文件>
stop music
stop sound
```

示例：
```renpy
play music bgm/主题曲.mp3 loop fadein 0.5
stop music
```

### 变量赋值

```renpy
$ <变量> = <值>
$ <变量> += <值>
$ <变量> -= <值>
```

示例：
```renpy
$ trust += 1
$ trust -= 1
$ promised = true
```

### 分支

```renpy
menu "<标题>":
    "<选项1>" -> call <片段名>
    "<选项2>" -> call <片段名>
    "<选项3>" -> $ <变量赋值>
```

示例：
```renpy
menu "怎么回答":
    "打招呼" -> call 选项1_打招呼
    "保持沉默" -> $ trust -= 1
```

### 片段调用

```renpy
call <片段名>
```

示例：
```renpy
call 问候分支
```

### 幕布

```renpy
curtain close duration <秒>
curtain open duration <秒>
```

示例：
```renpy
curtain close duration 0.5
curtain open duration 1.0
```

### 注释

```renpy
# 这是注释
```

---

## 导入 LetsGal Studio 预览

AVGForge 生成的项目完全兼容 LetsGal Studio，可直接导入预览。

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
