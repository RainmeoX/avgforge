"""
AVGForge Schema — LetsGal Studio 项目格式定义
完全兼容官方格式，可直接导入 LetsGal Studio 预览。
"""
import uuid
import time
from typing import Any, Dict, List, Optional


def gen_id() -> str:
    """生成 UUID v4"""
    return str(uuid.uuid4())


def now_ms() -> int:
    """当前时间戳（毫秒）"""
    return int(time.time() * 1000)


# ============================================================
# 项目配置
# ============================================================

def default_project(name: str, author: str = "", description: str = "") -> Dict:
    """生成标准 project.json"""
    return {
        "id": gen_id(),
        "version": "1.0.0",
        "engineVersion": "1.0.0",
        "name": name,
        "description": description,
        "author": author,
        "resolution": {"width": 1920, "height": 1080},
        "backgroundColor": "#000",
        "window": {
            "lockAspectRatio": False,
            "allowMaximize": True,
            "allowFullscreen": True,
            "launchMode": "windowed"
        },
        "cursor": {
            "mode": "system",
            "image": "",
            "imagePixelRatio": 1,
            "imageSize": {"width": 24, "height": 24},
            "hotspot": {"x": 0, "y": 0},
            "fallback": "default",
            "css": "",
            "cssImagePixelRatio": 1,
            "cssImageSize": {"width": 24, "height": 24}
        },
        "chapterOrder": ["开始"],
        "extensionStorageVersion": 1,
        "extensions": {
            "avg.internal.default-shell": {
                "enabled": True,
                "bundle": {"version": "1.0.0"}
            }
        },
        "extensionSettings": {},
        "systemBindings": {
            "internal.system.title":    "ui:@avg.internal.default-shell/title-screen",
            "internal.system.save":     "ui:@avg.internal.default-shell/save-screen",
            "internal.system.load":     "ui:@avg.internal.default-shell/save-screen",
            "internal.system.settings": "ui:@avg.internal.default-shell/settings-screen",
            "internal.system.history":  "ui:@avg.internal.default-shell/history-screen",
            "internal.system.gallery":  "ui:@avg.internal.default-shell/gallery-screen",
            "internal.system.input":    "ui:@avg.internal.default-shell/input-dialog"
        },
        "actionBindings": {
            "internal.input.advance": ["mousedown", " ", "Enter", "wheeldown"],
            "internal.input.skip": ["Control"],
            "internal.input.auto-toggle": ["a"],
            "internal.input.hide-dialogue": ["contextmenu", "Delete"],
            "internal.input.replay-voice": ["r"],
            "avg.internal.default-shell.quick-save": ["F5"],
            "avg.internal.default-shell.quick-load": ["F9"],
            "avg.internal.default-shell.open-history": ["middleclick"]
        }
    }


# ============================================================
# 变量定义
# ============================================================

def default_variables() -> Dict:
    """生成标准 project.variables.json"""
    return {
        "version": 2,
        "variables": []
    }


def make_variable(key: str, display_name: str, var_type: str = "number",
                  scope: str = "project", persistence: str = "slot",
                  default: Any = 0, description: str = "") -> Dict:
    """创建变量定义"""
    return {
        "key": key,
        "displayName": display_name,
        "type": var_type,  # number / boolean / string
        "scope": scope,    # project / system
        "persistence": persistence,  # slot / shared
        "defaultValue": default,
        "description": description
    }


# ============================================================
# 角色配置
# ============================================================

DEFAULT_POSITIONS = [
    {"id": "left",         "name": "左",   "left": 2,  "top": 2},
    {"id": "center-left",  "name": "中左", "left": 19, "top": 2},
    {"id": "center",       "name": "中",   "left": 35, "top": 2},
    {"id": "center-right", "name": "中右", "left": 55, "top": 2},
    {"id": "right",        "name": "右",   "left": 68, "top": 2},
]


def default_characters() -> Dict:
    """生成标准 characters.json"""
    return {
        "version": 2,
        "globalSettings": {
            "defaultPosition": "left",
            "graphics": {
                "keepAspectRatio": True,
                "size": "(30%,30%)"
            },
            "positions": [p.copy() for p in DEFAULT_POSITIONS],
            "defaultPositionId": "center",
            "defaultAnchor": "left_top"
        },
        "attributeTemplate": [],
        "characters": []
    }


