
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

## Pre-commit Hooks

To ensure code quality and prevent broken code from being checked into the repository, this project utilizes `pre-commit` hooks. These hooks run automatically before each commit, performing checks like linting, formatting, and running unit tests.

### Installation and Usage

1.  **Install `pre-commit`**: First, ensure `pre-commit` is installed in your development environment. If you installed the `dev` dependencies using `pip install -e '.[dev]'`, it should already be available. Otherwise, you can install it separately:
    ```bash
pip install pre-commit
    ```

2.  **Install the Git Hooks**: Navigate to your project's root directory and install the Git hooks. This command sets up `pre-commit` to run the configured hooks automatically:
    ```bash
pre-commit install
    ```

3.  **Commit Your Changes**: From now on, whenever you run `git commit`, the configured hooks will execute. If any hook fails (e.g., due to linting errors or failing tests), the commit will be aborted, allowing you to fix the issues before committing. You can temporarily skip hooks with `git commit -n` or `git commit --no-verify` (use with caution).

### Configured Hooks

The `.pre-commit-config.yaml` file includes the following hooks:

*   **`trailing-whitespace`**: Removes superfluous whitespace at the end of lines.
*   **`end-of-file-fixer`**: Ensures files end with a newline.
*   **`check-yaml`**, **`check-json`**, **`check-toml`**: Checks YAML, JSON, and TOML files for syntax errors.
*   **`check-added-large-files`**: Prevents adding large files to the repository.
*   **`flake8`**: A comprehensive linting tool for Python code.
*   **`autopep8`**: Automatically formats Python code to conform to PEP 8 style guidelines.
*   **`pytest`**: Runs all unit tests to catch regressions and ensure code correctness.

By using these hooks, we can maintain a consistent and high-quality codebase effortlessly.

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

## Pre-commit Hooks

To ensure code quality and prevent broken code from being checked into the repository, this project utilizes `pre-commit` hooks. These hooks run automatically before each commit, performing checks like linting, formatting, and running unit tests.

### Installation and Usage

1.  **Install `pre-commit`**: First, ensure `pre-commit` is installed in your development environment. If you installed the `dev` dependencies using `pip install -e '.[dev]'`, it should already be available. Otherwise, you can install it separately:
    ```bash
pip install pre-commit
    ```

2.  **Install the Git Hooks**: Navigate to your project's root directory and install the Git hooks. This command sets up `pre-commit` to run the configured hooks automatically:
    ```bash
pre-commit install
    ```

3.  **Commit Your Changes**: From now on, whenever you run `git commit`, the configured hooks will execute. If any hook fails (e.g., due to linting errors or failing tests), the commit will be aborted, allowing you to fix the issues before committing. You can temporarily skip hooks with `git commit -n` or `git commit --no-verify` (use with caution).

### Configured Hooks

The `.pre-commit-config.yaml` file includes the following hooks:

*   **`trailing-whitespace`**: Removes superfluous whitespace at the end of lines.
*   **`end-of-file-fixer`**: Ensures files end with a newline.
*   **`check-yaml`**, **`check-json`**, **`check-toml`**: Checks YAML, JSON, and TOML files for syntax errors.
*   **`check-added-large-files`**: Prevents adding large files to the repository.
*   **`flake8`**: A comprehensive linting tool for Python code.
*   **`autopep8`**: Automatically formats Python code to conform to PEP 8 style guidelines.
*   **`pytest`**: Runs all unit tests to catch regressions and ensure code correctness.

By using these hooks, we can maintain a consistent and high-quality codebase effortlessly.

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
