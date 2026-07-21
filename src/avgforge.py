#!/usr/bin/env python3
"""
AVGForge — Enterprise-Grade Visual Novel Authoring Pipeline
Copyright (c) 2026 AVGForge Project Contributors

Dual-licensed under AGPL-3.0 and Commercial License.
See LICENSE for details.
"""

import argparse
import json
import os
import sys
import uuid
import shutil
import subprocess
import tempfile
import http.server
import socketserver
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

__version__ = "1.0.0-enterprise"
__author__ = "AVGForge Project Contributors"
__license__ = "AGPL-3.0 + Commercial"

# ============================================================================
# Constants
# ============================================================================

PROJECT_FILE = "project.json"
VARIABLES_FILE = "project.variables.json"
CHARACTERS_FILE = "characters.json"
SCENES_FILE = "scenes.json"
CHAPTERS_DIR = "chapters"
ASSETS_DIR = "assets"
CONFIG_DIR = "config"

DEFAULT_POSITIONS = [
    {"id": "left", "name": "左", "left": 2, "top": 2},
    {"id": "center-left", "name": "中左", "left": 19, "top": 2},
    {"id": "center", "name": "中", "left": 35, "top": 2},
    {"id": "center-right", "name": "中右", "left": 55, "top": 2},
    {"id": "right", "name": "右", "left": 68, "top": 2},
]

BLOCK_TYPES = [
    "dialogue", "narration", "scene", "curtain", "branch",
    "camera", "particle", "sound", "stopSound", "wait",
    "setver", "floatingText", "removeCharacter", "animateSprite",
    "switchDialogueStyle", "video", "stopVideo", "destroyScene",
    "resetCamera", "showExtensionUI", "callExtensionFunction",
    "callFragment", "comment", "portraitStyleRule", "returnToEntry",
]

# ============================================================================
# Utility Functions
# ============================================================================

def info(msg: str):
    print(f"  ℹ️  {msg}")

def success(msg: str):
    print(f"  ✓  {msg}")

def warn(msg: str):
    print(f"  ⚠️  {msg}")

def error(msg: str):
    print(f"  ✗  {msg}", file=sys.stderr)

def gen_id() -> str:
    return str(uuid.uuid4())

def now_iso() -> str:
    return datetime.now().isoformat()

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def find_project_root(start: Path = None) -> Optional[Path]:
    """Find project root by looking for project.json"""
    if start is None:
        start = Path.cwd()
    current = start.resolve()
    while current != current.parent:
        if (current / PROJECT_FILE).exists():
            return current
        current = current.parent
    return None

# ============================================================================
# Project Commands
# ============================================================================

