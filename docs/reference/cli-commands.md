# CLI Commands Reference

Complete reference for all AVGForge CLI commands.

## Global Options

```
avgforge [--version] [--help] <command> [subcommand] [options]
```

| Option | Description |
|--------|-------------|
| `--version` | Display version information |
| `--help` | Show help message |

## Commands

### `init` — Initialize New Project

```bash
avgforge init <path> [--template <name>] [--name <name>] [--description <text>]
```

Creates a new AVGForge project at the specified path.

**Options:**
- `--template` — Project template (`blank` | `demo`). Default: `blank`
- `--name` — Project display name
- `--description` — Project description

**Example:**
```bash
avgforge init my-game --template blank --name "My Visual Novel"
```

---

### `info` — Display Project Information

```bash
avgforge info [path]
```

Shows project metadata, character count, scene count, and block statistics.

---

### `char` — Character Management

```bash
avgforge char add <id> --name <name> [--pos <position>] [--color-ring <hex>] [--color-bg <hex>] [--color-fg <hex>]
avgforge char list
avgforge char remove <id>
```

**Positions:** `left`, `center-left`, `center`, `center-right`, `right`

**Example:**
```bash
avgforge char add hoshino --name "星野" --pos right --color-ring "#ffb6d9"
```

---

### `scene` — Scene Management

```bash
avgforge scene add <id> --name <name> --layer <layer-spec> [--layer <layer-spec> ...]
avgforge scene list
avgforge scene remove <id>
```

**Layer spec format:** `<name>:<distance>:<asset-path>`

- `name` — Layer identifier (e.g., `bg`, `fg`, `clouds`)
- `distance` — Parallax depth (0-20, lower = closer)
- `asset-path` — Path to image file relative to assets/

**Example:**
```bash
avgforge scene add classroom --name "教室" \
  --layer "bg:1:backgrounds/classroom.png" \
  --layer "fg:0.5:backgrounds/classroom_fg.png"
```

---

### `chapter` — Chapter Management

```bash
avgforge chapter add <name>
avgforge chapter list
avgforge chapter remove <name>
avgforge chapter move <name> <direction>
```

**Directions:** `up`, `down`

**Note:** The `开始` (Start) chapter is the entry point and cannot be removed.

---

### `frag` — Fragment Management

```bash
avgforge frag add <chapter>/<fragment-name>
avgforge frag list [chapter]
avgforge frag remove <chapter>/<fragment-name>
```

**Example:**
```bash
avgforge frag add 序章/相遇
avgforge frag list 序章
```

---

### `edit` — Edit Fragment (Ren'Py Style)

```bash
avgforge edit <chapter>/<fragment>
```

Opens the fragment in `$EDITOR` with Ren'Py-style syntax.

**Supported Syntax:**
- `scene <name> [with <transition>]`
- `show <character> [<expression>] [at <position>]`
- `hide <character>`
- `<character> "<dialogue>"`
- `play music|sound|voice <file> [volume <n>%] [loop]`
- `stop music|sound`
- `pause <seconds>`
- `$ <variable> = <value>`
- `if <condition>:`
- `menu "<title>":`
- `call <fragment>`
- `jump <fragment>`

---

### `check` — Validate Project

```bash
avgforge check [path]
```

Validates project integrity:
- JSON schema compliance
- Asset reference existence
- Fragment reference resolution
- Variable reference consistency

**Exit codes:**
- `0` — No errors
- `1` — Errors found
- `2` — Project not found

---

### `preview` — Preview

#### Text Preview

```bash
avgforge preview text <chapter>
```

Renders the chapter as formatted text in the terminal.

#### Web Preview

```bash
avgforge preview web [--port <port>]
```

Starts a local HTTP server and opens the browser.

**Default port:** 8765

---

### `build` — Build

```bash
avgforge build html [--output <path>]
```

Builds the project as a single-file HTML game.

**Output:** `<project-name>.html` in current directory (or specified path)

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Project not found |
| 3 | Invalid arguments |
| 4 | Asset missing |
| 5 | Build failed |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AVGFORGE_EDITOR` | `$EDITOR` | Editor for `edit` command |
| `AVGFORGE_PORT` | `8765` | Default preview port |
| `AVGFORGE_LANG` | `auto` | Interface language |
