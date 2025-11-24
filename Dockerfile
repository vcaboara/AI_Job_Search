# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy necessary project files and directories
COPY job_search_module/ job_search_module/
COPY app.py .
COPY requirements.txt .
<<<<<<< HEAD
COPY setup.py . # Added setup.py
COPY README.md . # Added README.md

# Upgrade pip and install project dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
=======
COPY setup.py .
COPY README.md .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt
>>>>>>> 61ae92d9877ce1c72fc021455de1c71aa6074cbe

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
