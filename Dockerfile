# Use a Python base image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy necessary project files and directories
COPY requirements.txt .
# Upgrade pip and install project dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY setup.py .
COPY README.md .
COPY app.py .
COPY job_search_module/ job_search_module/

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
