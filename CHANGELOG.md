# Changelog

All notable changes to Project Grandma will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- [ ] Add PDF generation improvements
- [ ] Custom branding support in exports
- [ ] Batch recording mode
- [ ] Cloud storage integration
- [ ] Advanced video encoding options
- [ ] Keyboard shortcut customization
- [ ] Theme customization

## [1.0.0] - 2026-02-22

### Added
- Initial release of Project Grandma
- Windows and macOS support (universal binaries)
- Step-by-step recording with automatic screenshots
- Windows UI element detection and descriptions
- Multiple export formats:
  - HTML (interactive step-by-step guide)
  - PDF (printable report)
  - Markdown (editable with images folder)
  - MP4 (video recording)
- Comment system to explain steps
- Configurable screenshot storage
- Optional video recording with FPS settings
- Electron desktop app with Python backend
- Professional documentation site with Starlight
- GitHub Actions for automated builds
- Executable builds for Windows and macOS

### Features
- **Record Steps**: Click any UI element, automatic screenshot capture
- **Smart Detection**: Windows shows what element you clicked
- **Add Comments**: Explain confusing steps in plain language
- **Multiple Exports**: Choose HTML, PDF, Markdown, or video
- **No Signing**: Works out of the box on any Windows machine
- **Cross-Platform**: Windows 10+ and macOS 10.12+
- **Open Source**: MIT licensed

### Performance
- ~50MB uncompressed Windows executable
- ~60MB uncompressed macOS app
- Fast startup time (<2 seconds)
- Efficient memory usage

### Known Limitations
- Typed text is not recorded (for privacy, like Windows PSR)
- Passwords and sensitive input not captured
- macOS screen recording requires permission grant
- Video recording takes additional disk space
- No direct guide editing after recording (export to Markdown to edit)

### Dependencies
- **Electron**: 28.0.0 (UI framework)
- **Python**: 3.8+ (backend engine)
- **pynput**: Mouse/keyboard tracking
- **mss**: Screenshot capture
- **Flask**: Web API
- **Pillow**: Image processing
- **reportlab**: PDF generation
- **electron-builder**: Build packaging

### Installation
- Windows: Download installer or portable executable
- macOS: Download DMG or ZIP

### Documentation
- Comprehensive getting started guide
- Installation instructions for both platforms
- Step-by-step recording tutorial
- Export format comparison guide
- FAQ with 50+ answered questions
- Full troubleshooting guide
- Developer documentation
- Contributing guidelines

### Browser Compatibility
HTML exports work in:
- Chrome/Chromium 90+
- Firefox 88+
- Safari 13+
- Edge 90+

### Supported Languages
UI: English (additional languages in future releases)

### Testing
- Manual testing on Windows 11
- Manual testing on macOS 12+
- Build verification on GitHub Actions
- Cross-platform compatibility verified

### Contributors
- Initial development by Khotso Tsoaela
- Icon design from Flaticon

## [Unreleased] - Future
See [GitHub Issues](https://github.com/ktsoaela/project_grandma/issues) for planned features

---

### Versioning Note

Project Grandma follows Semantic Versioning:
- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Patch** (1.0.0 → 1.0.1): Bug fixes only

### How to Read This File

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features being phased out
- **Removed**: Deleted features
- **Fixed**: Bug fixes
- **Security**: Security issue fixes
- **Performance**: Performance improvements
- **Docs**: Documentation updates