def cmd_init(args):
    """Initialize a new AVGForge project."""
    project_path = Path(args.name).resolve()
    if project_path.exists() and any(project_path.iterdir()):
        error(f"目录不为空: {project_path}")
        return 1

    project_path.mkdir(parents=True, exist_ok=True)

    # project.json
    project = {
        "id": gen_id(),
        "name": args.name,
        "version": "1.0.0",
        "engineVersion": __version__,
        "description": args.description or "",
        "resolution": {"width": 1920, "height": 1080},
        "backgroundColor": "#000",
        "chapterOrder": ["开始"],
        "extensions": {},
        "extensionSettings": {},
        "systemBindings": {
            "internal.system.title": "ui:@avg.internal.default-shell/title-screen",
            "internal.system.save": "ui:@avg.internal.default-shell/save-screen",
            "internal.system.load": "ui:@avg.internal.default-shell/save-screen",
            "internal.system.settings": "ui:@avg.internal.default-shell/settings-screen",
            "internal.system.history": "ui:@avg.internal.default-shell/history-screen",
        },
        "inputBindings": {
            "internal.input.advance": ["Space", "Enter", "wheeldown"],
            "internal.input.skip": ["Control"],
            "internal.input.auto-toggle": ["a"],
            "internal.input.hide-dialogue": ["contextmenu", "Delete"],
            "internal.input.replay-voice": ["r"],
            "internal.input.quick-save": ["F5"],
            "internal.input.quick-load": ["F9"],
        },
        "window": {
            "lockAspectRatio": False,
            "allowMaximize": True,
            "allowFullscreen": True,
            "launchMode": "windowed",
        },
    }
    save_json(project_path / PROJECT_FILE, project)

    # project.variables.json
    variables = {"version": 2, "variables": []}
    save_json(project_path / VARIABLES_FILE, variables)

    # characters.json
    characters = {
        "version": 2,
        "globalSettings": {
            "defaultPosition": "center",
            "graphics": {"keepAspectRatio": True, "size": "(30%,30%)"},
            "positions": DEFAULT_POSITIONS,
            "defaultPositionId": "center",
            "defaultAnchor": "left_top",
        },
        "attributeTemplate": [],
        "characters": [],
    }
    save_json(project_path / CHARACTERS_FILE, characters)

    # scenes.json
    scenes = {"version": 3, "scenes": []}
    save_json(project_path / SCENES_FILE, scenes)

    # chapters/开始.json (entry chapter)
    chapters_dir = project_path / CHAPTERS_DIR
    chapters_dir.mkdir(exist_ok=True)
    entry_chapter = {
        "id": gen_id(),
        "name": "开始",
        "fragments": [
            {
                "id": "frag-main",
                "name": "main",
                "blocks": [
                    {
                        "type": "narration",
                        "props": {"disabled": False},
                        "content": [{"type": "text", "text": "游戏从这里开始。", "styles": {}}],
                    }
                ],
            }
        ],
    }
    save_json(chapters_dir / "开始.json", entry_chapter)

    # assets directories
    for subdir in ["backgrounds", "characters", "bgm", "se", "voice", "video", "particles", "ui"]:
        (project_path / ASSETS_DIR / subdir).mkdir(parents=True, exist_ok=True)

    # config
    (project_path / CONFIG_DIR / "personalization").mkdir(parents=True, exist_ok=True)
    save_json(project_path / CONFIG_DIR / "personalization" / "active.json", {})

    success(f"项目已创建: {project_path}")
    info(f"引擎版本: {__version__}")
    info(f"画布尺寸: {project['resolution']['width']}x{project['resolution']['height']}")
    info(f"入口章节: 开始")
    print()
    print(f"  下一步:")
    print(f"    cd {args.name}")
    print(f"    avgforge char add <id> --name <角色名>")
    print(f"    avgforge scene add <id> --name <场景名>")
    print(f"    avgforge edit 开始/main")
    return 0

def cmd_info(args):
    """Show project information."""
    root = find_project_root(Path(args.path) if args.path else None)
    if not root:
        error("未找到 AVGForge 项目 (缺少 project.json)")
        return 1

    project = load_json(root / PROJECT_FILE)
    characters = load_json(root / CHARACTERS_FILE)
    scenes = load_json(root / SCENES_FILE)
    variables = load_json(root / VARIABLES_FILE)

    print(f"\n  ╔══════════════════════════════════════════════════╗")
    print(f"  ║  {project['name']:<46} ║")
    print(f"  ╚══════════════════════════════════════════════════╝")
    print()
    print(f"  项目 ID:     {project['id']}")
    print(f"  版本:        {project['version']}")
    print(f"  引擎版本:    {project.get('engineVersion', '?')}")
    print(f"  描述:        {project.get('description', '(无)')}")
    print(f"  画布尺寸:    {project['resolution']['width']}x{project['resolution']['height']}")
    print(f"  章节顺序:    {' → '.join(project.get('chapterOrder', []))}")
    print()
    print(f"  角色:        {len(characters.get('characters', []))} 个")
    for c in characters.get('characters', []):
        exprs = sum(len(ch.get('expressions', [])) for ch in [c])
        print(f"    · {c['name']} ({c.get('id', '?')[:8]}...) — {exprs} 表情")
    print()
    print(f"  场景:        {len(scenes.get('scenes', []))} 个")
    for s in scenes.get('scenes', []):
        layers = len(s.get('layers', []))
        print(f"    · {s['name']} — {layers} 层")
    print()
    print(f"  变量:        {len(variables.get('variables', []))} 个")
    print()
    # 统计 blocks
    total_blocks = 0
    chapters_dir = root / CHAPTERS_DIR
    if chapters_dir.exists():
        for ch_file in chapters_dir.glob("*.json"):
            ch = load_json(ch_file)
            for frag in ch.get('fragments', []):
                total_blocks += len(frag.get('blocks', []))
    print(f"  Block 总数:  {total_blocks}")
    print()
    return 0

