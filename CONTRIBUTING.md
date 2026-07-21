# Contributing to AVGForge

First off, thank you for considering contributing to AVGForge! 🎉

This document outlines our contribution process and standards.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git 2.20 or higher
- A modern web browser (for testing web preview)
- A text editor with JSON support (VS Code recommended)

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/avgforge.git
cd avgforge

# Create a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Verify installation
python3 src/avgforge.py --version

# Run tests
python3 -m pytest tests/  # (when test suite is available)
```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please:
1. Check the [existing issues](https://github.com/YOUR_USERNAME/avgforge/issues) to avoid duplicates
2. Verify the bug exists on the latest `main` branch
3. Collect the following information:
   - OS and version
   - Python version
   - AVGForge version (`avgforge --version`)
   - Minimal reproduction steps
   - Expected vs actual behavior

Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).

### Suggesting Enhancements

Enhancement suggestions are welcome. Please:
1. Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
2. Describe the use case and expected benefit
3. Indicate if you're willing to implement it yourself

### Pull Requests

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes** following our coding standards (see below)

3. **Test thoroughly**:
   ```bash
   # Test core functionality
   python3 src/avgforge.py init test-project --template blank
   python3 src/avgforge.py --help
   
   # Test web preview (if applicable)
   cd test-project
   python3 ../src/avgforge.py preview web
   ```

4. **Commit with conventional messages**:
   ```
   feat: add new block type 'shake'
   fix: resolve unicode path handling on Windows
   docs: update README with installation steps
   refactor: extract project validator
   test: add unit tests for Ren'Py parser
   chore: update dependencies
   ```

5. **Open a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (for UI changes)
   - Test results

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use 4-space indentation
- Maximum line length: 100 characters
- Use type hints for function signatures
- Document public functions with docstrings

```python
def add_character(project: dict, char_id: str, name: str,
                  position: str = "center") -> dict:
    """Add a character to the project.
    
    Args:
        project: The project dictionary.
        char_id: Unique character identifier.
        name: Display name of the character.
        position: Default position (left/center-left/center/center-right/right).
    
    Returns:
        Updated project dictionary.
    
    Raises:
        ValueError: If char_id already exists.
    """
    if char_id in project.get("characters", {}):
        raise ValueError(f"Character '{char_id}' already exists")
    # ... implementation
```

### JSON Style

- 2-space indentation
- UTF-8 encoding
- No trailing commas
- Keys in snake_case
- Consistent key ordering (alphabetical within groups)

### File Organization

```
src/
├── avgforge.py          # Main CLI entry point
├── commands/            # Command implementations
│   ├── __init__.py
│   ├── project.py       # Project management
│   ├── character.py     # Character commands
│   ├── scene.py         # Scene commands
│   ├── chapter.py       # Chapter/fragment commands
│   ├── block.py         # Block editing
│   ├── variable.py      # Variable management
│   ├── asset.py         # Asset management
│   ├── preview.py       # Preview commands
│   └── build.py         # Build commands
├── engine/              # Core engine
│   ├── __init__.py
│   ├── parser.py        # Ren'Py parser
│   ├── executor.py      # Block executor
│   ├── validator.py     # Project validator
│   └── renderer.py      # Web preview renderer
└── utils/               # Utilities
    ├── __init__.py
    ├── json_utils.py    # JSON helpers
    └── io_utils.py      # I/O helpers
```

## Testing

### Manual Testing Checklist

Before submitting a PR, verify:

- [ ] `avgforge --version` works
- [ ] `avgforge init test-project` creates valid project
- [ ] `avgforge char add` / `scene add` / `chapter add` work
- [ ] `avgforge edit` opens `$EDITOR`
- [ ] `avgforge preview text` renders correctly
- [ ] `avgforge preview web` starts server and renders in browser
- [ ] `avgforge build html` produces valid HTML file
- [ ] `avgforge check` reports no errors on valid project

### Test Projects

Use the `examples/` directory for test projects:
- `examples/blank/` — minimal valid project
- `examples/demo/` — full-featured demo project

## License

By contributing, you agree that your contributions will be dual-licensed
under the [AGPL-3.0 + Commercial license](LICENSE). See the
[Contributor License Agreement](LICENSE) section for details.

## Questions?

- 💬 [GitHub Discussions](https://github.com/YOUR_USERNAME/avgforge/discussions)
- 📧 Email: `community@avgforge.example`

Thank you for contributing! ⚒️