def make_character(name: str, position: str = "center",
                   color_ring: str = "#7fd4c8", color_bg: str = "#1a2e2c",
                   color_fg: str = "#7fd4c8") -> Dict:
    """创建角色"""
    return {
        "id": gen_id(),
        "name": name,
        "expressions": [],
        "defaultPosition": position,
        "themeColor": {
            "bg": color_bg,
            "fg": color_fg,
            "ring": color_ring
        },
        "graphics": {"size": "(100%,100%)"},
        "attributeValues": {}
    }


def make_expression(name: str, asset_path: str,
                    avatar_crop: Optional[Dict] = None) -> Dict:
    """创建表情"""
    expr = {
        "name": name,
        "assetPath": asset_path
    }
    if avatar_crop:
        expr["avatarCrop"] = avatar_crop
    return expr


# ============================================================
# 场景配置
# ============================================================

def default_scenes() -> Dict:
    """生成标准 scenes.json"""
    return {
        "version": 3,
        "scenes": [],
        "groups": [],
        "layout": []
    }


def make_scene(name: str, layers: List[Dict]) -> Dict:
    """创建场景"""
    return {
        "id": gen_id(),
        "name": name,
        "layers": layers
    }


def make_layer(name: str, asset_path: str, distance: float = 1.0) -> Dict:
    """创建场景图层"""
    return {
        "id": gen_id(),
        "name": name,
        "assetPath": asset_path,
        "distance": distance
    }


# ============================================================
# 章节与片段
# ============================================================

def default_chapter(name: str) -> Dict:
    """生成标准章节"""
    return {
        "id": gen_id(),
        "name": name,
        "fragments": [
            {
                "id": gen_id(),
                "name": "main",
                "blocks": []
            }
        ]
    }


def make_fragment(name: str) -> Dict:
    """创建片段"""
    return {
        "id": gen_id(),
        "name": name,
        "blocks": []
    }


# ============================================================
# Block 生成器（25 种类型）
# ============================================================

def make_block(block_type: str, props: Optional[Dict] = None,
               content: Optional[List] = None) -> Dict:
    """创建 block"""
    block = {
        "type": block_type,
        "props": {"disabled": False},
        "id": gen_id()
    }
    if props:
        block["props"].update(props)
    if content:
        block["content"] = content
    return block


def make_dialogue(character_id: str, character_name: str, text: str,
                  expression: str = "", position: str = "",
                  is_first: bool = False, is_last: bool = False,
                  show_character: bool = True, keep_character: bool = True,
                  keep_dialogue: bool = True) -> Dict:
    """对白 block"""
    return make_block("dialogue", {
        "characterId": character_id,
        "characterName": character_name,
        "expression": expression,
        "position": position,
        "isFirst": is_first,
        "isLast": is_last,
        "showCharacter": show_character,
        "keepCharacter": keep_character,
        "keepDialogue": keep_dialogue,
        "voiceHash": ""
    }, [{"type": "text", "text": text, "styles": {}}])


def make_narration(text: str, keep_dialogue: bool = True) -> Dict:
    """旁白 block"""
    return make_block("narration", {
        "keepDialogue": keep_dialogue,
        "voiceHash": ""
    }, [{"type": "text", "text": text, "styles": {}}])


def make_scene_block(scene_id: str, scene_name: str,
                     transition_mode: str = "fade",
                     transition_duration: str = "500") -> Dict:
    """场景切换 block"""
    return make_block("scene", {
        "sceneId": scene_id,
        "sceneName": scene_name,
        "uri": "",
        "transitionMode": transition_mode,
        "transitionDuration": transition_duration,
        "waitForComplete": "false",
        "resetCamera": "false",
        "displayType": "cover",
        "position": "(50%,50%)",
        "anchor": "center",
        "size": ""
    })


def make_curtain(op: str = "open", duration: str = "1000",
                 color: str = "#000000", mode: str = "full-screen",
                 curtain_size: str = "100") -> Dict:
    """幕布 block (op: open/close)"""
    return make_block("curtain", {
        "op": op,
        "effect": "",
        "duration": duration,
        "color": color,
        "mode": mode,
        "curtainSize": curtain_size
    })


