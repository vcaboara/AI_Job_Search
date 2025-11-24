# Job Search Module

A Python module for finding and evaluating job leads using various AI models. Designed for configurability and extensibility, allowing easy integration of different AI services and UI components.

## Installation

```bash
pip install -e .
```

## Usage

```python
from job_search_module.core import find_job_leads

# Set your GEMINI_API_KEY as an environment variable or in Colab secrets
# os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY'

query = "DevOps Engineer with Python in sustainability"
leads = find_job_leads(user_query=query)

for lead in leads:
    print(f"Title: {lead.title}\nCompany: {lead.company}\nLink: {lead.link}\n")
```

## Dependency Management Guidelines

To maintain a healthy and consistent project, consider the following guidelines for dependency management:

*   **Pin Major Versions**: In `requirements.txt` or `setup.py`, pin major versions (e.g., `pydantic~=2.0` or `requests==2.32.4`) to prevent unexpected breaking changes from new major releases. Use `~=` for compatible release (e.g., `~=2.0` means `2.0`, `2.1`, but not `3.0`).
*   **Separate Development Dependencies**: Keep development tools (like `pytest`, `flake8`, `pylint`) in a separate `extras_require` section in `setup.py` or in a `requirements-dev.txt` file. This prevents them from being installed in production environments.
*   **Regularly Review and Update**: Periodically review your dependencies for security vulnerabilities and updates. Tools like Dependabot (for GitHub) can automate this.
*   **Automate Dependency Checks**: Integrate dependency checks into your CI/CD pipeline to ensure that new dependencies or updates don't introduce issues.
*   **Avoid Platform-Specific Dependencies in Production**: As seen with `google-colab`, avoid including platform-specific packages in your main `install_requires` if your application is meant to run in diverse environments (e.g., Docker containers). Use conditional imports or separate dependency lists.

### Recommended Dependency Management Tools

While `pip` and `requirements.txt` are standard, for more complex projects, consider these tools:

*   **Poetry**: A comprehensive dependency management and packaging tool for Python. It simplifies dependency resolution, virtual environment management, and package publishing. It uses `pyproject.toml` instead of `setup.py` and `requirements.txt`.
*   **Pipenv**: A tool that aims to bring the best of all packaging worlds to the Python world (bundler, cargo, npm, etc.). It creates and manages a virtualenv for your projects, and adds/removes packages from your `Pipfile` as you install/uninstall packages.
*   **Conda**: A package, dependency, and environment manager for any language. It's particularly popular in the data science community for managing environments with complex native dependencies (e.g., scientific computing libraries).
