# Contributing to Orkinosai Conversational Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up `.env` file with your Azure credentials

## Code Standards

### Python Style
- Follow PEP 8 style guidelines
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Run tests with: `pytest tests/ -v`
- Aim for high code coverage

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep first line under 72 characters
- Add detailed description if needed

Example:
```
Add support for streaming responses

- Implement streaming in AzureAIClient
- Add streaming endpoint to Flask API
- Update documentation with streaming examples
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear commits
3. Add/update tests as needed
4. Update documentation (README, docstrings, etc.)
5. Ensure all tests pass
6. Submit PR with clear description of changes

## Adding New Features

### New API Endpoints
1. Add endpoint in `src/api/app.py`
2. Update API documentation in README
3. Add example usage in `examples/`

### New Configuration Options
1. Update `config.yaml` with new options
2. Add corresponding fields in `src/config/settings.py`
3. Update `.env.example` if needed
4. Document in README

### New Azure Services
1. Add configuration in `AzureConfig` class
2. Create client wrapper in `src/agent/`
3. Add integration tests
4. Document setup requirements

## Testing Guidelines

### Unit Tests
- Place in `tests/` directory
- Test individual functions/methods
- Mock external dependencies (Azure API calls)

### Integration Tests
- Test component interactions
- Use test Azure resources if possible
- Document test setup requirements

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest tests/ -v --cov=src
```

## Documentation

- Update README.md for user-facing changes
- Update QUICKSTART.md for setup changes
- Add docstrings to new code
- Include examples for new features

## Code Review

All submissions require review. We'll review:
- Code quality and style
- Test coverage
- Documentation completeness
- Security considerations
- Performance implications

## Security

- Never commit secrets or API keys
- Report security issues privately
- Follow Azure security best practices
- Use environment variables for credentials

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about contributing
- General discussions

Thank you for contributing! 🎉
