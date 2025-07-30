# Project Setup with uv

This project uses `uv` for dependency management and virtual environments.

## Installation

1.  **Install `uv`**: If you don't have `uv` installed, you can install it using:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Or for Windows PowerShell:
    # powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    After installation, restart your terminal.

2.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-project-directory>
    ```

## Setting up the Environment

1.  **Pin Python version (Optional)**: If a specific Python version is required for this project, you can pin it:

    ```bash
    uv python pin 3.11 # Replace 3.11 with the required version
    ```

2.  **Initialize the project and install dependencies**:
    ```bash
    uv init
    uv sync
    ```
    This will create a `.venv` virtual environment and install all dependencies listed in `pyproject.toml` and `uv.lock`.

## Running Commands

To run Python scripts or commands within the project's virtual environment, use `uv run`:

```bash
uv run python your_script.py
uv run pytest
```

## IPython Kernel Setup

1.  **Install the IPython kernel**: Replace `YOUR_ENV_NAME` with a descriptive name for your kernel (e.g., your project's name).
    ```bash
    uv run python -m ipykernel install --user --name research --display-name "Python research"
    ```
    This should output sth like: Installed kernelspec research in /Users/user/Library/Jupyter/kernels/research
    After this, you should be able to select "Python research" from the kernel list in Jupyter.

## Project Components

- **Literature Review Search String Generator**: A Python package for generating academic search strings. See its [README.md](src/literature_review/search_string/README.md) for details.
