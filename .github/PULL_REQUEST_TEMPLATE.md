---
name: Pull Request Template
about: Submit changes to AVGForge
---

## Description

Brief description of what this PR changes and why.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test coverage improvement

## Related Issues

Closes #(issue number)
Refs #(issue number)

## Changes Made

- Change 1
- Change 2
- Change 3

## Testing

- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manual testing completed
- [ ] Tested on: [Linux / macOS / Windows]

### Test Commands Run

```bash
python src/avgforge.py --version
python src/avgforge.py init test-pr --template blank
python src/avgforge.py check test-pr
```

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## License

By submitting this pull request, I confirm that my contributions are
licensed under the [AVGForge Dual License (AGPL-3.0 + Commercial)](LICENSE).

## Screenshots / Output

(If applicable, add screenshots or command output to help explain your changes)