def make_wait(duration: str = "1000") -> Dict:
    """等待 block"""
    return make_block("wait", {"duration": duration})


def make_sound(sound_type: str = "BGM", uri: str = "", volume: str = "100",
               loop: bool = False, fade_duration: str = "") -> Dict:
    """音频 block (sound_type: BGM/SE/VOICE)"""
    return make_block("sound", {
        "soundType": sound_type,
        "soundId": "",
        "uri": uri,
        "volume": volume,
        "loop": str(loop).lower(),
        "fadeDuration": fade_duration
    })


def make_stop_sound(sound_type: str = "BGM", fade_duration: str = "800") -> Dict:
    """停止音频 block"""
    return make_block("stopSound", {
        "soundType": sound_type,
        "soundId": "",
        "fadeDuration": fade_duration
    })


def make_branch(title: str, choices: List[Dict]) -> Dict:
    """分支 block
    choices: [{"text": "选项1", "mode": "jump", "fragmentId": "xxx"}, ...]
    """
    import json
    return make_block("branch", {
        "branchId": gen_id(),
        "title": title,
        "choices": json.dumps(choices, ensure_ascii=False)
    })


def make_call_fragment(fragment_id: str) -> Dict:
    """调用片段 block"""
    return make_block("callFragment", {
        "fragmentId": fragment_id
    })


def make_camera(offset_x: str = "", offset_y: str = "", zoom: str = "",
                duration: str = "0", easing: str = "easeInOut",
                wait_for_complete: bool = False) -> Dict:
    """镜头 block"""
    return make_block("camera", {
        "offsetX": offset_x,
        "offsetY": offset_y,
        "zoom": zoom,
        "focalDistance": "",
        "blurStrength": "",
        "duration": duration,
        "easing": easing,
        "waitForComplete": str(wait_for_complete).lower(),
        "targets": "scene,characters",
        "distortionStrength": "",
        "vignetteIntensity": "",
        "vignetteSize": "",
        "blurAmount": "",
        "colorToneMode": "none",
        "colorToneIntensity": "",
        "oldFilmIntensity": "",
        "shockIntensity": "",
        "lutPreset": "",
        "lutIntensity": "",
        "shakeAmplitude": "",
        "shakeFrequency": "",
        "shakeDuration": "",
        "shakeFalloff": "linear",
        "shakeAxis": "both"
    })


def make_reset_camera() -> Dict:
    """重置镜头 block"""
    return make_block("resetCamera", {})


def make_particle(mode: str = "show", preset: str = "LIGHT_SNOW",
                  texture_uri: str = "particles/snow.png",
                  fade_in: str = "500", fade_out: str = "500") -> Dict:
    """粒子 block (mode: show/hide)"""
    return make_block("particle", {
        "mode": mode,
        "effectId": gen_id(),
        "preset": preset,
        "textureUri": texture_uri,
        "optionsJson": "",
        "fadeInDuration": fade_in,
        "fadeOutDuration": fade_out
    })


def make_floating_text(text: str, position: str = "(50%,50%)",
                       font_size: str = "42", color: str = "#ffffff",
                       duration: str = "2500", anim_in: str = "fade",
                       anim_out: str = "fade") -> Dict:
    """浮动文字 block"""
    return make_block("floatingText", {
        "floatingTextId": "",
        "blocking": "true",
        "recordHistory": "false",
        "position": position,
        "anchor": "center",
        "size": "",
        "fontFamily": "",
        "fontSize": font_size,
        "color": color,
        "fontWeight": "normal",
        "fontStyle": "normal",
        "textAlign": "left",
        "lineHeight": "",
        "letterSpacing": "",
        "textShadow": "2px 2px 4px rgba(0,0,0,0.5)",
        "duration": duration,
        "animIn": anim_in,
        "inDuration": "3000",
        "animOut": anim_out,
        "outDuration": "3000",
        "slideFrom": "top",
        "slideDistance": "40",
        "scaleFrom": "0.8",
        "scaleTo": "0.8",
        "blurRadius": "8"
    }, [{"type": "text", "text": text, "styles": {}}])


