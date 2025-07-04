# Contributing to SmartHomeHarmonizer

We love your input! We want to make contributing to SmartHomeHarmonizer as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable.
2. Update the docs/ with any new functionality.
3. The PR will be merged once you have the sign-off of at least one maintainer.

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report bugs using GitHub's [issue tracker](https://github.com/yourusername/SmartHomeHarmonizer/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/SmartHomeHarmonizer/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Code Style

We use [Black](https://black.readthedocs.io/) for Python code formatting. Please run:

```bash
black smarthomeharmonizer tests
```

## Testing

We use pytest for testing. Please write tests for new functionality:

```bash
pytest tests/
```

## Documentation

We use Sphinx for documentation. Please update docs for new features:

```bash
cd docs
make html
```

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