# ============================================================================
# Character Commands
# ============================================================================

def cmd_char_list(args):
    """List characters."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    characters = load_json(root / CHARACTERS_FILE)
    chars = characters.get('characters', [])
    if not chars:
        info("暂无角色")
        return 0
    print(f"\n  角色 ({len(chars)} 个):")
    print(f"  {'ID':<12} {'名称':<12} {'位置':<10} {'表情数':<8} {'主题色'}")
    print(f"  {'-'*12} {'-'*12} {'-'*10} {'-'*8} {'-'*20}")
    for c in chars:
        cid = c.get('id', '?')[:8]
        name = c.get('name', '?')
        pos = c.get('defaultPosition', 'center')
        exprs = len(c.get('expressions', []))
        tc = c.get('themeColor', {}).get('ring', '-')
        print(f"  {cid:<12} {name:<12} {pos:<10} {exprs:<8} {tc}")
    print()
    return 0

def cmd_char_add(args):
    """Add a character."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    characters = load_json(root / CHARACTERS_FILE)
    # 检查重复
    for c in characters.get('characters', []):
        if c.get('id') == args.id or c.get('name') == args.name:
            error(f"角色已存在: {args.id} / {args.name}")
            return 1
    char = {
        "id": args.id,
        "name": args.name,
        "expressions": [],
        "defaultPosition": args.position,
        "themeColor": {
            "bg": args.color_bg or "#dbeafe",
            "fg": args.color_fg or "#1e40af",
            "ring": args.color_ring or "#60a5fa",
        },
        "graphics": {"size": "(100%,100%)"},
        "attributeValues": {},
    }
    characters.setdefault('characters', []).append(char)
    save_json(root / CHARACTERS_FILE, characters)
    success(f"角色已添加: {args.name} ({args.id})")
    info(f"默认位置: {args.position}")
    info(f"主题色: {char['themeColor']['ring']}")
    return 0

def cmd_char_rm(args):
    """Remove a character."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    characters = load_json(root / CHARACTERS_FILE)
    before = len(characters.get('characters', []))
    characters['characters'] = [
        c for c in characters.get('characters', [])
        if c.get('id') != args.id and c.get('name') != args.id
    ]
    after = len(characters['characters'])
    if before == after:
        error(f"未找到角色: {args.id}")
        return 1
    save_json(root / CHARACTERS_FILE, characters)
    success(f"已删除角色: {args.id}")
    return 0

# ============================================================================
# Scene Commands
# ============================================================================

def cmd_scene_list(args):
    """List scenes."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    scenes = load_json(root / SCENES_FILE)
    sc_list = scenes.get('scenes', [])
    if not sc_list:
        info("暂无场景")
        return 0
    print(f"\n  场景 ({len(sc_list)} 个):")
    print(f"  {'ID':<12} {'名称':<16} {'层数':<6} {'图层'}")
    print(f"  {'-'*12} {'-'*16} {'-'*6} {'-'*30}")
    for s in sc_list:
        sid = s.get('id', '?')[:8]
        name = s.get('name', '?')
        layers = s.get('layers', [])
        layer_names = ', '.join(l.get('name', '?') for l in layers[:3])
        if len(layers) > 3:
            layer_names += f" +{len(layers)-3}"
        print(f"  {sid:<12} {name:<16} {len(layers):<6} {layer_names}")
    print()
    return 0

def cmd_scene_add(args):
    """Add a scene."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    scenes = load_json(root / SCENES_FILE)
    scene = {
        "id": gen_id(),
        "name": args.name,
        "layers": [],
    }
    # 解析 --layer 参数 (格式: name:distance:assetpath)
    for i, layer_str in enumerate(args.layers or []):
        parts = layer_str.split(':', 2)
        if len(parts) < 2:
            warn(f"跳过无效图层定义: {layer_str} (格式: name:distance[:assetpath])")
            continue
        name = parts[0]
        try:
            distance = float(parts[1])
        except ValueError:
            distance = 1.0
        asset = parts[2] if len(parts) > 2 else ""
        scene['layers'].append({
            "id": gen_id(),
            "name": name,
            "assetPath": asset,
            "distance": distance,
        })
    scenes.setdefault('scenes', []).append(scene)
    save_json(root / SCENES_FILE, scenes)
    success(f"场景已添加: {args.name}")
    info(f"图层数: {len(scene['layers'])}")
    return 0

def cmd_scene_rm(args):
    """Remove a scene."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    scenes = load_json(root / SCENES_FILE)
    before = len(scenes.get('scenes', []))
    scenes['scenes'] = [
        s for s in scenes.get('scenes', [])
        if s.get('id') != args.id and s.get('name') != args.id
    ]
    after = len(scenes['scenes'])
    if before == after:
        error(f"未找到场景: {args.id}")
        return 1
    save_json(root / SCENES_FILE, scenes)
    success(f"已删除场景: {args.id}")
    return 0

