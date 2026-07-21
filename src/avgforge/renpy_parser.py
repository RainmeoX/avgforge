"""
AVGForge Ren'Py 风格剧本解析器
支持官方文档列出的核心语法，解析为 LetsGal Studio Block 格式。
"""
import re
from typing import Dict, List, Optional, Tuple

from . import schema
from .project import Project


class RenpyParser:
    """Ren'Py 风格剧本解析器"""

    def __init__(self, project: Project):
        self.project = project
        # 角色名 -> character dict
        self.char_by_name = {c["name"]: c for c in project.char_list()}
        # 场景名 -> scene dict
        self.scene_by_name = {s["name"]: s for s in project.scene_list()}
        # 变量 key -> variable dict
        self.var_by_key = {v["key"]: v for v in project.var_list()}

    def parse(self, text: str, chapter_name: str,
              frag_name: str = "main") -> List[Dict]:
        """解析 Ren'Py 风格文本为 block 列表"""
        lines = text.split("\n")
        blocks: List[Dict] = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()
            stripped = line.strip()

            # 跳过空行和注释
            if not stripped or stripped.startswith("#"):
                i += 1
                continue

            # 解析各种语句
            block, consumed = self._parse_line(stripped, lines, i)
            if block:
                if isinstance(block, list):
                    blocks.extend(block)
                else:
                    blocks.append(block)
            i += consumed

        return blocks

    def _parse_line(self, line: str, lines: List[str],
                    idx: int) -> Tuple[Optional[object], int]:
        """解析单行，返回 (block 或 blocks, 消耗的行数)"""

        # scene <场景名> [with <过渡>] [duration <秒>]
        m = re.match(r'scene\s+(\S+)(?:\s+with\s+(\w+))?(?:\s+duration\s+([\d.]+))?', line)
        if m:
            scene_name = m.group(1)
            transition = m.group(2) or "fade"
            duration = m.group(3) or "0.5"
            scene = self.scene_by_name.get(scene_name)
            if not scene:
                raise ValueError(f"场景不存在: {scene_name}")
            duration_ms = str(int(float(duration) * 1000))
            return schema.make_scene_block(scene["id"], scene["name"],
                                            transition, duration_ms), 1

        # show <角色> [表情] [at <位置>]
        # 注意：'at' 是位置关键字，不是表情
        m = re.match(r'show\s+(\S+)(?:\s+at\s+(\S+))?(?:\s+(\S+))?', line)
        if m:
            char_name = m.group(1)
            position = m.group(2) or ""
            expression = m.group(3) or ""
            char = self.char_by_name.get(char_name)
            if not char:
                raise ValueError(f"角色不存在: {char_name}")
            # show 单独使用时，作为"显示角色"标记，下一个对白会使用
            # 这里用一个空对白 block 来触发显示
            return schema.make_dialogue(
                char["id"], char["name"], "", expression, position,
                is_first=True, show_character=True, keep_character=True,
                keep_dialogue=False
            ), 1

        # hide <角色>
        m = re.match(r'hide\s+(\S+)', line)
        if m:
            char_name = m.group(1)
            char = self.char_by_name.get(char_name)
            if not char:
                raise ValueError(f"角色不存在: {char_name}")
            return schema.make_remove_character(char["id"], char["name"]), 1

        # play music|sound|voice <文件> [volume <n>%] [loop] [fadein <秒>]
        m = re.match(r'play\s+(music|sound|voice)\s+(\S+)(?:\s+volume\s+(\d+)%?)?(?:\s+(loop))?(?:\s+fadein\s+([\d.]+))?', line)
        if m:
            sound_type = {"music": "BGM", "sound": "SE", "voice": "VOICE"}[m.group(1)]
            uri = m.group(2)
            volume = m.group(3) or "100"
            loop = bool(m.group(4))
            fade = m.group(5)
            fade_ms = str(int(float(fade) * 1000)) if fade else ""
            return schema.make_sound(sound_type, uri, volume, loop, fade_ms), 1

        # stop music|sound
        m = re.match(r'stop\s+(music|sound|voice)', line)
        if m:
            sound_type = {"music": "BGM", "sound": "SE", "voice": "VOICE"}[m.group(1)]
            return schema.make_stop_sound(sound_type), 1

        # pause <秒>
        m = re.match(r'pause\s+([\d.]+)', line)
        if m:
            duration_ms = str(int(float(m.group(1)) * 1000))
            return schema.make_wait(duration_ms), 1

        # $ <变量> = <值>  或  $ <变量> += <值>
        m = re.match(r'\$\s+(\w+)\s*(\+=|-=|\*=|/=|=)\s*(.+)', line)
        if m:
            key = m.group(1)
            op_sym = m.group(2)
            value = m.group(3).strip()
            op_map = {"=": "set", "+=": "add", "-=": "sub", "*=": "mul", "/=": "div"}
            op = op_map[op_sym]
            # 尝试解析值
            try:
                if "." in value:
                    val = float(value)
                else:
                    val = int(value)
            except ValueError:
                val = value.strip('"\'')
            return schema.make_setver(key, op, val), 1

        # camera x <n> y <n> zoom <n> duration <秒> [easing <word>]
        m = re.match(r'camera\s+(.*)', line)
        if m:
            params = m.group(1)
            offset_x = offset_y = zoom = duration = easing = ""
            m2 = re.search(r'x\s+(-?[\d.]+)', params)
            if m2: offset_x = m2.group(1)
            m2 = re.search(r'y\s+(-?[\d.]+)', params)
            if m2: offset_y = m2.group(1)
            m2 = re.search(r'zoom\s+([\d.]+)', params)
            if m2: zoom = m2.group(1)
            m2 = re.search(r'duration\s+([\d.]+)', params)
            if m2: duration = str(int(float(m2.group(1)) * 1000))
            m2 = re.search(r'easing\s+(\w+)', params)
            if m2: easing = m2.group(1)
            return schema.make_camera(offset_x, offset_y, zoom,
                                       duration, easing or "easeInOut"), 1

        # particle show|hide <PRESET>
        m = re.match(r'particle\s+(show|hide)\s+(\w+)', line)
        if m:
            mode = m.group(1)
            preset = m.group(2)
            texture = {"LIGHT_SNOW": "particles/snow.png",
                       "SAKURA": "particles/sakura.png",
                       "STAR": "particles/star.png"}.get(preset, "particles/snow.png")
            return schema.make_particle(mode, preset, texture), 1

        # curtain open|close [duration <秒>] [color <#hex>]
        m = re.match(r'curtain\s+(open|close)(?:\s+duration\s+([\d.]+))?(?:\s+color\s+(#\w+))?', line)
        if m:
            op = m.group(1)
            duration = str(int(float(m.group(2)) * 1000)) if m.group(2) else "1000"
            color = m.group(3) or "#000000"
            return schema.make_curtain(op, duration, color), 1

        # float "<文本>" [position <x%,y%>] [duration <秒>]
        m = re.match(r'float\s+"([^"]+)"(?:\s+position\s+\(([\d.]+)%,([\d.]+)%\))?(?:\s+duration\s+([\d.]+))?', line)
        if m:
            text = m.group(1)
            pos = f"({m.group(2) or '50'}%,{m.group(3) or '50'}%)"
            duration = str(int(float(m.group(4)) * 1000)) if m.group(4) else "2500"
            return schema.make_floating_text(text, pos, duration=duration), 1

        # call <片段名>
        m = re.match(r'call\s+(\S+)', line)
        if m:
            frag_name = m.group(1)
            # 查找片段
            for ch in self.project.chapters.values():
                for f in ch.get("fragments", []):
                    if f["name"] == frag_name:
                        return schema.make_call_fragment(f["id"]), 1
            raise ValueError(f"片段不存在: {frag_name}")

        # menu "标题":
        #   "选项1" -> call <片段>
        #   "选项2" -> $ <变量> += 1
        m = re.match(r'menu\s+"([^"]+)":', line)
        if m:
            title = m.group(1)
            choices = []
            consumed = 1
            j = idx + 1
            while j < len(lines):
                cline = lines[j].strip()
                if not cline or cline.startswith("#"):
                    j += 1
                    consumed += 1
                    continue
                # 选项行: "文本" -> call <片段>  或  "文本" -> $ <赋值>
                cm = re.match(r'"([^"]+)"\s*->\s+(.+)', cline)
                if cm:
                    choice_text = cm.group(1)
                    action = cm.group(2).strip()
                    if action.startswith("call "):
                        target_frag = action[5:].strip()
                        for ch in self.project.chapters.values():
                            for f in ch.get("fragments", []):
                                if f["name"] == target_frag:
                                    choices.append({
                                        "mode": "jump",
                                        "text": choice_text,
                                        "fragmentId": f["id"]
                                    })
                                    break
                            else:
                                continue
                            break
                    elif action.startswith("$ "):
                        # 变量赋值选项 - 暂时用 jump 到 main
                        choices.append({
                            "mode": "jump",
                            "text": choice_text,
                            "fragmentId": ""
                        })
                    j += 1
                    consumed += 1
                else:
                    break
            return schema.make_branch(title, choices), consumed

        # 角色 "台词"
        m = re.match(r'(\S+)\s+"(.+)"', line)
        if m:
            char_name = m.group(1)
            text = m.group(2)
            char = self.char_by_name.get(char_name)
            if not char:
                raise ValueError(f"角色不存在: {char_name}")
            return schema.make_dialogue(char["id"], char["name"], text), 1

        # 纯旁白（引号包裹的文本）
        m = re.match(r'"(.+)"', line)
        if m:
            return schema.make_narration(m.group(1)), 1

        # 无引号旁白（以"旁白:"开头）
        m = re.match(r'旁白[:：]\s*(.+)', line)
        if m:
            return schema.make_narration(m.group(1)), 1

        # 其他无引号文本作为旁白
        if not line.startswith(("$", "scene", "show", "hide", "play", "stop",
                                  "pause", "camera", "particle", "curtain",
                                  "float", "call", "menu")):
            return schema.make_narration(line), 1

        return None, 1

    def serialize(self, blocks: List[Dict]) -> str:
        """将 block 列表序列化为 Ren'Py 风格文本"""
        lines = []
        for b in blocks:
            btype = b.get("type", "")
            props = b.get("props", {})
            content = b.get("content", [])
            text = content[0].get("text", "") if content else ""

            if btype == "narration":
                lines.append(f'"{text}"')
            elif btype == "dialogue":
                char_name = props.get("characterName", "")
                expression = props.get("expression", "")
                if expression:
                    lines.append(f'show {char_name} {expression}')
                lines.append(f'{char_name} "{text}"')
            elif btype == "scene":
                scene_name = props.get("sceneName", "")
                duration_ms = int(props.get("transitionDuration", "500"))
                duration_s = duration_ms / 1000
                lines.append(f'scene {scene_name} with fade duration {duration_s}')
            elif btype == "curtain":
                op = props.get("op", "open")
                duration_ms = int(props.get("duration", "1000"))
                lines.append(f'curtain {op} duration {duration_ms/1000}')
            elif btype == "wait":
                duration_ms = int(props.get("duration", "1000"))
                lines.append(f'pause {duration_ms/1000}')
            elif btype == "sound":
                sound_type = props.get("soundType", "BGM")
                uri = props.get("uri", "")
                type_map = {"BGM": "music", "SE": "sound", "VOICE": "voice"}
                lines.append(f'play {type_map.get(sound_type, "sound")} {uri}')
            elif btype == "stopSound":
                sound_type = props.get("soundType", "BGM")
                type_map = {"BGM": "music", "SE": "sound", "VOICE": "voice"}
                lines.append(f'stop {type_map.get(sound_type, "sound")}')
            elif btype == "camera":
                params = []
                if props.get("offsetX"): params.append(f'x {props["offsetX"]}')
                if props.get("offsetY"): params.append(f'y {props["offsetY"]}')
                if props.get("zoom"): params.append(f'zoom {props["zoom"]}')
                if props.get("duration"): params.append(f'duration {int(props["duration"])/1000}')
                lines.append(f'camera {" ".join(params)}')
            elif btype == "particle":
                mode = props.get("mode", "show")
                preset = props.get("preset", "LIGHT_SNOW")
                lines.append(f'particle {mode} {preset}')
            elif btype == "floatingText":
                lines.append(f'float "{text}"')
            elif btype == "setver":
                key = props.get("key", "")
                op = props.get("op", "set")
                val = props.get("bLit", "")
                op_map = {"set": "=", "add": "+=", "sub": "-=", "mul": "*=", "div": "/="}
                lines.append(f'$ {key} {op_map.get(op, "=")} {val}')
            elif btype == "branch":
                title = props.get("title", "")
                lines.append(f'menu "{title}":')
                import json
                choices = props.get("choices", "[]")
                if isinstance(choices, str):
                    choices = json.loads(choices)
                for c in choices:
                    lines.append(f'    "{c.get("text", "")}" -> call {c.get("fragmentId", "")}')
            elif btype == "callFragment":
                fid = props.get("fragmentId", "")
                for ch in self.project.chapters.values():
                    for f in ch.get("fragments", []):
                        if f["id"] == fid:
                            lines.append(f'call {f["name"]}')
                            break
            elif btype == "removeCharacter":
                char_name = props.get("characterName", "")
                lines.append(f'hide {char_name}')
            elif btype == "comment":
                lines.append(f'# {text}')

        return "\n".join(lines)
