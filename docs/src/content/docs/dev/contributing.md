---
title: Contributing
description: Help improve Project Grandma
---

## Welcome Contributions! 👋

We love contributions! Whether it's bug fixes, features, or documentation, your help makes Project Grandma better.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create** a branch for your changes
4. **Make** your changes
5. **Test** thoroughly
6. **Push** to your fork
7. **Submit** a pull request

## Development Setup

See [Building from Source](/dev/build/) for complete setup instructions.

## Types of Contributions

### 🐛 Bug Fixes
- Found a bug? [Create an issue](https://github.com/ktsoaela/project_grandma/issues)
- Include steps to reproduce
- Submit a PR with the fix

### ✨ Features
- Have an idea? [Discuss first](https://github.com/ktsoaela/project_grandma/discussions)
- Get feedback before coding
- Submit PR when ready

### 📚 Documentation
- Improve README
- Add guides and tutorials
- Fix typos and errors
- Improve this wiki

### 🎨 UI/UX
- Improve design
- Better user experience
- Accessibility improvements

## Pull Request Process

### Before Submitting

1. **Test your changes**
   ```bash
   npm run dev
   # Test your feature thoroughly
   ```

2. **Run builds** (Windows in Admin Terminal)
   ```bash
   npm run build:win
   npm run build:mac  # if on Mac
   ```

3. **Check code quality**
   - No console errors
   - Clean code
   - Well-commented

### PR Template

```markdown
## Description
Brief description of changes

## Type
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Other

## Testing
How were these changes tested?

## Screenshots
If UI changes, include screenshots

## Checklist
- [ ] Code builds without errors
- [ ] No new warnings
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
```

## Commit Guidelines

```bash
# Good commit messages
git commit -m "Fix: recording stops on short actions"
git commit -m "Feature: add dark mode toggle"
git commit -m "Docs: update installation guide"

# Format: [Type]: brief description
# Types: Fix, Feature, Docs, Refactor, Style, Test
```

## Coding Standards

### JavaScript/Electron

```javascript
// Use clear variable names
const recordingDuration = 0;  // ✅ Good
const rd = 0;                 // ❌ Unclear

// Add comments for complex logic
// Retry connection up to 3 times
for (let i = 0; i < 3; i++) {
  if (await connectRecorder()) break;
}

// Use const/let (not var)
const immutable = "value";    // ✅ Good
let mutable = "value";
var old = "value";            // ❌ Avoid
```

### Python

```python
# Follow PEP 8
def capture_screenshot():
    """Capture current screen."""
    pass

# Use type hints
def start_recorder(port: int) -> bool:
    return True

# Add docstrings
class WindowInfo:
    """Get information about Windows UI elements."""
    pass
```

## Testing

### Manual Testing

1. **Recording**
   - Click to record
   - Add comments
   - Stop recording

2. **Exports**
   - Test HTML generation
   - Test PDF generation
   - Test Markdown export
   - Test Video recording

3. **Platforms**
   - Test on Windows
   - Test on macOS if possible

## Documentation

When adding features, update:
- `README.md` (overview)
- `docs/` (user guides)
- Code comments (for developers)
- `CHANGELOG.md` (version history)

## Review Process

1. Maintainer reviews PR
2. Requests changes if needed
3. Approves and merges

Don't worry - maintainers are friendly and helpful! 💙

## Code of Conduct

### Be Respectful
- Welcome all contributions
- Be kind and supportive
- Listen to feedback

### No Harassment
- Be professional
- Avoid discriminatory language
- Treat everyone equally

## Questions?

- [GitHub Discussions](https://github.com/ktsoaela/project_grandma/discussions)
- [GitHub Issues](https://github.com/ktsoaela/project_grandma/issues)
- Email maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Recognized in README.md

Thank you for contributing! 🙏