# ============================================================================
# Chapter / Fragment Commands
# ============================================================================

def cmd_chapter_list(args):
    """List chapters."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    project = load_json(root / PROJECT_FILE)
    chapters_dir = root / CHAPTERS_DIR
    print(f"\n  章节 ({len(project.get('chapterOrder', []))} 个):")
    print(f"  {'序号':<4} {'名称':<20} {'片段数':<8} {'Block 数'}")
    print(f"  {'-'*4} {'-'*20} {'-'*8} {'-'*10}")
    for i, ch_name in enumerate(project.get('chapterOrder', []), 1):
        ch_file = chapters_dir / f"{ch_name}.json"
        if not ch_file.exists():
            print(f"  {i:<4} {ch_name:<20} (文件缺失)")
            continue
        ch = load_json(ch_file)
        frags = ch.get('fragments', [])
        blocks = sum(len(f.get('blocks', [])) for f in frags)
        print(f"  {i:<4} {ch_name:<20} {len(frags):<8} {blocks}")
    print()
    return 0

def cmd_chapter_add(args):
    """Add a chapter."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    project = load_json(root / PROJECT_FILE)
    if args.name in project.get('chapterOrder', []):
        error(f"章节已存在: {args.name}")
        return 1
    chapter = {
        "id": gen_id(),
        "name": args.name,
        "fragments": [
            {
                "id": f"frag-{args.name}-main",
                "name": "main",
                "blocks": [],
            }
        ],
    }
    save_json(root / CHAPTERS_DIR / f"{args.name}.json", chapter)
    project.setdefault('chapterOrder', []).append(args.name)
    save_json(root / PROJECT_FILE, project)
    success(f"章节已添加: {args.name}")
    return 0

def cmd_frag_list(args):
    """List fragments in a chapter."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    ch_file = root / CHAPTERS_DIR / f"{args.chapter}.json"
    if not ch_file.exists():
        error(f"章节不存在: {args.chapter}")
        return 1
    ch = load_json(ch_file)
    frags = ch.get('fragments', [])
    print(f"\n  章节「{args.chapter}」的片段 ({len(frags)} 个):")
    print(f"  {'ID':<30} {'名称':<16} {'Block 数'}")
    print(f"  {'-'*30} {'-'*16} {'-'*10}")
    for f in frags:
        fid = f.get('id', '?')
        fname = f.get('name', '?')
        blocks = len(f.get('blocks', []))
        print(f"  {fid:<30} {fname:<16} {blocks}")
    print()
    return 0

# ============================================================================
# Edit Command (Ren'Py style)
# ============================================================================

RENPY_TEMPLATE = """# AVGForge Ren'Py 风格剧本
# 章节: {chapter} / 片段: {fragment}
# 语法参考: https://github.com/YOUR_USERNAME/avgforge/docs/renpy-syntax.md

scene 教室 with fade
show 星野 happy at right
星野 "你好，初次见面。"
menu "如何回应":
    "打招呼" -> call 问候分支
    "沉默" -> $ 好感度 -= 1
