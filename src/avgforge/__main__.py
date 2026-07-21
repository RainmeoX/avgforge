"""
AVGForge CLI — 主入口
企业级视觉小说开发流水线工具
"""
import argparse
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# 添加包路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from avgforge.project import Project, create_project
from avgforge import schema
from avgforge.renpy_parser import RenpyParser
from avgforge.preview import preview_text, preview_graph_mermaid, preview_stats

__version__ = "1.0.0-enterprise"


def find_project(path: str = ".") -> Project:
    """查找并加载项目"""
    proj = Project(path)
    proj.load()
    return proj


# ============================================================
# 命令实现
# ============================================================

def cmd_init(args):
    """初始化新项目"""
    proj = create_project(
        args.path,
        name=args.name or os.path.basename(os.path.abspath(args.path)),
        author=args.author or "",
        description=args.description or ""
    )
    print(f"  ✓  项目已创建: {proj.path}")
    print(f"  ℹ️  引擎版本: {proj.project['engineVersion']}")
    print(f"  ℹ️  画布尺寸: {proj.project['resolution']['width']}x{proj.project['resolution']['height']}")
    print(f"  ℹ️  入口章节: 开始")
    print(f"\n  下一步:")
    print(f"    cd {os.path.basename(proj.path)}")
    print(f"    avgforge char add <id> --name <角色名>")
    print(f"    avgforge scene add <id> --name <场景名>")
    print(f"    avgforge edit 开始/main")


def cmd_info(args):
    """显示项目信息"""
    proj = find_project(args.path)
    print(preview_stats(proj))


def cmd_check(args):
    """验证项目"""
    proj = find_project(args.path)
    print(f"  ℹ️  检查项目: {proj.path}")
    errors, warnings = proj.check()
    print()
    if errors:
        print(f"  ❌ 错误 ({len(errors)}):")
        for e in errors:
            print(f"     · {e}")
    if warnings:
        print(f"  ⚠️  警告 ({len(warnings)}):")
        for w in warnings:
            print(f"     · {w}")
    if not errors and not warnings:
        print(f"  ✓  项目检查通过，无错误无警告 ✓")
    print()
    return 1 if errors else 0


# ============================================================
# 角色命令
# ============================================================

def cmd_char(args):
    proj = find_project(args.path)

    if args.char_command == "add":
        char = proj.char_add(
            args.name, args.pos or "center",
            args.color_ring or "#7fd4c8",
            args.color_bg or "#1a2e2c",
            args.color_fg or "#7fd4c8"
        )
        proj.save()
        print(f"  ✓  角色已添加: {char['name']} ({char['id'][:8]}...)")
        print(f"  ℹ️  默认位置: {char['defaultPosition']}")
        print(f"  ℹ️  主题色: {char['themeColor']['ring']}")

    elif args.char_command == "list":
        chars = proj.char_list()
        print(f"\n  角色 ({len(chars)} 个):")
        print(f"  {'ID':12s} {'名称':12s} {'位置':10s} {'表情数':6s} {'主题色'}")
        print(f"  {'-'*12} {'-'*12} {'-'*10} {'-'*6} {'-'*20}")
        for c in chars:
            exprs = c.get("expressions", [])
            print(f"  {c['id'][:8]+'...':12s} {c['name']:12s} {c.get('defaultPosition','?'):10s} {len(exprs):6d} {c.get('themeColor',{}).get('ring','?')}")

    elif args.char_command == "remove":
        if proj.char_remove(args.identifier):
            proj.save()
            print(f"  ✓  角色已删除: {args.identifier}")
        else:
            print(f"  ✗  角色不存在: {args.identifier}")
            return 1

    elif args.char_command == "expr":
        if args.expr_command == "add":
            if proj.char_add_expression(args.identifier, args.expr_name, args.file):
                proj.save()
                print(f"  ✓  表情已添加: {args.expr_name} → {args.file}")
            else:
                print(f"  ✗  角色不存在: {args.identifier}")
                return 1


# ============================================================
# 场景命令
# ============================================================

