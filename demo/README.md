# 《星轨之约》Demo

> 基于 AVGForge CLI 创建的标准 LetsGal Studio 项目，可直接导入预览

## 项目信息

| 项目 | 内容 |
|---|---|
| **游戏名** | 星轨之约 |
| **版本** | 1.0.0 |
| **作者** | AVGForge Demo |
| **引擎** | LetsGal Studio 1.0.0 |
| **画布** | 1920×1080 |

## 内容规模

| 维度 | 数量 |
|---|---|
| **章节** | 5 个（开始 → 第一章_相遇 → 第二章_相知 → 第三章_抉择 → 终章） |
| **片段** | 15 个 |
| **Block 总数** | 104 个 |
| **角色** | 2 个（星野 + 我） |
| **场景** | 6 个（教室/天台/星轨观测站/3 个结局） |
| **变量** | 5 个（信任度/回忆数/是否约定/已解锁结局/游玩次数） |
| **结局** | 3 种（真结局/普通结局/Bad End） |

## 素材复用

本项目复用了 LetsGal Studio 官方模板《LetsGal 恋爱游戏进行时》的素材资源：

| 素材类型 | 来源 | 用途 |
|---|---|---|
| 角色立绘 | 真琴（Makoto） | 星野（5 表情：平静/微笑/闭眼/惊讶/害羞） |
| 角色立绘 | 影缝（Kagenui） | 我（3 表情：平静/生气/严肃） |
| 背景 | LG01 序章 | 星轨观测站（6 层视差） |
| 背景 | LG02 雪域 | 天台（6 层视差） |
| 背景 | 部室关门 | 教室 |
| 背景 | LG06 主体 | 真结局 |
| 背景 | 东京全景 | 普通结局 |
| 背景 | LG04 夜晚关灯 | Bad End |
| BGM | 雪之华等 | 背景音乐 |

## 剧情简介

毕业前最后 30 天，男主在教室里遇见了自称来自"星轨观测站"的神秘少女星野。两周的相处后，她必须搭上每 120 年才经过一次的星轨离开。玩家需要在最终抉择中决定：是随她踏入宇宙，还是留在人间，抑或……

## 如何预览

### 方法 1：用 LetsGal Studio 预览（推荐）

1. 打开 LetsGal Studio
2. 选择"打开项目"
3. 选择本目录（包含 `project.json`）
4. 按 F5 运行预览

### 方法 2：用 AVGForge CLI 文本预览

```bash
# 在仓库根目录
./avgforge preview text 开始 --path demo
./avgforge preview text 第一章_相遇 --path demo
./avgforge info --path demo
./avgforge check --path demo
```

## 项目结构

```
demo/
├── project.json              # 项目配置
├── project.variables.json    # 变量定义
├── characters.json           # 角色配置（星野 + 我）
├── scenes.json               # 场景配置（6 个场景）
├── chapters/                 # 章节剧本
│   ├── 开始.json             # 入口章节
│   ├── 第一章_相遇.json      # 相遇 + 分支
│   ├── 第二章_相知.json      # 相知 + 分支
│   ├── 第三章_抉择.json      # 抉择 + 3 分支
│   └── 终章.json             # 3 个结局
├── assets/                   # 素材（复用 game_data）
│   ├── backgrounds/          # 背景图
│   ├── characters/           # 立绘
│   ├── bgm/                  # 背景音乐
│   ├── se/                   # 音效
│   ├── voice/                # 语音
│   └── video/                # 视频
├── extensions/               # 扩展（默认游戏壳）
│   └── avg.internal.default-shell/
└── config/                   # 个性化配置
```

## 版权声明

本项目复用的素材（立绘、背景、BGM、语音等）版权归 LetsGal Studio 官方所有，仅供学习交流与技术研究所用，不得用于商业用途。

如需商业使用，请前往 [avg-engine.com](https://avg-engine.com/) 购买正版授权。

详见上级目录的 [DISCLAIMER.md](../game_data/DISCLAIMER.md)。