def make_setver(key: str, op: str = "set", value: Any = 0,
                value_type: str = "literal") -> Dict:
    """变量赋值 block
    op: set/add/sub/mul/div
    value_type: literal/variable
    """
    return make_block("setver", {
        "key": key,
        "op": op,
        "aKind": "variable",
        "aLit": "",
        "aVar": key,
        "bKind": value_type,
        "bLit": str(value),
        "bVar": "",
        "binOp": ""
    })


def make_remove_character(character_id: str, character_name: str = "") -> Dict:
    """移除角色 block"""
    return make_block("removeCharacter", {
        "characterId": character_id,
        "characterName": character_name
    })


def make_destroy_scene(scene_id: str = "", scene_name: str = "",
                       animated: bool = True, wait: bool = True) -> Dict:
    """销毁场景 block"""
    return make_block("destroyScene", {
        "sceneId": scene_id,
        "sceneName": scene_name,
        "animated": str(animated).lower(),
        "waitForComplete": str(wait).lower()
    })


def make_comment(text: str) -> Dict:
    """注释 block（不渲染）"""
    return make_block("comment", {}, [{"type": "text", "text": text, "styles": {}}])


def make_video(uri: str, video_id: str = "", loop: bool = False,
               muted: bool = False, alpha: str = "1",
               wait: bool = False, mode: str = "play") -> Dict:
    """视频 block"""
    return make_block("video", {
        "videoId": video_id or gen_id(),
        "uri": uri,
        "loop": str(loop).lower(),
        "muted": str(muted).lower(),
        "alpha": alpha,
        "waitForFinished": str(wait).lower(),
        "mode": mode
    })


def make_stop_video(video_id: str, fade_out: str = "500") -> Dict:
    """停止视频 block"""
    return make_block("stopVideo", {
        "videoId": video_id,
        "fadeOutDuration": fade_out
    })


def make_end(title: str, text: str, ending_type: str = "normal") -> Dict:
    """结局 block（自定义扩展类型，用于标记结局）"""
    return make_block("comment", {
        "_endingType": ending_type,
        "_endingTitle": title
    }, [{"type": "text", "text": f"[END:{ending_type}] {title}\n{text}", "styles": {}}])


# ============================================================
# Block 类型注册表
# ============================================================

BLOCK_TYPES = {
    "dialogue":         {"name": "对白",       "category": "文本",   "factory": make_dialogue},
    "narration":        {"name": "旁白",       "category": "文本",   "factory": make_narration},
    "floatingText":     {"name": "浮动文字",   "category": "文本",   "factory": make_floating_text},
    "comment":          {"name": "注释",       "category": "文本",   "factory": make_comment},
    "scene":            {"name": "场景切换",   "category": "场景",   "factory": make_scene_block},
    "destroyScene":     {"name": "销毁场景",   "category": "场景",   "factory": make_destroy_scene},
    "curtain":          {"name": "幕布",       "category": "场景",   "factory": make_curtain},
    "removeCharacter":  {"name": "移除角色",   "category": "角色",   "factory": make_remove_character},
    "camera":           {"name": "镜头",       "category": "演出",   "factory": make_camera},
    "resetCamera":      {"name": "重置镜头",   "category": "演出",   "factory": make_reset_camera},
    "particle":         {"name": "粒子",       "category": "演出",   "factory": make_particle},
    "sound":            {"name": "音频",       "category": "音频",   "factory": make_sound},
    "stopSound":        {"name": "停止音频",   "category": "音频",   "factory": make_stop_sound},
    "video":            {"name": "视频",       "category": "音频",   "factory": make_video},
    "stopVideo":        {"name": "停止视频",   "category": "音频",   "factory": make_stop_video},
    "wait":             {"name": "等待",       "category": "流程",   "factory": make_wait},
    "branch":           {"name": "分支",       "category": "流程",   "factory": make_branch},
    "callFragment":     {"name": "调用片段",   "category": "流程",   "factory": make_call_fragment},
    "setver":           {"name": "变量赋值",   "category": "变量",   "factory": make_setver},
}
