# Quick Start

Get up and running with AVGForge in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- A text editor (VS Code recommended)
- A modern web browser

## Installation

### Option 1: Direct Download

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/avgforge.git
cd avgforge

# Make executable (Linux/macOS)
chmod +x src/avgforge.py

# Verify installation
python3 src/avgforge.py --version
```

### Option 2: Add to PATH

```bash
# Create symlink (Linux/macOS)
sudo ln -s $(pwd)/src/avgforge.py /usr/local/bin/avgforge

# Or add to PATH in ~/.bashrc / ~/.zshrc
echo 'export PATH="$PATH:'$(pwd)/src'"' >> ~/.bashrc
source ~/.bashrc

# Now you can use avgforge directly
avgforge --version
```

## Your First Project

### 1. Create a New Project

```bash
avgforge init my-first-vn --name "My First Visual Novel"
cd my-first-vn
```

### 2. Add Characters

```bash
# Add the protagonist
avgforge char add hero --name "Hero" --pos left --color-ring "#7fc8f8"

# Add the heroine
avgforge char add heroine --name "Heroine" --pos right --color-ring "#ffb6d9"
```

### 3. Add Scenes

```bash
# Add a classroom scene
avgforge scene add classroom --name "Classroom" \
  --layer "bg:1:backgrounds/classroom.png"

# Add a rooftop scene
avgforge scene add rooftop --name "Rooftop" \
  --layer "bg:1:backgrounds/rooftop.png"
```

### 4. Edit the Script

```bash
# Edit the entry fragment
avgforge edit 开始/main
```

This opens your `$EDITOR` with Ren'Py-style syntax:

```renpy
scene classroom with fade

show hero neutral at left
hero "What a beautiful day."

show heroine happy at right
heroine "Good morning!"

menu "How to respond?":
    "Say hello" -> call greeting
    "Stay silent" -> $ heroine_affection -= 1
```

Save and exit the editor.

### 5. Preview Your Game

#### Text Preview (Quick Check)

```bash
avgforge preview text 开始
```

#### Web Preview (Full Visual)

```bash
avgforge preview web
```

This starts a local server and opens your browser.

### 6. Build the Final Game

```bash
# Build as single-file HTML
avgforge build html -o my-first-vn.html
```

Distribute the HTML file — anyone can play it in a browser.

## Next Steps

- [CLI Commands Reference](../reference/cli-commands.md) — Complete command list
- [Block Types](../reference/block-types.md) — All 25+ block types
- [Ren'Py Syntax](../reference/renpy-syntax.md) — Script syntax guide
- [Authoring Workflow](../guides/authoring-workflow.md) — Best practices

## Common Issues

### Q: The web preview doesn't open my browser

A: Some Linux environments don't have a default browser set. Open
`http://localhost:8765` manually.

### Q: My editor doesn't open

A: Set the `EDITOR` environment variable:
```bash
export EDITOR=vim  # or nano, code, etc.
```

### Q: Build fails with "asset missing"

A: Run `avgforge check` to identify missing assets, then add them to
the `assets/` directory.

## Need Help?

- 📖 [Full Documentation](../README.md)
- 💬 [GitHub Discussions](https://github.com/YOUR_USERNAME/avgforge/discussions)
- 🐛 [Report Issues](https://github.com/YOUR_USERNAME/avgforge/issues)
