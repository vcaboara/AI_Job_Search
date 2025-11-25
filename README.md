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

* **Pin Major Versions**: In `requirements.txt` or `setup.py`, pin major versions (e.g., `pydantic~=2.0` or `requests==2.32.4`) to prevent unexpected breaking changes from new major releases. Use `~=` for compatible release (e.g., `~=2.0` means `2.0`, `2.1`, but not `3.0`).
* **Separate Development Dependencies**: Keep development tools (like `pytest`, `flake8`, `pylint`) in a separate `extras_require` section in `setup.py` or in a `requirements-dev.txt` file. This prevents them from being installed in production environments.
* **Regularly Review and Update**: Periodically review your dependencies for security vulnerabilities and updates. Tools like Dependabot (for GitHub) can automate this.
* **Automate Dependency Checks**: Integrate dependency checks into your CI/CD pipeline to ensure that new dependencies or updates don't introduce issues.
* **Avoid Platform-Specific Dependencies in Production**: As seen with `google-colab`, avoid including platform-specific packages in your main `install_requires` if your application is meant to run in diverse environments (e.g., Docker containers). Use conditional imports or separate dependency lists.

### Recommended Dependency Management Tools

While `pip` and `requirements.txt` are standard, for more complex projects, consider these tools:

* **Poetry**: A comprehensive dependency management and packaging tool for Python. It simplifies dependency resolution, virtual environment management, and package publishing. It uses `pyproject.toml` instead of `setup.py` and `requirements.txt`.
* **Pipenv**: A tool that aims to bring the best of all packaging worlds to the Python world (bundler, cargo, npm, etc.). It creates and manages a virtualenv for your projects, and adds/removes packages from your `Pipfile` as you install/uninstall packages.
* **Conda**: A package, dependency, and environment manager for any language. It's particularly popular in the data science community for managing environments with complex native dependencies (e.g., scientific computing libraries).

## Recent Enhancements

This project has undergone several significant enhancements to improve its modularity, extensibility, user experience, and robustness. Below is a summary of the key updates:

*   **Python Version Update**: The project now explicitly requires Python version `>=3.10`. This change is reflected in `setup.py` and the `Dockerfile`, ensuring compatibility with modern Python features.

*   **AI Service Interface Refactoring**: The core logic for interacting with AI models has been refactored to support multiple AI backends. This involves:
    *   An `AbstractAIService` interface (`job_search_module/services/base.py`) defining a common contract for AI interactions.
    *   A concrete `GeminiService` implementation (`job_search_module/services/gemini.py`) for the Google Gemini API.
    *   A placeholder `OpenAIService` (`job_search_module/services/openai.py`) demonstrating how other AI services can be easily integrated.

*   **Streamlit UI Enhancements**: The `app.py` Streamlit application has been significantly upgraded:
    *   **Dynamic AI Service Selection**: Users can now select their preferred AI service (Gemini or OpenAI) via a dropdown in the sidebar.
    *   **Editable Model Name Inputs**: Model names for both Gemini and OpenAI can be specified through text inputs, which are conditionally enabled based on the selected AI service.
    *   **API Key Inputs**: Secure password-type text input fields have been added in the sidebar for users to directly enter their Gemini and OpenAI API keys, prioritizing UI input over environment variables for convenience.

*   **Improved Context Document Handling**: The application now offers more robust handling of user-uploaded context documents:
    *   **File Size Limits**: Uploaded files are checked against a maximum size limit of 5 MB.
    *   **Supported File Type Validation**: The app validates uploaded files to ensure they are of supported types (PNG, JPG, JPEG, PDF, TXT, MD, DOCX).
    *   **Basic Content Validation**: Text-based files (`.txt`, `.md`) are checked for non-empty content and a minimum character count to ensure meaningful input.
    *   **Secure Temporary Storage**: Uploaded files are temporarily saved and automatically cleaned up after processing using `tempfile.NamedTemporaryFile`, ensuring data privacy and preventing accumulation.

### Latest Fixes and Enhancements (Post-Refactoring)

*   **Resolved `SyntaxError` in `app.py`:** Fixed an unclosed parenthesis in the `st.sidebar.selectbox` configuration, ensuring the Streamlit application launches correctly.
*   **Resolved `AttributeError` for `google.generativeai.Client`:** Refactored `job_search_module/services/gemini.py` to correctly instantiate the Gemini client using `google.generativeai.GenerativeModel` and handle API key configuration internally, improving compatibility across environments.

### Latest Fixes and Enhancements

*   **Resolved `SyntaxError` in `app.py`:** Fixed an unclosed parenthesis in the `st.sidebar.selectbox` configuration, ensuring the Streamlit application launches correctly.
*   **Resolved `AttributeError` for `google.generativeai.Client`:** Refactored `job_search_module/services/gemini.py` to correctly instantiate the Gemini client using `google.generativeai` and handle API key configuration internally, improving compatibility across environments.

### Latest Fixes and Enhancements

*   **Resolved `SyntaxError` in `app.py`:** Fixed an unclosed parenthesis in the `st.sidebar.selectbox` configuration, ensuring the Streamlit application launches correctly.
*   **Resolved `AttributeError` for `google.generativeai.Client`:** Refactored `job_search_module/services/gemini.py` to correctly instantiate the Gemini client using `google.generativeai` and handle API key configuration internally, improving compatibility across environments.

## Continuous Integration (CI) with GitHub Actions

This project utilizes GitHub Actions for Continuous Integration (CI) to automate testing and linting whenever new code is pushed or a pull request is opened. This helps maintain code quality and prevent regressions.

### Workflow Details

The CI workflow is defined in `.github/workflows/ci.yml` and includes the following steps:

1.  **Checkout Code**: Fetches the latest code from the repository.
2.  **Set up Python 3.10**: Configures the Python environment to use version 3.10.
3.  **Install Dependencies**: Installs project dependencies from `requirements.txt` and development dependencies (including `flake8` and `pytest`) specified in `setup.py`.
4.  **Run Flake8 Linting**: Executes `flake8` to check for Python style guide violations and potential errors.
5.  **Run Pytest**: Runs all unit tests to ensure the application's core functionality is working as expected.

### Benefits

*   **Automated Quality Checks**: Catches errors and style violations early in the development cycle.
*   **Faster Feedback**: Developers receive immediate feedback on their code changes.
*   **Increased Confidence**: Ensures that new features or bug fixes don't break existing functionality.
*   **Collaborative Development**: Promotes a consistent code standard across all contributors.

## Continuous Integration (CI) with GitHub Actions

This project utilizes GitHub Actions for Continuous Integration (CI) to automate testing and linting whenever new code is pushed or a pull request is opened. This helps maintain code quality and prevent regressions.

### Workflow Details

The CI workflow is defined in `.github/workflows/ci.yml` and includes the following steps:

1.  **Checkout Code**: Fetches the latest code from the repository.
2.  **Set up Python 3.10**: Configures the Python environment to use version 3.10.
3.  **Install Dependencies**: Installs project dependencies from `requirements.txt` and development dependencies (including `flake8` and `pytest`) specified in `setup.py`.
4.  **Run Flake8 Linting**: Executes `flake8` to check for Python style guide violations and potential errors.
5.  **Run Pytest**: Runs all unit tests to ensure the application's core functionality is working as expected.

### Benefits

*   **Automated Quality Checks**: Catches errors and style violations early in the development cycle.
*   **Faster Feedback**: Developers receive immediate feedback on their code changes.
*   **Increased Confidence**: Ensures that new features or bug fixes don't break existing functionality.
*   **Collaborative Development**: Promotes a consistent code standard across all contributors.