def cmd_scene(args):
    proj = find_project(args.path)

    if args.scene_command == "add":
        layers = []
        for spec in (args.layer or []):
            # 格式: name:distance:assetPath
            parts = spec.split(":", 2)
            if len(parts) == 3:
                layers.append(schema.make_layer(parts[0], parts[2], float(parts[1])))
            elif len(parts) == 2:
                layers.append(schema.make_layer(parts[0], parts[1], 1.0))
            else:
                layers.append(schema.make_layer(f"layer{len(layers)}", parts[0], 1.0))
        scene = proj.scene_add(args.name, layers)
        proj.save()
        print(f"  ✓  场景已添加: {scene['name']} ({scene['id'][:8]}...)")
        print(f"  ℹ️  图层数: {len(layers)}")

    elif args.scene_command == "list":
        scenes = proj.scene_list()
        print(f"\n  场景 ({len(scenes)} 个):")
        for s in scenes:
            layers = s.get("layers", [])
            layer_info = ", ".join(f"{l['name']}({l.get('distance',1)})" for l in layers)
            print(f"  · {s['name']:20s} — {len(layers)} 层 [{layer_info}]")

    elif args.scene_command == "remove":
        if proj.scene_remove(args.identifier):
            proj.save()
            print(f"  ✓  场景已删除: {args.identifier}")
        else:
            print(f"  ✗  场景不存在: {args.identifier}")
            return 1


# ============================================================
# 章节命令
# ============================================================

def cmd_chapter(args):
    proj = find_project(args.path)

    if args.chapter_command == "add":
        ch = proj.chapter_add(args.name)
        proj.save()
        print(f"  ✓  章节已添加: {ch['name']}")

    elif args.chapter_command == "list":
        order = proj.project.get("chapterOrder", [])
        print(f"\n  章节顺序 ({len(order)} 个):")
        for i, name in enumerate(order):
            if name in proj.chapters:
                frag_count = len(proj.chapters[name].get("fragments", []))
                block_count = sum(len(f.get("blocks", [])) for f in proj.chapters[name].get("fragments", []))
                print(f"  {i+1}. {name} — {frag_count} 片段, {block_count} blocks")
            else:
                print(f"  {i+1}. {name} ⚠️ 文件缺失")

    elif args.chapter_command == "remove":
        if proj.chapter_remove(args.name):
            proj.save()
            print(f"  ✓  章节已删除: {args.name}")
        else:
            print(f"  ✗  章节不存在: {args.name}")
            return 1

    elif args.chapter_command == "reorder":
        order = args.order.split(",")
        order = [n.strip() for n in order]
        proj.chapter_reorder(order)
        proj.save()
        print(f"  ✓  章节顺序已更新: {' → '.join(order)}")


# ============================================================
# Fragment 命令
# ============================================================

def cmd_frag(args):
    proj = find_project(args.path)

    if args.frag_command == "add":
        frag = proj.frag_add(args.chapter, args.name)
        proj.save()
        print(f"  ✓  片段已添加: {frag['name']} (章节: {args.chapter})")

    elif args.frag_command == "list":
        if args.chapter not in proj.chapters:
            print(f"  ✗  章节不存在: {args.chapter}")
            return 1
        frags = proj.frag_list(args.chapter)
        print(f"\n  章节 '{args.chapter}' 的片段 ({len(frags)} 个):")
        for f in frags:
            blocks = f.get("blocks", [])
            print(f"  · {f['name']:20s} — {len(blocks)} blocks")


# ============================================================
# 编辑命令（Ren'Py 风格）
# ============================================================

