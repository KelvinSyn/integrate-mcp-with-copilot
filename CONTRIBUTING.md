# Contributing to Mergington High School Activities API

Thank you for your interest in contributing to the Mergington High School Activities API! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/integrate-mcp-with-copilot.git
   cd integrate-mcp-with-copilot
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application** to verify your setup:
   ```bash
   cd src
   uvicorn app:app --reload
   ```

5. **Access the application**:
   - Main application: http://localhost:8000
   - API documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues or errors in the code
- **New features**: Add new functionality to the application
- **Documentation**: Improve or expand documentation
- **Code quality**: Refactor code, improve performance, or add tests
- **UI/UX improvements**: Enhance the user interface

### Finding Work

- Check the [Issues](https://github.com/KelvinSyn/integrate-mcp-with-copilot/issues) page for open issues
- Look for issues labeled `good first issue` if you're new to the project
- Issues labeled `help wanted` are actively seeking contributors

## Development Workflow

1. **Create a new branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/issue-description
   ```

2. **Make your changes** following the coding standards

3. **Test your changes** thoroughly:
   - Manual testing: Run the application and test your changes
   - API testing: Use the Swagger UI at `/docs` to test endpoints
   - Browser testing: Verify the web interface works correctly

4. **Commit your changes** with a clear, descriptive commit message:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example:

```python
def signup_for_activity(activity_name: str, email: str) -> dict:
    """
    Sign up a student for an activity.
    
    Args:
        activity_name: Name of the activity to sign up for
        email: Student's email address
        
    Returns:
        dict: Success message with confirmation details
        
    Raises:
        HTTPException: If activity not found or student already signed up
    """
    # Implementation here
    pass
```

### JavaScript Code Style

- Use meaningful variable names
- Add comments for complex logic
- Follow consistent indentation (2 spaces)
- Use modern JavaScript features (ES6+)

### General Guidelines

- **Keep it simple**: Write clear, readable code
- **Document your code**: Add comments for complex logic
- **Test thoroughly**: Ensure your changes work as expected
- **Stay consistent**: Follow the existing code style in the project

## Submitting Changes

### Pull Request Guidelines

When submitting a pull request:

1. **Provide a clear title** that summarizes your changes
2. **Describe your changes** in detail:
   - What problem does this solve?
   - How does it solve the problem?
   - Are there any breaking changes?
3. **Reference related issues**: Use "Fixes #123" or "Relates to #456"
4. **Include screenshots** if you made UI changes
5. **Update documentation** if you changed functionality

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
Describe how you tested your changes

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Fixes #(issue number)
```

## Reporting Issues

### Before Submitting an Issue

- Search existing issues to avoid duplicates
- Verify the issue exists in the latest version
- Collect relevant information about your environment

### How to Submit a Good Issue

Include the following information:

1. **Clear title**: Summarize the issue in one line
2. **Description**: Explain the issue in detail
3. **Steps to reproduce**: How can someone else reproduce the issue?
4. **Expected behavior**: What should happen?
5. **Actual behavior**: What actually happens?
6. **Environment details**: 
   - Python version
   - Operating system
   - Browser (for UI issues)
7. **Screenshots or logs**: If applicable

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- OS:
- Browser (if applicable):

## Additional Context
Any other relevant information
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` label
- Check existing documentation in the repository
- Review closed issues for similar questions

## Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort! 🎉
