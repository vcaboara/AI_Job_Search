import streamlit as st
import os
import json
from typing import List, Optional
import tempfile # For handling temporary files
import imghdr # For image type detection (optional, but good practice)

# Conditional import for Colab-specific modules
try:
    from google.colab import userdata
    IS_COLAB = True
except ImportError:
    IS_COLAB = False

# Import the refactored components from the new module
from job_search_module.core import JobLead, find_job_leads
from job_search_module.services.gemini import GeminiService
from job_search_module.services.openai import OpenAIService # Imported OpenAIService
from job_search_module.config import load_config

# Load initial application configuration
app_config = load_config()

# --- Streamlit App --- #
st.title("AI-Powered Job Lead Finder")
st.write("Configure your AI service and search for job leads. This app uses the selected AI API.")

# Sidebar for configuration
st.sidebar.header("AI Service Configuration")

# 1. AI Service Type Selection
ai_service_type = st.sidebar.selectbox(
    "Select AI Service:",
    ("gemini", "openai"),
    index=("gemini", "openai").index(app_config["AI_SERVICE_TYPE"])
)

# Update config based on selection
app_config["AI_SERVICE_TYPE"] = ai_service_type

# 2. Model Name Inputs
current_gemini_model = st.sidebar.text_input(
    "Gemini Model Name:",
    value=app_config["GEMINI_MODEL_NAME"],
    disabled=(ai_service_type != "gemini")
)
if ai_service_type == "gemini":
    app_config["GEMINI_MODEL_NAME"] = current_gemini_model

current_openai_model = st.sidebar.text_input(
    "OpenAI Model Name:",
    value=app_config["OPENAI_MODEL_NAME"],
    disabled=(ai_service_type != "openai")
)
if ai_service_type == "openai":
    app_config["OPENAI_MODEL_NAME"] = current_openai_model


# Instantiate the AI Service based on configuration
ai_service = None
if app_config["AI_SERVICE_TYPE"] == "gemini":
    # Ensure GEMINI_API_KEY is set (for Colab context or local env)
    if 'GEMINI_API_KEY' not in os.environ:
        if IS_COLAB:
            try:
                os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')
            except Exception:
                st.error("GEMINI_API_KEY not found. Please set it in Colab secrets or your environment variables.")
                st.stop()
        else:
            st.error("GEMINI_API_KEY not found. Please set it as an environment variable.")
            st.stop()
    ai_service = GeminiService(model_name=app_config["GEMINI_MODEL_NAME"])
elif app_config["AI_SERVICE_TYPE"] == "openai":
    # Placeholder for OpenAI API Key check (similar logic as Gemini if needed)
    # if 'OPENAI_API_KEY' not in os.environ:
    #    st.error("OPENAI_API_KEY not found...")
    #    st.stop()
    ai_service = OpenAIService(model_name=app_config["OPENAI_MODEL_NAME"])
else:
    st.error(f"Unsupported AI_SERVICE_TYPE: {app_config['AI_SERVICE_TYPE']}")
    st.stop()



# Main content area
search_query = st.text_input("Enter Job Search Query", "DevOps Engineer for climate impact")

# 3. File Uploader for context documents
uploaded_file = st.file_uploader("Upload Context Document (e.g., Resume, Job Description)", type=["png", "jpg", "jpeg", "pdf", "txt", "md", "docx"])

context_filepath = None
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB

if uploaded_file is not None:
    # 4. Implement basic file checks
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error(f"File is too large. Max size is {MAX_FILE_SIZE / (1024 * 1024):.0f} MB.")
        uploaded_file = None # Invalidate file
    else:
        # Check content type if it's an image for more accurate mime type
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            # Use imghdr to verify image format (optional, but good practice)
            # For simplicity, we trust uploaded_file.type for now.
            pass
        elif uploaded_file.type not in ["application/pdf", "text/plain", "text/markdown", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
             st.error("Unsupported file type. Please upload PNG, JPG, JPEG, PDF, TXT, MD, or DOCX.")
             uploaded_file = None # Invalidate file

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            context_filepath = tmp_file.name
        st.success(f"Uploaded file: {uploaded_file.name}")


if st.button("Find Job Leads"):
    if ai_service is None:
        st.error("AI service not initialized. Please select a valid service.")
    elif app_config["AI_SERVICE_TYPE"] == "gemini" and not os.getenv("GEMINI_API_KEY"):
        st.error("GEMINI_API_KEY is not set. Please add it to Colab secrets or your environment variables.")
    else:
        with st.spinner(f"Searching for job leads using {app_config['AI_SERVICE_TYPE']}..."):
            leads = find_job_leads(user_query=search_query, ai_service=ai_service, context_filepath=context_filepath)

            if leads:
                st.success(f"Found {len(leads)} Job Leads:")
                for i, lead in enumerate(leads):
                    st.subheader(f"{i+1}. {lead.title} at {lead.company}")
                    st.write(f"**Summary:** {lead.description}")
                    st.markdown(f"**Link:** [Apply Here]({lead.link})")
                    st.markdown("--- (End of Lead) ---")
            else:
                st.info("No job leads were returned for your query. Try a different search term or check your API key.")

    # Clean up temporary file if it was created
    if context_filepath and os.path.exists(context_filepath):
        os.remove(context_filepath)
