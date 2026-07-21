"""
AVGForge 项目操作 — 读写 LetsGal Studio 标准项目文件
"""
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import schema


class Project:
    """LetsGal Studio 项目操作类"""

    def __init__(self, path: str):
        self.path = Path(path).resolve()
        self.project: Dict = {}
        self.variables: Dict = {}
        self.characters: Dict = {}
        self.scenes: Dict = {}
        self.chapters: Dict[str, Dict] = {}  # name -> chapter data

    # ============================================================
    # 加载与保存
    # ============================================================

    def load(self) -> None:
        """加载项目"""
        if not self.path.is_dir():
            raise FileNotFoundError(f"项目目录不存在: {self.path}")

        # project.json
        pj = self.path / "project.json"
        if not pj.exists():
            raise FileNotFoundError(f"缺少 project.json: {pj}")
        with open(pj, encoding="utf-8") as f:
            self.project = json.load(f)

        # project.variables.json
        pv = self.path / "project.variables.json"
        self.variables = json.load(open(pv, encoding="utf-8")) if pv.exists() else schema.default_variables()

        # characters.json
        cf = self.path / "characters.json"
        self.characters = json.load(open(cf, encoding="utf-8")) if cf.exists() else schema.default_characters()

        # scenes.json
        sf = self.path / "scenes.json"
        self.scenes = json.load(open(sf, encoding="utf-8")) if sf.exists() else schema.default_scenes()

        # chapters/
        ch_dir = self.path / "chapters"
        if ch_dir.exists():
            for f in ch_dir.glob("*.json"):
                with open(f, encoding="utf-8") as fp:
                    data = json.load(fp)
                    self.chapters[data["name"]] = data

    def save(self) -> None:
        """保存项目"""
        self.path.mkdir(parents=True, exist_ok=True)

        # project.json
        with open(self.path / "project.json", "w", encoding="utf-8") as f:
            json.dump(self.project, f, ensure_ascii=False, indent=2)

        # project.variables.json
        with open(self.path / "project.variables.json", "w", encoding="utf-8") as f:
            json.dump(self.variables, f, ensure_ascii=False, indent=2)

        # characters.json
        with open(self.path / "characters.json", "w", encoding="utf-8") as f:
            json.dump(self.characters, f, ensure_ascii=False, indent=2)

        # scenes.json
        with open(self.path / "scenes.json", "w", encoding="utf-8") as f:
            json.dump(self.scenes, f, ensure_ascii=False, indent=2)

        # chapters/
        ch_dir = self.path / "chapters"
        ch_dir.mkdir(exist_ok=True)
        for name, data in self.chapters.items():
            with open(ch_dir / f"{name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        # assets/
        for sub in ["backgrounds", "characters", "bgm", "se", "voice", "video", "particles", "fonts", "ui"]:
            (self.path / "assets" / sub).mkdir(parents=True, exist_ok=True)

        # config/personalization/
        (self.path / "config" / "personalization").mkdir(parents=True, exist_ok=True)
        active = self.path / "config" / "personalization" / "active.json"
        if not active.exists():
            with open(active, "w", encoding="utf-8") as f:
                json.dump({}, f)

    # ============================================================
    # 项目信息
    # ============================================================

    def info(self) -> Dict:
        """获取项目统计信息"""
        total_blocks = 0
        total_fragments = 0
        for ch in self.chapters.values():
            for frag in ch.get("fragments", []):
                total_fragments += 1
                total_blocks += len(frag.get("blocks", []))
        return {
            "name": self.project.get("name", ""),
            "id": self.project.get("id", ""),
            "version": self.project.get("version", ""),
            "engineVersion": self.project.get("engineVersion", ""),
            "author": self.project.get("author", ""),
            "description": self.project.get("description", ""),
            "resolution": self.project.get("resolution", {}),
            "chapterOrder": self.project.get("chapterOrder", []),
            "characterCount": len(self.characters.get("characters", [])),
            "sceneCount": len(self.scenes.get("scenes", [])),
            "variableCount": len(self.variables.get("variables", [])),
            "chapterCount": len(self.chapters),
            "fragmentCount": total_fragments,
            "blockCount": total_blocks,
        }

    # ============================================================
    # 角色操作
    # ============================================================

    def char_add(self, name: str, position: str = "center",
                 color_ring: str = "#7fd4c8", color_bg: str = "#1a2e2c",
                 color_fg: str = "#7fd4c8") -> Dict:
        """添加角色"""
        char = schema.make_character(name, position, color_ring, color_bg, color_fg)
        self.characters.setdefault("characters", []).append(char)
        return char

    def char_list(self) -> List[Dict]:
        """列出角色"""
        return self.characters.get("characters", [])

    def char_get(self, identifier: str) -> Optional[Dict]:
        """按 id 或 name 获取角色"""
        for c in self.char_list():
            if c["id"] == identifier or c["name"] == identifier:
                return c
        return None

    def char_remove(self, identifier: str) -> bool:
        """删除角色"""
        chars = self.characters.get("characters", [])
        for i, c in enumerate(chars):
            if c["id"] == identifier or c["name"] == identifier:
                chars.pop(i)
                return True
        return False

    def char_add_expression(self, identifier: str, expr_name: str,
                            asset_path: str) -> bool:
        """为角色添加表情"""
        char = self.char_get(identifier)
        if not char:
            return False
        char.setdefault("expressions", []).append(
            schema.make_expression(expr_name, asset_path)
        )
        return True

    # ============================================================
    # 场景操作
    # ============================================================

    def scene_add(self, name: str, layers: List[Dict]) -> Dict:
        """添加场景"""
        scene = schema.make_scene(name, layers)
        self.scenes.setdefault("scenes", []).append(scene)
        return scene

    def scene_list(self) -> List[Dict]:
        return self.scenes.get("scenes", [])

    def scene_get(self, identifier: str) -> Optional[Dict]:
        for s in self.scene_list():
            if s["id"] == identifier or s["name"] == identifier:
                return s
        return None

    def scene_remove(self, identifier: str) -> bool:
        scenes = self.scenes.get("scenes", [])
        for i, s in enumerate(scenes):
            if s["id"] == identifier or s["name"] == identifier:
                scenes.pop(i)
                return True
        return False

    # ============================================================
    # 章节操作
    # ============================================================

    def chapter_add(self, name: str) -> Dict:
        """添加章节"""
        if name in self.chapters:
            raise ValueError(f"章节已存在: {name}")
        ch = schema.default_chapter(name)
        self.chapters[name] = ch
        if name not in self.project.get("chapterOrder", []):
            self.project.setdefault("chapterOrder", []).append(name)
        return ch

    def chapter_list(self) -> List[str]:
        return list(self.chapters.keys())

    def chapter_remove(self, name: str) -> bool:
        if name == "开始":
            raise ValueError("入口章节'开始'不能删除")
        if name not in self.chapters:
            return False
        del self.chapters[name]
        if name in self.project.get("chapterOrder", []):
            self.project["chapterOrder"].remove(name)
        return True

    def chapter_reorder(self, order: List[str]) -> None:
        """重排章节顺序"""
        for name in order:
            if name not in self.chapters:
                raise ValueError(f"章节不存在: {name}")
        self.project["chapterOrder"] = order

    # ============================================================
    # Fragment 操作
    # ============================================================

    def frag_add(self, chapter_name: str, frag_name: str) -> Dict:
        """添加片段"""
        if chapter_name not in self.chapters:
            raise ValueError(f"章节不存在: {chapter_name}")
        frag = schema.make_fragment(frag_name)
        self.chapters[chapter_name].setdefault("fragments", []).append(frag)
        return frag

    def frag_list(self, chapter_name: str) -> List[Dict]:
        return self.chapters.get(chapter_name, {}).get("fragments", [])

    def frag_get(self, chapter_name: str, frag_identifier: str) -> Optional[Dict]:
        """按 id 或 name 获取片段"""
        for f in self.frag_list(chapter_name):
            if f["id"] == frag_identifier or f["name"] == frag_identifier:
                return f
        return None

    def frag_remove(self, chapter_name: str, frag_identifier: str) -> bool:
        frags = self.chapters.get(chapter_name, {}).get("fragments", [])
        for i, f in enumerate(frags):
            if f["id"] == frag_identifier or f["name"] == frag_identifier:
                if f["name"] == "main":
                    raise ValueError("main 片段不能删除")
                frags.pop(i)
                return True
        return False

    # ============================================================
    # Block 操作
    # ============================================================

    def block_add(self, chapter_name: str, frag_identifier: str,
                  block: Dict, position: int = -1) -> bool:
        """添加 block 到片段"""
        frag = self.frag_get(chapter_name, frag_identifier)
        if not frag:
            return False
        blocks = frag.setdefault("blocks", [])
        if position < 0 or position >= len(blocks):
            blocks.append(block)
        else:
            blocks.insert(position, block)
        return True

    def block_list(self, chapter_name: str, frag_identifier: str) -> List[Dict]:
        frag = self.frag_get(chapter_name, frag_identifier)
        return frag.get("blocks", []) if frag else []

    def block_remove(self, chapter_name: str, frag_identifier: str,
                     block_id: str) -> bool:
        frag = self.frag_get(chapter_name, frag_identifier)
        if not frag:
            return False
        blocks = frag.get("blocks", [])
        for i, b in enumerate(blocks):
            if b.get("id") == block_id:
                blocks.pop(i)
                return True
        return False

    def block_move(self, chapter_name: str, frag_identifier: str,
                   block_id: str, new_position: int) -> bool:
        frag = self.frag_get(chapter_name, frag_identifier)
        if not frag:
            return False
        blocks = frag.get("blocks", [])
        idx = next((i for i, b in enumerate(blocks) if b.get("id") == block_id), -1)
        if idx < 0:
            return False
        block = blocks.pop(idx)
        new_position = max(0, min(new_position, len(blocks)))
        blocks.insert(new_position, block)
        return True

    # ============================================================
    # 变量操作
    # ============================================================

    def var_add(self, key: str, display_name: str, var_type: str = "number",
                scope: str = "project", persistence: str = "slot",
                default: Any = 0, description: str = "") -> Dict:
        """添加变量"""
        for v in self.variables.get("variables", []):
            if v["key"] == key:
                raise ValueError(f"变量已存在: {key}")
        var = schema.make_variable(key, display_name, var_type, scope,
                                    persistence, default, description)
        self.variables.setdefault("variables", []).append(var)
        return var

    def var_list(self) -> List[Dict]:
        return self.variables.get("variables", [])

    def var_remove(self, key: str) -> bool:
        vs = self.variables.get("variables", [])
        for i, v in enumerate(vs):
            if v["key"] == key:
                vs.pop(i)
                return True
        return False

    # ============================================================
    # 素材操作
    # ============================================================

    def asset_import(self, src_file: str, category: str,
                     subpath: str = "") -> str:
        """导入素材
        category: backgrounds / characters / bgm / se / voice / video / particles
        subpath: 子目录（如 characters/星野/）
        返回相对路径（assets/...）
        """
        src = Path(src_file)
        if not src.exists():
            raise FileNotFoundError(f"源文件不存在: {src}")

        dest_dir = self.path / "assets" / category / subpath
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        shutil.copy2(src, dest)

        rel = f"{category}/{subpath}{src.name}" if subpath else f"{category}/{src.name}"
        return rel

    def asset_list(self, category: Optional[str] = None) -> List[str]:
        """列出素材"""
        assets_dir = self.path / "assets"
        if not assets_dir.exists():
            return []
        result = []
        cats = [category] if category else os.listdir(assets_dir)
        for cat in cats:
            cat_dir = assets_dir / cat
            if not cat_dir.is_dir():
                continue
            for root, _, files in os.walk(cat_dir):
                for f in files:
                    rel = os.path.relpath(os.path.join(root, f), assets_dir)
                    result.append(rel)
        return sorted(result)

    # ============================================================
    # 验证
    # ============================================================

    def check(self) -> Tuple[List[str], List[str]]:
        """验证项目完整性
        返回 (errors, warnings)
        """
        errors = []
        warnings = []

        # 检查入口章节
        if "开始" not in self.chapters:
            errors.append("缺少入口章节'开始'")

        # 检查 chapterOrder 一致性
        order = self.project.get("chapterOrder", [])
        for name in order:
            if name not in self.chapters:
                errors.append(f"chapterOrder 引用了不存在的章节: {name}")
        for name in self.chapters:
            if name not in order:
                warnings.append(f"章节 '{name}' 不在 chapterOrder 中")

        # 检查角色引用
        char_ids = {c["id"] for c in self.char_list()}
        char_names = {c["name"] for c in self.char_list()}

        # 检查场景引用
        scene_ids = {s["id"] for s in self.scene_list()}
        scene_names = {s["name"] for s in self.scene_list()}

        # 检查 fragment 引用
        frag_ids = set()
        for ch in self.chapters.values():
            for f in ch.get("fragments", []):
                frag_ids.add(f["id"])

        # 遍历所有 block 检查引用
        for ch_name, ch in self.chapters.items():
            for frag in ch.get("fragments", []):
                for i, b in enumerate(frag.get("blocks", [])):
                    btype = b.get("type", "")
                    props = b.get("props", {})
                    loc = f"{ch_name}/{frag['name']}#{i} ({btype})"

                    if btype == "dialogue":
                        cid = props.get("characterId", "")
                        if cid and cid not in char_ids:
                            errors.append(f"{loc}: 引用了不存在的角色 ID: {cid}")

                    if btype == "scene":
                        sid = props.get("sceneId", "")
                        if sid and sid not in scene_ids:
                            errors.append(f"{loc}: 引用了不存在的场景 ID: {sid}")

                    if btype == "callFragment":
                        fid = props.get("fragmentId", "")
                        if fid and fid not in frag_ids:
                            errors.append(f"{loc}: 引用了不存在的片段 ID: {fid}")

                    if btype == "branch":
                        import json as _json
                        choices_str = props.get("choices", "[]")
                        try:
                            choices = _json.loads(choices_str) if isinstance(choices_str, str) else choices_str
                        except Exception:
                            errors.append(f"{loc}: branch choices 解析失败")
                            choices = []
                        for j, c in enumerate(choices):
                            fid = c.get("fragmentId", "")
                            if fid and fid not in frag_ids:
                                errors.append(f"{loc}: 选项 {j+1} 引用了不存在的片段 ID: {fid}")

        # 检查素材文件存在性
        for s in self.scene_list():
            for layer in s.get("layers", []):
                ap = layer.get("assetPath", "")
                if ap:
                    full = self.path / "assets" / ap
                    if not full.exists():
                        warnings.append(f"场景 '{s['name']}' 图层 '{layer['name']}' 素材缺失: assets/{ap}")

        for c in self.char_list():
            for expr in c.get("expressions", []):
                ap = expr.get("assetPath", "")
                if ap:
                    full = self.path / "assets" / ap
                    if not full.exists():
                        warnings.append(f"角色 '{c['name']}' 表情 '{expr['name']}' 素材缺失: assets/{ap}")

        return errors, warnings


def create_project(path: str, name: str, author: str = "",
                   description: str = "") -> Project:
    """创建新项目"""
    proj = Project(path)
    proj.project = schema.default_project(name, author, description)
    proj.variables = schema.default_variables()
    proj.characters = schema.default_characters()
    proj.scenes = schema.default_scenes()

    # 创建入口章节
    proj.chapters["开始"] = schema.default_chapter("开始")

    # 添加欢迎旁白
    frag = proj.chapters["开始"]["fragments"][0]
    frag["blocks"].append(schema.make_curtain("close", "0"))
    frag["blocks"].append(schema.make_narration("游戏从这里开始。"))
    frag["blocks"].append(schema.make_curtain("open", "1000"))

    proj.save()
    return proj
