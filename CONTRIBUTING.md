# Contributing to Brain Hemorrhage Detection

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in Issues
- Provide a clear description of the bug
- Include steps to reproduce
- Add screenshots or error messages if possible

### Suggesting Enhancements
- Check if the enhancement has already been suggested
- Provide a clear description of the enhancement
- Explain why this enhancement would be useful
- List any alternatives you've considered

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/flask-app-brain-hemorrhage.git
   cd flask-app-brain-hemorrhage
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 for Python code
   - Add docstrings to functions
   - Add comments for complex logic
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git commit -m "Add description of changes"
   # Use clear, descriptive commit messages
   # Examples: 
   #   - "Fix: Correct image preprocessing bug"
   #   - "Feature: Add batch processing capability"
   #   - "Docs: Improve setup instructions"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe the changes you made
   - Reference any related issues
   - Include screenshots for UI changes

## Code Style Guidelines

- **Python**: Follow [PEP 8](https://pep8.org/)
- **JavaScript**: Use consistent naming conventions
- **Comments**: Write clear, concise comments
- **Documentation**: Update README if adding new features

## Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run the app
python app.py
```

## Pull Request Process

1. Update documentation if needed
2. Add/update tests if applicable
3. Ensure no conflicts with the main branch
4. Wait for review and address feedback
5. Squash commits if requested

## Questions?

- Open an issue for questions
- Check existing documentation first
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
