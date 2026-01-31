# Contributing to Journal Buddy

Thanks for your interest in contributing! 🎉

## How to Contribute

### 🐛 Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/sk0dot7/journal-buddy/issues)
2. If not, create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Output of `python3 test.py`

### 💡 Suggesting Features

1. Check [Discussions](https://github.com/sk0dot7/journal-buddy/discussions) first
2. Create a new issue with:
   - Clear description of the feature
   - Why it would be useful
   - How you envision it working

### 🔧 Pull Requests

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**: `python3 test.py`
5. **Commit**: Use clear commit messages
6. **Push**: `git push origin feature/your-feature-name`
7. **Create Pull Request** with description of changes

### 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

### 🧪 Testing

Before submitting:

```bash
# Run tests
python3 test.py

# Test basic flow
python3 journal-direct.py

# Check imports
python3 -m py_compile main.py
```

### 🎯 Priority Areas

We especially welcome contributions in:

1. **Voice Input** - Add speech-to-text journaling
2. **Mobile App** - React Native or Flutter companion
3. **Analytics** - Mood tracking, sentiment analysis
4. **UI/UX** - Make it more beautiful
5. **Documentation** - Improve guides and tutorials
6. **Bug Fixes** - Always appreciated!
7. **Performance** - Optimize LLM calls, reduce memory

### 💬 Getting Help

- Open a [Discussion](https://github.com/sk0dot7/journal-buddy/discussions)
- Check existing [Issues](https://github.com/sk0dot7/journal-buddy/issues)
- Read the docs: [STRUCTURE.md](STRUCTURE.md)

### 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Development Setup

```bash
# Clone your fork
git clone https://github.com/sk0dot7/journal-buddy.git
cd journal-buddy

# Install dependencies
pip install -r requirements.txt

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama

# Run in dev mode
python3 journal-direct.py
```

## Code of Conduct

Be kind, respectful, and constructive. We're all here to make journaling easier.

---

Thank you for contributing! 🙏
