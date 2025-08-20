# Contributing to Spotify MCP Server

Thank you for your interest in contributing to the Spotify MCP Server! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Git
- A Spotify Developer account
- Basic knowledge of FastAPI and MCP protocol

### Development Setup

1. **Fork the repository**
2. **Clone your fork:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/spotify-mcp-server.git
   cd spotify-mcp-server
   ```

3. **Install dependencies:**

   ```bash
   make install
   ```

4. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your Spotify credentials
   ```

## 🛠️ Development Workflow

### Code Style

We follow these coding standards:

- **Python**: PEP 8 with Black formatting
- **Type Hints**: Required for all functions
- **Docstrings**: Portuguese for comments, English for docstrings
- **Line Length**: 88 characters (Black default)

### Running Tests

```bash
# Run all tests
make test-pytest

# Run specific test categories
python -m pytest tests/ -k "test_tools" -v
python -m pytest tests/ -k "test_resources" -v
```

### Code Quality Checks

```bash
# Format code
make format

# Lint code
make lint

# Type checking
mypy src/
```

### Security Checks

```bash
# Run security checks
make security

# Check for vulnerabilities
safety check
```

## 📝 Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code structure
- Add tests for new functionality
- Update documentation if needed
- Ensure all tests pass

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: add new Spotify feature

- Added new tool for playlist management
- Updated documentation
- Added comprehensive tests"
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

## 🧪 Testing Guidelines

### Test Structure

- **Tools Tests**: Test MCP tools functionality
- **Resources Tests**: Test MCP resources
- **Integration Tests**: Test complete workflows
- **Security Tests**: Test authentication and permissions

### Writing Tests

```python
@pytest.mark.asyncio
async def test_new_feature(self):
    """Test new feature functionality"""
    # Arrange
    expected_result = {"status": "success"}

    # Act
    result = await spotify_service.new_feature()

    # Assert
    assert result == expected_result
```

## 📚 Documentation

### Updating Documentation

- Update README.md for new features
- Update README-PT.md for Portuguese documentation
- Add docstrings to new functions
- Update API documentation if endpoints change

### Documentation Standards

- Use clear, concise language
- Include code examples
- Provide step-by-step instructions
- Keep both English and Portuguese versions in sync

## 🔒 Security Guidelines

### Credential Management

- **Never commit** `.env` files
- **Use placeholders** in examples
- **Validate inputs** to prevent injection attacks
- **Follow OAuth 2.0** best practices

### Code Security

- Validate all user inputs
- Sanitize data before API calls
- Use environment variables for secrets
- Implement proper error handling

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues
2. Try to reproduce the bug
3. Check if it's a configuration issue
4. Verify your Spotify credentials

### Bug Report Template

```markdown
**Bug Description**
Brief description of the issue

**Steps to Reproduce**

1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**

- OS: [e.g., macOS, Linux, Windows]
- Python Version: [e.g., 3.12.0]
- Spotify MCP Server Version: [e.g., 0.1.0]

**Additional Information**
Logs, screenshots, etc.
```

## 💡 Feature Requests

### Before Submitting

1. Check if the feature already exists
2. Consider if it fits the project scope
3. Think about implementation complexity
4. Consider security implications

### Feature Request Template

```markdown
**Feature Description**
Brief description of the requested feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you've considered
```

## 🤝 Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] Linting passes
- [ ] Documentation is updated
- [ ] Security checks pass
- [ ] No sensitive data is committed

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement

## Testing

- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 📋 Code Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Review**: Maintainers review the code
3. **Feedback**: Comments and suggestions provided
4. **Updates**: Address feedback and update PR
5. **Merge**: PR is merged after approval

## 🏷️ Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🆘 Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check README files for setup and usage

## 🙏 Acknowledgments

Thank you for contributing to the Spotify MCP Server! Your contributions help make this project better for everyone.

---

**🎵 Let's make music control amazing together! 🚀**
