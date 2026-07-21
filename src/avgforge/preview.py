"""
AVGForge 预览模块
- 文本预览：终端打印剧本流程
- Mermaid 流程图：生成分支结构图
"""
import json
from typing import Dict, List
from .project import Project


def preview_text(project: Project, chapter_name: str) -> str:
    """文本预览：渲染章节为可读文本"""
    if chapter_name not in project.chapters:
        return f"错误：章节 '{chapter_name}' 不存在"

    chapter = project.chapters[chapter_name]
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  📖 {chapter['name']}")
    lines.append(f"{'='*60}\n")

    char_map = {c["id"]: c["name"] for c in project.char_list()}
    scene_map = {s["id"]: s["name"] for s in project.scene_list()}

    for frag in chapter.get("fragments", []):
        lines.append(f"\n  ── 片段: {frag['name']} ──\n")
        for i, b in enumerate(frag.get("blocks", [])):
            btype = b.get("type", "")
            props = b.get("props", {})
            content = b.get("content", [])
            text = content[0].get("text", "") if content else ""

            if props.get("disabled"):
                continue

            if btype == "narration":
                lines.append(f"  〔旁白〕{text}")
            elif btype == "dialogue":
                char_name = props.get("characterName", "") or char_map.get(props.get("characterId", ""), "?")
                expr = props.get("expression", "")
                expr_str = f"（{expr}）" if expr else ""
                lines.append(f"  【{char_name}】{expr_str}{text}")
            elif btype == "scene":
                scene_name = props.get("sceneName", "") or scene_map.get(props.get("sceneId", ""), "?")
                lines.append(f"  🎬 [场景切换] → {scene_name}")
            elif btype == "curtain":
                op = props.get("op", "open")
                lines.append(f"  🎭 [幕布{op}]")
            elif btype == "wait":
                duration = props.get("duration", "1000")
                lines.append(f"  ⏱  [等待 {int(duration)/1000:.1f}s]")
            elif btype == "sound":
                sound_type = props.get("soundType", "BGM")
                uri = props.get("uri", "")
                lines.append(f"  🎵 [播放{sound_type}] {uri}")
            elif btype == "stopSound":
                sound_type = props.get("soundType", "BGM")
                lines.append(f"  🎵 [停止{sound_type}]")
            elif btype == "camera":
                params = []
                if props.get("offsetX"): params.append(f"x={props['offsetX']}")
                if props.get("offsetY"): params.append(f"y={props['offsetY']}")
                if props.get("zoom"): params.append(f"zoom={props['zoom']}")
                lines.append(f"  📷 [镜头] {' '.join(params)}")
            elif btype == "particle":
                mode = props.get("mode", "show")
                preset = props.get("preset", "")
                lines.append(f"  ✨ [粒子{mode}] {preset}")
            elif btype == "floatingText":
                lines.append(f"  💬 [浮字] \"{text}\"")
            elif btype == "setver":
                key = props.get("key", "")
                op = props.get("op", "set")
                val = props.get("bLit", "")
                op_map = {"set": "=", "add": "+=", "sub": "-=", "mul": "*=", "div": "/="}
                lines.append(f"  🔧 [变量] {key} {op_map.get(op, '=')} {val}")
            elif btype == "branch":
                title = props.get("title", "")
                lines.append(f"\n  🔀 [分支] {title}")
                choices = props.get("choices", "[]")
                if isinstance(choices, str):
                    choices = json.loads(choices)
                for j, c in enumerate(choices):
                    lines.append(f"     {j+1}. {c.get('text', '')}")
                lines.append("")
            elif btype == "callFragment":
                fid = props.get("fragmentId", "")
                frag_name = "?"
                for ch in project.chapters.values():
                    for f in ch.get("fragments", []):
                        if f["id"] == fid:
                            frag_name = f["name"]
                            break
                lines.append(f"  📞 [调用片段] → {frag_name}")
            elif btype == "removeCharacter":
                char_name = props.get("characterName", "")
                lines.append(f"  👋 [移除角色] {char_name}")
            elif btype == "comment":
                if text:
                    lines.append(f"  💭 [注释] {text}")

    lines.append(f"\n{'='*60}\n")
    return "\n".join(lines)


