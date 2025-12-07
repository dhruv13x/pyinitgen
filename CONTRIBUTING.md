# Contributing to pyinitgen

Thank you for your interest in contributing to `pyinitgen`! We appreciate your help in making this tool better for the Python community.

## 🤝 Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/pyinitgen.git
    cd pyinitgen
    ```
3.  **Set up your environment**:
    We recommend using a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install -e ".[dev]"
    ```
    This installs the package in editable mode along with development dependencies (pytest, black, ruff, etc.).

## 🧪 Running Tests

We use `pytest` for testing. Ensure all tests pass before submitting your changes.

```bash
python -m pytest tests/
```

We aim for high test coverage. You can check coverage with:

```bash
pytest --cov=src/pyinitgen --cov-report=term-missing
```

## 🧹 Code Style

We follow strict code style guidelines to ensure consistency.

-   **Formatting**: We use [Black](https://github.com/psf/black).
    ```bash
    black .
    ```
-   **Linting**: We use [Ruff](https://github.com/astral-sh/ruff).
    ```bash
    ruff check .
    ```

Please ensure your code is formatted and lint-free before committing.

## 📝 Submitting a Pull Request

1.  Create a new branch for your feature or bugfix:
    ```bash
    git checkout -b feature/my-new-feature
    ```
2.  Commit your changes with descriptive commit messages.
3.  Push your branch to your fork:
    ```bash
    git push origin feature/my-new-feature
    ```
4.  Open a Pull Request on the [main repository](https://github.com/dhruv13x/pyinitgen).
5.  Describe your changes and link any related issues.

## 🐛 Reporting Bugs

If you find a bug, please open an issue on GitHub with:
-   A clear description of the problem.
-   Steps to reproduce.
-   Your environment (OS, Python version, `pyinitgen` version).

Thank you for contributing! 🚀
