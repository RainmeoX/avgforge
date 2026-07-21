# Changelog

All notable changes to AVGForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-enterprise] - 2026-07-21

### 🎉 Enterprise General Availability

First stable release of AVGForge — the enterprise-grade visual novel
authoring pipeline.

### Added — Core Authoring

- **Project scaffolding** (`avgforge init`) with blank and template presets
- **Character management** with portraits, expressions, 5-position system,
  theme colors, and custom attributes
- **Scene composition** with multi-layer parallax backgrounds (depth distance)
- **Chapter & fragment management** with hierarchical narrative structure
- **Block-based scripting** supporting 25+ block types:
  - Dialogue, narration, scene, curtain, branch
  - Camera, particle, sound, stopSound, wait
  - Setver, floatingText, removeCharacter, animateSprite
  - SwitchDialogueStyle, video, stopVideo, destroyScene
  - ResetCamera, showExtensionUI, callExtensionFunction
  - CallFragment, comment, portraitStyleRule, returnToEntry
- **Variable system** with three dimensions:
  - Type: Boolean / Number / String
  - Scope: Project / System
  - Persistence: Slot (save-bound) / Shared (cross-save)
- **Branch & condition** with choice jumps, conditional execution,
  and fragment calls
- **Ren'Py-style script editor** with `$EDITOR` integration
- **Asset management** with import, reference tracking, and unused detection
- **Project validation** with reference integrity check

### Added — Preview & Debug

- **Text preview** — terminal-rendered script flow with indentation
- **Mermaid flowchart export** — branch structure visualization
- **Web preview engine** — browser-based runtime with full visual fidelity
  - 5-position character rendering
  - Multi-layer parallax scenes
  - Particle system (star / snow / sakura)
  - Web Audio API BGM synthesis
  - Save/load system (10 slots + quick save/load)
  - History log (100 entries)
  - Settings screen
  - Title screen with animated transitions

### Added — Build & Distribution

- **HTML single-file build** — self-contained `.html` with embedded assets
  (base64-encoded images, inlined CSS/JS)
- **Web bundle build** — separated assets for CDN deployment
- **Project export** — portable project archive

### Added — Enterprise Features

- **Git-native format** — every artifact is plain-text JSON, fully diffable
- **Deterministic builds** — content-addressed, reproducible output
- **CI/CD pipeline** — headless operation with exit-code semantics
- **Python SDK** — programmatic project manipulation
- **Zero runtime dependencies** — pure Python standard library

### Added — Documentation

- Comprehensive README with feature matrix and architecture diagram
- Dual-license declaration (AGPL-3.0 + Commercial)
- Contributing guide
- Security policy
- Code of conduct

### Technical Specifications

- **Supported platforms:** Linux x64, macOS 11+, Windows 10+
- **Python version:** 3.9+
- **Project format:** JSON (UTF-8)
- **Build output:** HTML5 (single-file or bundle)
- **Browser support:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Performance Benchmarks

- Project parsing: < 100ms (10,000 blocks)
- HTML build: < 5s (100MB project)
- Web preview startup: < 500ms
- Memory footprint: < 50MB (typical project)

---

## [0.9.0-rc] - 2026-07-15

### Added
- Release candidate with feature freeze
- Final API stabilization
- Documentation review pass

### Fixed
- Edge cases in Ren'Py parser
- Unicode handling in asset paths

---

## [0.5.0-beta] - 2026-06-01

### Added
- Initial beta release
- Core CLI commands
- Basic project schema
- Text preview only

### Known Issues
- Web preview engine under development
- Limited block type support

---

## Versioning Scheme

AVGForge uses a modified semantic versioning scheme:

```
MAJOR.MINOR.PATCH-SUFFIX
```

- **MAJOR**: Breaking changes (e.g., project format incompatibility)
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)
- **SUFFIX**: Release stage (`alpha`, `beta`, `rc`, `enterprise`)

---

## Migration Guides

For migration guides between major versions, see [docs/migration/](docs/migration/).