def cmd_edit(args):
    proj = find_project(args.path)

    # 解析 chapter/frag
    if "/" in args.target:
        chapter_name, frag_name = args.target.split("/", 1)
    else:
        chapter_name = args.target
        frag_name = "main"

    if chapter_name not in proj.chapters:
        print(f"  ✗  章节不存在: {chapter_name}")
        return 1

    frag = proj.frag_get(chapter_name, frag_name)
    if not frag:
        print(f"  ✗  片段不存在: {chapter_name}/{frag_name}")
        return 1

    # 序列化为 Ren'Py 文本
    parser = RenpyParser(proj)
    current_text = parser.serialize(frag.get("blocks", []))

    # 如果指定了 --file，直接从文件读取
    if hasattr(args, "file") and args.file:
        with open(args.file, encoding="utf-8") as f:
            new_text = f.read()
        # 过滤注释行
        lines = [l for l in new_text.split("\n") if not l.startswith("#") and not l.startswith("//")]
        new_text = "\n".join(lines).strip()

        try:
            new_blocks = parser.parse(new_text, chapter_name, frag_name)
            frag["blocks"] = new_blocks
            proj.save()
            print(f"  ✓  已从文件导入: {args.file}")
            print(f"  ✓  解析为 {len(new_blocks)} 个 block")
            print(f"  ✓  已保存到 {chapter_name}/{frag_name}")
        except Exception as e:
            print(f"  ✗  解析失败: {e}")
            return 1
        return 0

    # 写入临时文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".rpy", delete=False,
                                      encoding="utf-8", prefix="avgforge_") as tf:
        tf.write("# AVGForge Ren'Py 风格剧本\n")
        tf.write(f"# 章节: {chapter_name} / 片段: {frag_name}\n")
        tf.write("# 保存并退出即同步到项目\n\n")
        tf.write(current_text)
        temp_path = tf.name

    # 获取编辑器
    editor = os.environ.get("AVGFORGE_EDITOR") or os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
    print(f"  ℹ️  使用编辑器: {editor}")
    print(f"  ℹ️  临时文件: {temp_path}")
    print(f"  ℹ️  保存并退出即同步到项目")

    # 打开编辑器
    try:
        subprocess.call([editor, temp_path])
    except FileNotFoundError:
        print(f"  ✗  编辑器不存在: {editor}")
        print(f"     请设置 EDITOR 环境变量，或直接编辑: {temp_path}")
        return 1

    # 读取编辑后的内容
    with open(temp_path, encoding="utf-8") as f:
        new_text = f.read()

    # 过滤注释行
    lines = [l for l in new_text.split("\n") if not l.startswith("#") and not l.startswith("//")]
    new_text = "\n".join(lines).strip()

    # 如果内容有变化，解析并更新
    if new_text != current_text.strip():
        try:
            new_blocks = parser.parse(new_text, chapter_name, frag_name)
            frag["blocks"] = new_blocks
            proj.save()
            print(f"  ✓  片段已更新: {chapter_name}/{frag_name} ({len(new_blocks)} blocks)")
        except ValueError as e:
            print(f"  ✗  解析失败: {e}")
            print(f"     临时文件保留: {temp_path}")
            return 1
    else:
        print(f"  ℹ️  内容无变化")

    # 清理临时文件
    try:
        os.unlink(temp_path)
    except Exception:
        pass


# ============================================================
# 变量命令
# ============================================================