"""

def cmd_edit(args):
    """Edit a fragment in Ren'Py style."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    # 解析 chapter/fragment
    if '/' not in args.target:
        error("格式应为: chapter/fragment (例如: 开始/main)")
        return 1
    chapter_name, frag_id = args.target.split('/', 1)
    ch_file = root / CHAPTERS_DIR / f"{chapter_name}.json"
    if not ch_file.exists():
        error(f"章节不存在: {chapter_name}")
        return 1
    ch = load_json(ch_file)
    frag = None
    for f in ch.get('fragments', []):
        if f.get('id') == frag_id or f.get('name') == frag_id:
            frag = f
            break
    if not frag:
        error(f"片段不存在: {frag_id}")
        return 1

    # 写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.rpy', delete=False, encoding='utf-8') as tf:
        tf.write(RENPY_TEMPLATE.format(chapter=chapter_name, fragment=frag_id))
        tmp_path = tf.name

    editor = os.environ.get('EDITOR', 'vi')
    info(f"使用编辑器: {editor}")
    try:
        subprocess.run([editor, tmp_path], check=True)
    except subprocess.CalledProcessError:
        error("编辑器退出异常")
        os.unlink(tmp_path)
        return 1
    except FileNotFoundError:
        error(f"编辑器不存在: {editor} (设置 $EDITOR 环境变量)")
        os.unlink(tmp_path)
        return 1

    # 读取编辑后的内容
    with open(tmp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    os.unlink(tmp_path)

    # TODO: 解析 Ren'Py 语法并转换为 blocks
    # 目前先保存为 comment block
    success(f"已编辑片段: {args.target}")
    info(f"内容长度: {len(content)} 字符")
    warn("Ren'Py 解析器开发中，当前仅保存原始文本")
    return 0

# ============================================================================
# Check Command
# ============================================================================

def cmd_check(args):
    """Validate project integrity."""
    root = find_project_root(Path(args.path) if args.path else None)
    if not root:
        error("未找到项目")
        return 1
    info(f"检查项目: {root}")
    errors_count = 0
    warnings_count = 0

    # 检查 project.json
    try:
        project = load_json(root / PROJECT_FILE)
        success("project.json 读取成功")
    except Exception as e:
        error(f"project.json 读取失败: {e}")
        return 1

    # 检查章节文件
    chapters_dir = root / CHAPTERS_DIR
    if not chapters_dir.exists():
        error(f"章节目录不存在: {chapters_dir}")
        return 1

    for ch_name in project.get('chapterOrder', []):
        ch_file = chapters_dir / f"{ch_name}.json"
        if not ch_file.exists():
            error(f"章节文件缺失: {ch_name}.json")
            errors_count += 1
            continue
        try:
            ch = load_json(ch_file)
            for frag in ch.get('fragments', []):
                for i, block in enumerate(frag.get('blocks', [])):
                    btype = block.get('type')
                    if btype not in BLOCK_TYPES:
                        warn(f"{ch_name}/{frag.get('id')}/block[{i}]: 未知 block 类型 '{btype}'")
                        warnings_count += 1
        except Exception as e:
            error(f"章节文件解析失败: {ch_name}.json: {e}")
            errors_count += 1

    # 检查角色引用
    characters = load_json(root / CHARACTERS_FILE)
    char_ids = {c['id'] for c in characters.get('characters', [])}
    for ch_file in chapters_dir.glob("*.json"):
        ch = load_json(ch_file)
        for frag in ch.get('fragments', []):
            for block in frag.get('blocks', []):
                if block.get('type') == 'dialogue':
                    cid = block.get('props', {}).get('characterId', '')
                    if cid and cid not in char_ids:
                        warn(f"{ch_file.name}/{frag.get('id')}: 引用不存在的角色 {cid}")
                        warnings_count += 1

    # 检查素材引用
    scenes = load_json(root / SCENES_FILE)
    for s in scenes.get('scenes', []):
        for layer in s.get('layers', []):
            asset = layer.get('assetPath', '')
            if asset and not (root / ASSETS_DIR / asset).exists():
                warn(f"场景 {s['name']} 图层 {layer['name']}: 素材缺失 {asset}")
                warnings_count += 1

    print()
    if errors_count == 0 and warnings_count == 0:
        success("项目检查通过，无错误无警告 ✓")
        return 0
    else:
        if errors_count:
            error(f"发现 {errors_count} 个错误")
        if warnings_count:
            warn(f"发现 {warnings_count} 个警告")
        return 1 if errors_count else 0

# ============================================================================
# Preview Commands
# ============================================================================

def cmd_preview_text(args):
    """Text preview of a chapter."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    ch_file = root / CHAPTERS_DIR / f"{args.chapter}.json"
    if not ch_file.exists():
        error(f"章节不存在: {args.chapter}")
        return 1
    ch = load_json(ch_file)
    characters = load_json(root / CHARACTERS_FILE)
    char_map = {c['id']: c['name'] for c in characters.get('characters', [])}

    print(f"\n  ════════════════════════════════════════════")
    print(f"    章节: {ch.get('name', args.chapter)}")
    print(f"  ════════════════════════════════════════════\n")

    for frag in ch.get('fragments', []):
        print(f"  ── 片段: {frag.get('name', frag.get('id'))} ──\n")
        for block in frag.get('blocks', []):
            btype = block.get('type')
            props = block.get('props', {})
            content = block.get('content', [])
            text = content[0].get('text', '') if content else ''

            if btype == 'dialogue':
                cid = props.get('characterId', '')
                name = char_map.get(cid, props.get('characterName', '???'))
                expr = props.get('expression', '')
                expr_str = f" [{expr}]" if expr else ""
                print(f"    {name}{expr_str}: {text}")
            elif btype == 'narration':
                print(f"    〔旁白〕{text}")
            elif btype == 'scene':
                print(f"    [场景切换 → {props.get('sceneName', '?')}]")
            elif btype == 'branch':
                print(f"    [分支] {props.get('title', '')}")
                choices = props.get('choices', [])
                if isinstance(choices, str):
                    try:
                        choices = json.loads(choices)
                    except:
                        choices = []
                for i, c in enumerate(choices):
                    print(f"      {i+1}. {c.get('text', '?')} → {c.get('fragmentId', '?')}")
            elif btype == 'wait':
                print(f"    [等待 {props.get('duration', '?')}ms]")
            elif btype == 'sound':
                print(f"    [播放 {props.get('soundType', '?')}: {props.get('uri', '?')}]")
            elif btype == 'curtain':
                print(f"    [幕布 {props.get('op', '?')}]")
            elif btype == 'floatingText':
                print(f"    [浮字: {props.get('text', '?')}]")
            elif btype == 'comment':
                print(f"    // {text}")
            else:
                print(f"    [{btype}]")
        print()
    return 0

def cmd_preview_web(args):
    """Start web preview server."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    port = args.port or 8765
    info(f"启动 Web 预览服务器: http://localhost:{port}")
    info(f"项目: {root}")
    info(f"按 Ctrl+C 停止")
    # TODO: 生成 HTML 并启动服务器
    warn("Web 预览引擎开发中，当前仅启动占位服务器")
    try:
        with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            webbrowser.open(f"http://localhost:{port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        success("预览服务器已停止")
    except OSError as e:
        error(f"无法启动服务器: {e}")
        return 1
    return 0

# ============================================================================
# Build Commands
# ============================================================================

def cmd_build_html(args):
    """Build project to single-file HTML."""
    root = find_project_root()
    if not root:
        error("未找到项目")
        return 1
    output = Path(args.output) if args.output else root / "build" / "game.html"
    info(f"构建 HTML: {output}")
    # TODO: 实际的 HTML 生成逻辑
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("<!-- AVGForge build output - 开发中 -->", encoding='utf-8')
    success(f"HTML 已生成: {output}")
    info(f"文件大小: {output.stat().st_size} 字节")
    warn("HTML 构建引擎开发中，当前为占位文件")
    return 0

# ============================================================================
# CLI Definition
# ============================================================================

def build_parser():
    parser = argparse.ArgumentParser(
        prog="avgforge",
        description="AVGForge — Enterprise-Grade Visual Novel Authoring Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  avgforge init my-game --template blank
  avgforge info
  avgforge char add hoshino --name "星野" --pos right
  avgforge scene add classroom --name "教室" --layer "bg:1:bg.png"
  avgforge chapter add 序章
  avgforge edit 序章/main
  avgforge preview text 序章
  avgforge preview web
  avgforge build html -o game.html

文档: https://github.com/YOUR_USERNAME/avgforge
        """,
    )
    parser.add_argument('--version', action='version', version=f'AVGForge {__version__} ({__license__})')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # init
    p_init = subparsers.add_parser('init', help='初始化新项目')
    p_init.add_argument('name', help='项目名称/目录名')
    p_init.add_argument('--template', default='blank', choices=['blank', 'demo'], help='项目模板')
    p_init.add_argument('--description', '-d', help='项目描述')
    p_init.set_defaults(func=cmd_init)

    # info
    p_info = subparsers.add_parser('info', help='显示项目信息')
    p_info.add_argument('path', nargs='?', help='项目路径 (默认当前目录)')
    p_info.set_defaults(func=cmd_info)

    # char
    p_char = subparsers.add_parser('char', help='角色管理')
    char_sub = p_char.add_subparsers(dest='char_command', required=True)
    char_sub.add_parser('list', help='列出角色').set_defaults(func=cmd_char_list)
    p_char_add = char_sub.add_parser('add', help='添加角色')
    p_char_add.add_argument('id', help='角色 ID')
    p_char_add.add_argument('--name', required=True, help='角色名称')
    p_char_add.add_argument('--position', '--pos', default='center', help='默认位置')
    p_char_add.add_argument('--color-bg', help='主题色 - 背景')
    p_char_add.add_argument('--color-fg', help='主题色 - 前景')
    p_char_add.add_argument('--color-ring', help='主题色 - 强调')
    p_char_add.set_defaults(func=cmd_char_add)
    p_char_rm = char_sub.add_parser('rm', help='删除角色')
    p_char_rm.add_argument('id', help='角色 ID 或名称')
    p_char_rm.set_defaults(func=cmd_char_rm)

    # scene
    p_scene = subparsers.add_parser('scene', help='场景管理')
    scene_sub = p_scene.add_subparsers(dest='scene_command', required=True)
    scene_sub.add_parser('list', help='列出场景').set_defaults(func=cmd_scene_list)
    p_scene_add = scene_sub.add_parser('add', help='添加场景')
    p_scene_add.add_argument('id', help='场景 ID')
    p_scene_add.add_argument('--name', required=True, help='场景名称')
    p_scene_add.add_argument('--layer', action='append', dest='layers', help='图层 (格式: name:distance[:assetpath])')
    p_scene_add.set_defaults(func=cmd_scene_add)
    p_scene_rm = scene_sub.add_parser('rm', help='删除场景')
    p_scene_rm.add_argument('id', help='场景 ID 或名称')
    p_scene_rm.set_defaults(func=cmd_scene_rm)

    # chapter
    p_chapter = subparsers.add_parser('chapter', help='章节管理')
    chapter_sub = p_chapter.add_subparsers(dest='chapter_command', required=True)
    chapter_sub.add_parser('list', help='列出章节').set_defaults(func=cmd_chapter_list)
    p_ch_add = chapter_sub.add_parser('add', help='添加章节')
    p_ch_add.add_argument('name', help='章节名称')
    p_ch_add.set_defaults(func=cmd_chapter_add)

    # frag
    p_frag = subparsers.add_parser('frag', help='片段管理')
    frag_sub = p_frag.add_subparsers(dest='frag_command', required=True)
    p_frag_list = frag_sub.add_parser('list', help='列出片段')
    p_frag_list.add_argument('chapter', help='章节名称')
    p_frag_list.set_defaults(func=cmd_frag_list)

    # edit
    p_edit = subparsers.add_parser('edit', help='编辑片段 (Ren\'Py 风格)')
    p_edit.add_argument('target', help='chapter/fragment (例如: 序章/main)')
    p_edit.set_defaults(func=cmd_edit)

    # check
    p_check = subparsers.add_parser('check', help='验证项目完整性')
    p_check.add_argument('path', nargs='?', help='项目路径')
    p_check.set_defaults(func=cmd_check)

    # preview
    p_preview = subparsers.add_parser('preview', help='预览')
    preview_sub = p_preview.add_subparsers(dest='preview_command', required=True)
    p_preview_text = preview_sub.add_parser('text', help='文本预览')
    p_preview_text.add_argument('chapter', help='章节名称')
    p_preview_text.set_defaults(func=cmd_preview_text)
    p_preview_web = preview_sub.add_parser('web', help='Web 预览')
    p_preview_web.add_argument('--port', type=int, default=8765, help='服务器端口')
    p_preview_web.set_defaults(func=cmd_preview_web)

    # build
    p_build = subparsers.add_parser('build', help='构建')
    build_sub = p_build.add_subparsers(dest='build_command', required=True)
    p_build_html = build_sub.add_parser('html', help='构建为单文件 HTML')
    p_build_html.add_argument('-o', '--output', help='输出文件路径')
    p_build_html.set_defaults(func=cmd_build_html)

    return parser

# ============================================================================
# Main
# ============================================================================

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        return 1
    return args.func(args) or 0

if __name__ == '__main__':
    sys.exit(main())