def preview_graph_mermaid(project: Project) -> str:
    """生成 Mermaid 流程图"""
    lines = ["graph TD"]
    lines.append("    %% 章节主干")

    # 章节节点
    chapter_order = project.project.get("chapterOrder", list(project.chapters.keys()))
    for i, ch_name in enumerate(chapter_order):
        lines.append(f"    CH{i}[{ch_name}]")
        if i > 0:
            lines.append(f"    CH{i-1} --> CH{i}")

    lines.append("")
    lines.append("    %% Fragment 与分支")

    # 每个章节的 fragment 和分支
    for ch_idx, ch_name in enumerate(chapter_order):
        if ch_name not in project.chapters:
            continue
        chapter = project.chapters[ch_name]
        for frag in chapter.get("fragments", []):
            frag_id = frag["id"]
            frag_name = frag["name"]
            node_id = f"F{ch_idx}_{frag_name}"
            lines.append(f"    {node_id}([{ch_name}/{frag_name}])")
            lines.append(f"    CH{ch_idx} --> {node_id}")

            # 找分支
            for b in frag.get("blocks", []):
                if b.get("type") == "branch":
                    props = b.get("props", {})
                    title = props.get("title", "")
                    choices = props.get("choices", "[]")
                    if isinstance(choices, str):
                        choices = json.loads(choices)
                    for j, c in enumerate(choices):
                        target_fid = c.get("fragmentId", "")
                        if target_fid:
                            # 找目标 fragment
                            for t_ch_idx, t_ch_name in enumerate(chapter_order):
                                if t_ch_name not in project.chapters:
                                    continue
                                for t_frag in project.chapters[t_ch_name].get("fragments", []):
                                    if t_frag["id"] == target_fid:
                                        t_node = f"F{t_ch_idx}_{t_frag['name']}"
                                        choice_text = c.get("text", "")[:20]
                                        lines.append(f"    {node_id} -->|{choice_text}| {t_node}")
                                        break

                elif b.get("type") == "callFragment":
                    props = b.get("props", {})
                    target_fid = props.get("fragmentId", "")
                    if target_fid:
                        for t_ch_idx, t_ch_name in enumerate(chapter_order):
                            if t_ch_name not in project.chapters:
                                continue
                            for t_frag in project.chapters[t_ch_name].get("fragments", []):
                                if t_frag["id"] == target_fid:
                                    t_node = f"F{t_ch_idx}_{t_frag['name']}"
                                    lines.append(f"    {node_id} -.->|call| {t_node}")
                                    break

    lines.append("")
    lines.append("    %% 变量因果")
    # 变量写入位置
    for ch_idx, ch_name in enumerate(chapter_order):
        if ch_name not in project.chapters:
            continue
        for frag in project.chapters[ch_name].get("fragments", []):
            for b in frag.get("blocks", []):
                if b.get("type") == "setver":
                    key = b.get("props", {}).get("key", "")
                    if key:
                        node_id = f"F{ch_idx}_{frag['name']}"
                        lines.append(f"    {node_id} -.->|write {key}| VAR_{key}[({key})]")

    return "\n".join(lines)


def preview_stats(project: Project) -> str:
    """项目统计"""
    info = project.info()
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  📊 项目统计: {info['name']}")
    lines.append(f"{'='*60}\n")
    lines.append(f"  项目 ID:     {info['id']}")
    lines.append(f"  版本:        {info['version']}")
    lines.append(f"  引擎版本:    {info['engineVersion']}")
    lines.append(f"  作者:        {info['author'] or '(未设置)'}")
    lines.append(f"  画布:        {info['resolution'].get('width')}x{info['resolution'].get('height')}")
    lines.append(f"  章节顺序:    {' → '.join(info['chapterOrder'])}")
    lines.append(f"\n  角色:        {info['characterCount']} 个")
    for c in project.char_list():
        exprs = c.get("expressions", [])
        lines.append(f"    · {c['name']} — {len(exprs)} 表情 — 位置: {c.get('defaultPosition', '?')}")
    lines.append(f"\n  场景:        {info['sceneCount']} 个")
    for s in project.scene_list():
        layers = s.get("layers", [])
        lines.append(f"    · {s['name']} — {len(layers)} 层")
    lines.append(f"\n  变量:        {info['variableCount']} 个")
    for v in project.var_list():
        lines.append(f"    · {v['key']} ({v['displayName']}) — {v['type']} / {v['scope']} / {v['persistence']}")
    lines.append(f"\n  章节:        {info['chapterCount']}")
    lines.append(f"  片段:        {info['fragmentCount']}")
    lines.append(f"  Block 总数:  {info['blockCount']}")
    lines.append(f"\n{'='*60}\n")
    return "\n".join(lines)