def cmd_var(args):
    proj = find_project(args.path)

    if args.var_command == "add":
        default = args.default
        if args.type == "number":
            try:
                default = int(default) if "." not in str(default) else float(default)
            except ValueError:
                default = 0
        elif args.type == "boolean":
            default = str(default).lower() in ("true", "1", "yes")
        var = proj.var_add(args.key, args.name, args.type, args.scope,
                           args.persistence, default, args.description or "")
        proj.save()
        print(f"  ✓  变量已添加: {var['key']} ({var['displayName']})")

    elif args.var_command == "list":
        vs = proj.var_list()
        print(f"\n  变量 ({len(vs)} 个):")
        print(f"  {'Key':20s} {'显示名':12s} {'类型':10s} {'作用域':10s} {'持久化':10s} {'默认值'}")
        print(f"  {'-'*20} {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
        for v in vs:
            print(f"  {v['key']:20s} {v['displayName']:12s} {v['type']:10s} {v['scope']:10s} {v['persistence']:10s} {str(v['defaultValue']):10s}")

    elif args.var_command == "remove":
        if proj.var_remove(args.key):
            proj.save()
            print(f"  ✓  变量已删除: {args.key}")
        else:
            print(f"  ✗  变量不存在: {args.key}")
            return 1


# ============================================================
# 素材命令
# ============================================================

def cmd_asset(args):
    proj = find_project(args.path)

    if args.asset_command == "import":
        rel = proj.asset_import(args.file, args.category, args.subpath or "")
        proj.save()
        print(f"  ✓  素材已导入: assets/{rel}")

    elif args.asset_command == "list":
        assets = proj.asset_list(args.category)
        print(f"\n  素材 ({len(assets)} 个):")
        for a in assets:
            print(f"  · assets/{a}")


# ============================================================
# 预览命令
# ============================================================

def cmd_preview(args):
    proj = find_project(args.path)

    if args.preview_command == "text":
        print(preview_text(proj, args.chapter))

    elif args.preview_command == "graph":
        mermaid = preview_graph_mermaid(proj)
        output = args.output or "project_graph.mmd"
        with open(output, "w", encoding="utf-8") as f:
            f.write(mermaid)
        print(f"  ✓  Mermaid 流程图已生成: {output}")
        print(f"  ℹ️  用 VS Code Mermaid 插件或 https://mermaid.live 查看")

    elif args.preview_command == "stats":
        print(preview_stats(proj))


# ============================================================
# Block 命令
# ============================================================

def cmd_block(args):
    proj = find_project(args.path)

    if "/" in args.target:
        chapter_name, frag_name = args.target.split("/", 1)
    else:
        chapter_name = args.target
        frag_name = "main"

    if args.block_command == "list":
        blocks = proj.block_list(chapter_name, frag_name)
        print(f"\n  {chapter_name}/{frag_name} 的 blocks ({len(blocks)} 个):")
        for i, b in enumerate(blocks):
            btype = b.get("type", "?")
            content = b.get("content", [])
            text = content[0].get("text", "")[:40] if content else ""
            props = b.get("props", {})
            extra = ""
            if btype == "dialogue":
                extra = f" [{props.get('characterName','')}]"
            elif btype == "scene":
                extra = f" [{props.get('sceneName','')}]"
            print(f"  {i:3d}. {btype:20s}{extra} {text}")

    elif args.block_command == "add":
        if args.type not in schema.BLOCK_TYPES:
            print(f"  ✗  未知 block 类型: {args.type}")
            print(f"     可用类型: {', '.join(sorted(schema.BLOCK_TYPES.keys()))}")
            return 1
        factory = schema.BLOCK_TYPES[args.type]["factory"]
        # 简化：只支持 narration 和 dialogue 的快速添加
        if args.type == "narration":
            block = schema.make_narration(args.text or "")
        elif args.type == "dialogue":
            char = proj.char_get(args.character or "")
            if not char:
                print(f"  ✗  角色不存在: {args.character}")
                return 1
            block = schema.make_dialogue(char["id"], char["name"], args.text or "")
        else:
            block = factory()
        proj.block_add(chapter_name, frag_name, block, args.position if args.position is not None else -1)
        proj.save()
        print(f"  ✓  Block 已添加: {args.type}")

    elif args.block_command == "remove":
        if proj.block_remove(chapter_name, frag_name, args.block_id):
            proj.save()
            print(f"  ✓  Block 已删除: {args.block_id}")
        else:
            print(f"  ✗  Block 不存在: {args.block_id}")
            return 1


# ============================================================
# 参数解析
# ============================================================

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
  avgforge edit 开始/main
  avgforge preview text 开始
  avgforge check
"""
    )
    parser.add_argument("--version", action="version", version=f"AVGForge {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True, help="可用命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化新项目")
    p_init.add_argument("path", help="项目路径")
    p_init.add_argument("--name", help="项目名称")
    p_init.add_argument("--author", help="作者")
    p_init.add_argument("--description", help="项目描述")
    p_init.set_defaults(func=cmd_init)

    # info
    p_info = subparsers.add_parser("info", help="显示项目信息")
    p_info.add_argument("path", nargs="?", default=".", help="项目路径")
    p_info.set_defaults(func=cmd_info)

    # check
    p_check = subparsers.add_parser("check", help="验证项目完整性")
    p_check.add_argument("path", nargs="?", default=".", help="项目路径")
    p_check.set_defaults(func=cmd_check)

    # char
    p_char = subparsers.add_parser("char", help="角色管理")
    char_sub = p_char.add_subparsers(dest="char_command", required=True)
    p_char_add = char_sub.add_parser("add", help="添加角色")
    p_char_add.add_argument("name", help="角色显示名")
    p_char_add.add_argument("--pos", choices=["left","center-left","center","center-right","right"], help="默认位置")
    p_char_add.add_argument("--color-ring", help="主题色 ring (hex)")
    p_char_add.add_argument("--color-bg", help="主题色 bg (hex)")
    p_char_add.add_argument("--color-fg", help="主题色 fg (hex)")
    p_char_add.add_argument("--path", default=".", help="项目路径")
    p_char_add.set_defaults(func=cmd_char)
    p_char_list = char_sub.add_parser("list", help="列出角色")
    p_char_list.add_argument("--path", default=".", help="项目路径")
    p_char_list.set_defaults(func=cmd_char)
    p_char_rm = char_sub.add_parser("remove", help="删除角色")
    p_char_rm.add_argument("identifier", help="角色 ID 或名称")
    p_char_rm.add_argument("--path", default=".", help="项目路径")
    p_char_rm.set_defaults(func=cmd_char)
    p_char_expr = char_sub.add_parser("expr", help="表情管理")
    expr_sub = p_char_expr.add_subparsers(dest="expr_command", required=True)
    p_expr_add = expr_sub.add_parser("add", help="添加表情")
    p_expr_add.add_argument("identifier", help="角色 ID 或名称")
    p_expr_add.add_argument("expr_name", help="表情名")
    p_expr_add.add_argument("file", help="素材路径 (相对 assets/)")
    p_expr_add.add_argument("--path", default=".", help="项目路径")
    p_expr_add.set_defaults(func=cmd_char)

    # scene
    p_scene = subparsers.add_parser("scene", help="场景管理")
    scene_sub = p_scene.add_subparsers(dest="scene_command", required=True)
    p_scene_add = scene_sub.add_parser("add", help="添加场景")
    p_scene_add.add_argument("name", help="场景名")
    p_scene_add.add_argument("--layer", action="append", help="图层 (name:distance:assetPath)")
    p_scene_add.add_argument("--path", default=".", help="项目路径")
    p_scene_add.set_defaults(func=cmd_scene)
    p_scene_list = scene_sub.add_parser("list", help="列出场景")
    p_scene_list.add_argument("--path", default=".", help="项目路径")
    p_scene_list.set_defaults(func=cmd_scene)
    p_scene_rm = scene_sub.add_parser("remove", help="删除场景")
    p_scene_rm.add_argument("identifier", help="场景 ID 或名称")
    p_scene_rm.add_argument("--path", default=".", help="项目路径")
    p_scene_rm.set_defaults(func=cmd_scene)

    # chapter
    p_chapter = subparsers.add_parser("chapter", help="章节管理")
    chapter_sub = p_chapter.add_subparsers(dest="chapter_command", required=True)
    p_ch_add = chapter_sub.add_parser("add", help="添加章节")
    p_ch_add.add_argument("name", help="章节名")
    p_ch_add.add_argument("--path", default=".", help="项目路径")
    p_ch_add.set_defaults(func=cmd_chapter)
    p_ch_list = chapter_sub.add_parser("list", help="列出章节")
    p_ch_list.add_argument("--path", default=".", help="项目路径")
    p_ch_list.set_defaults(func=cmd_chapter)
    p_ch_rm = chapter_sub.add_parser("remove", help="删除章节")
    p_ch_rm.add_argument("name", help="章节名")
    p_ch_rm.add_argument("--path", default=".", help="项目路径")
    p_ch_rm.set_defaults(func=cmd_chapter)
    p_ch_reorder = chapter_sub.add_parser("reorder", help="重排章节顺序")
    p_ch_reorder.add_argument("order", help="章节顺序 (逗号分隔)")
    p_ch_reorder.add_argument("--path", default=".", help="项目路径")
    p_ch_reorder.set_defaults(func=cmd_chapter)

    # frag
    p_frag = subparsers.add_parser("frag", help="片段管理")
    frag_sub = p_frag.add_subparsers(dest="frag_command", required=True)
    p_frag_add = frag_sub.add_parser("add", help="添加片段")
    p_frag_add.add_argument("chapter", help="章节名")
    p_frag_add.add_argument("name", help="片段名")
    p_frag_add.add_argument("--path", default=".", help="项目路径")
    p_frag_add.set_defaults(func=cmd_frag)
    p_frag_list = frag_sub.add_parser("list", help="列出片段")
    p_frag_list.add_argument("chapter", help="章节名")
    p_frag_list.add_argument("--path", default=".", help="项目路径")
    p_frag_list.set_defaults(func=cmd_frag)

    # edit
    p_edit = subparsers.add_parser("edit", help="编辑片段 (Ren'Py 风格)")
    p_edit.add_argument("target", help="目标 (chapter 或 chapter/frag)")
    p_edit.add_argument("--file", help="从文件导入剧本（不打开编辑器）")
    p_edit.add_argument("--path", default=".", help="项目路径")
    p_edit.set_defaults(func=cmd_edit)

    # var
    p_var = subparsers.add_parser("var", help="变量管理")
    var_sub = p_var.add_subparsers(dest="var_command", required=True)
    p_var_add = var_sub.add_parser("add", help="添加变量")
    p_var_add.add_argument("key", help="变量 key")
    p_var_add.add_argument("name", help="显示名")
    p_var_add.add_argument("--type", choices=["boolean","number","string"], default="number")
    p_var_add.add_argument("--scope", choices=["project","system"], default="project")
    p_var_add.add_argument("--persistence", choices=["slot","shared"], default="slot")
    p_var_add.add_argument("--default", default="0", help="默认值")
    p_var_add.add_argument("--description", help="描述")
    p_var_add.add_argument("--path", default=".", help="项目路径")
    p_var_add.set_defaults(func=cmd_var)
    p_var_list = var_sub.add_parser("list", help="列出变量")
    p_var_list.add_argument("--path", default=".", help="项目路径")
    p_var_list.set_defaults(func=cmd_var)
    p_var_rm = var_sub.add_parser("remove", help="删除变量")
    p_var_rm.add_argument("key", help="变量 key")
    p_var_rm.add_argument("--path", default=".", help="项目路径")
    p_var_rm.set_defaults(func=cmd_var)

    # asset
    p_asset = subparsers.add_parser("asset", help="素材管理")
    asset_sub = p_asset.add_subparsers(dest="asset_command", required=True)
    p_asset_import = asset_sub.add_parser("import", help="导入素材")
    p_asset_import.add_argument("file", help="源文件路径")
    p_asset_import.add_argument("category", choices=["backgrounds","characters","bgm","se","voice","video","particles","fonts","ui"])
    p_asset_import.add_argument("--subpath", help="子目录 (如 characters/星野/)")
    p_asset_import.add_argument("--path", default=".", help="项目路径")
    p_asset_import.set_defaults(func=cmd_asset)
    p_asset_list = asset_sub.add_parser("list", help="列出素材")
    p_asset_list.add_argument("category", nargs="?", help="素材类别")
    p_asset_list.add_argument("--path", default=".", help="项目路径")
    p_asset_list.set_defaults(func=cmd_asset)

    # block
    p_block = subparsers.add_parser("block", help="Block 管理")
    block_sub = p_block.add_subparsers(dest="block_command", required=True)
    p_block_list = block_sub.add_parser("list", help="列出 blocks")
    p_block_list.add_argument("target", help="目标 (chapter 或 chapter/frag)")
    p_block_list.add_argument("--path", default=".", help="项目路径")
    p_block_list.set_defaults(func=cmd_block)
    p_block_add = block_sub.add_parser("add", help="添加 block")
    p_block_add.add_argument("target", help="目标 (chapter 或 chapter/frag)")
    p_block_add.add_argument("type", help="block 类型")
    p_block_add.add_argument("--text", help="文本内容 (narration/dialogue)")
    p_block_add.add_argument("--character", help="角色名 (dialogue)")
    p_block_add.add_argument("--position", type=int, help="插入位置")
    p_block_add.add_argument("--path", default=".", help="项目路径")
    p_block_add.set_defaults(func=cmd_block)
    p_block_rm = block_sub.add_parser("remove", help="删除 block")
    p_block_rm.add_argument("target", help="目标 (chapter 或 chapter/frag)")
    p_block_rm.add_argument("block_id", help="block ID")
    p_block_rm.add_argument("--path", default=".", help="项目路径")
    p_block_rm.set_defaults(func=cmd_block)

    # preview
    p_preview = subparsers.add_parser("preview", help="预览")
    preview_sub = p_preview.add_subparsers(dest="preview_command", required=True)
    p_preview_text = preview_sub.add_parser("text", help="文本预览")
    p_preview_text.add_argument("chapter", help="章节名")
    p_preview_text.add_argument("--path", default=".", help="项目路径")
    p_preview_text.set_defaults(func=cmd_preview)
    p_preview_graph = preview_sub.add_parser("graph", help="Mermaid 流程图")
    p_preview_graph.add_argument("--output", help="输出文件 (默认 project_graph.mmd)")
    p_preview_graph.add_argument("--path", default=".", help="项目路径")
    p_preview_graph.set_defaults(func=cmd_preview)
    p_preview_stats = preview_sub.add_parser("stats", help="项目统计")
    p_preview_stats.add_argument("--path", default=".", help="项目路径")
    p_preview_stats.set_defaults(func=cmd_preview)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
