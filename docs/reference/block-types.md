# Block Types Reference

AVGForge supports 25+ block types for comprehensive visual novel authoring.

## Block Categories

### 📝 Text Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `dialogue` | Character dialogue | `characterId`, `expression`, `position`, `showCharacter`, `isFirst`, `isLast` |
| `narration` | Narration text | `keepDialogue` |
| `floatingText` | Floating text overlay | `position`, `fontSize`, `color`, `duration`, `animIn`, `animOut` |
| `comment` | Author notes (not rendered) | `text` |

### 🎬 Scene Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `scene` | Scene transition | `sceneId`, `transitionMode`, `transitionDuration`, `displayType` |
| `destroyScene` | Remove current scene | — |
| `curtain` | Curtain transition | `op` (open/close), `duration`, `color`, `mode` |

### 🎭 Character Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `showCharacter` | Show character (via dialogue) | `characterId`, `expression`, `position` |
| `removeCharacter` | Remove character | `characterId` |
| `animateSprite` | Animate sprite | `targetType`, `targetId`, `x`, `y`, `scaleX`, `scaleY`, `rotation`, `alpha`, `duration`, `easing` |
| `portraitStyleRule` | Portrait style override | `characterId`, `style` |
| `switchDialogueStyle` | Switch dialogue box style | `styleId` |

### 🎥 Camera Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `camera` | Camera movement | `x`, `y`, `zoom`, `rotation`, `duration`, `easing`, `waitForComplete` |
| `resetCamera` | Reset camera to default | `duration` |

### 🎵 Audio Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `sound` | Play audio | `soundType` (BGM/SE/voice), `uri`, `volume`, `loop`, `fadeDuration` |
| `stopSound` | Stop audio | `soundType`, `fadeDuration` |

### 🎞️ Video Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `video` | Play video | `uri`, `loop`, `volume` |
| `stopVideo` | Stop video | — |

### ✨ Effect Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `particle` | Particle effect | `mode` (show/hide), `effectId`, `density` |
| `floatingText` | Floating text | (see Text Blocks) |

### 🔀 Flow Control Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `branch` | Choice menu | `title`, `choices` (array of `{text, mode, fragmentId}`) |
| `callFragment` | Call fragment (returns) | `fragmentId`, `chapterId` |
| `jumpToFragment` | Jump to fragment (no return) | `fragmentId`, `chapterId` |
| `returnToEntry` | Return from called fragment | — |
| `if` | Conditional execution | `condition`, `thenFragmentId`, `elseFragmentId` |
| `end` | End game | `type_name`, `title`, `text` |

### ⚙️ Variable Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `setver` | Set variable | `variableKey`, `scope`, `operation` (set/add/sub/mul/div), `value` |

### ⏱️ Timing Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `wait` | Wait duration | `duration` (ms) |

### 🖥️ UI Blocks

| Block | Description | Key Properties |
|-------|-------------|----------------|
| `showExtensionUI` | Show extension UI | `uiId`, `modal` |

## Block Structure

All blocks follow this structure:

```json
{
  "id": "uuid",
  "type": "blockType",
  "props": {
    "disabled": false,
    ...
  },
  "content": [
    {
      "type": "text",
      "text": "Content text",
      "styles": {}
    }
  ]
}
```

## Block ID Generation

Block IDs are UUID v4 generated at creation time. IDs are stable across
edits unless the block is deleted and recreated.

## Disabled Blocks

Set `props.disabled = true` to skip a block during execution without
deleting it. Disabled blocks are preserved in the project file.
