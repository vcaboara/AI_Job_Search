import streamlit as st
import os
import json
from typing import List, Optional
import tempfile # For handling temporary files
import imghdr # For image type detection (optional, but good practice)
import PyPDF2 as pypdf # Import PyPDF2 as pypdf
import docx # Import python-docx
import google.generativeai as genai # Added: Import genai client

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

# 3. API Key Inputs (New)
gemini_api_key_input = st.sidebar.text_input(
    "Gemini API Key:",
    type="password",
    help="Enter your Google Gemini API Key. Will override environment variable."
)

openai_api_key_input = st.sidebar.text_input(
    "OpenAI API Key:",
    type="password",
    help="Enter your OpenAI API Key. Will override environment variable. (Placeholder functionality)"
)

# Instantiate the AI Service based on configuration
ai_service = None

# Determine the actual API key to use for Gemini
gemini_api_key = gemini_api_key_input if gemini_api_key_input else os.getenv('GEMINI_API_KEY')
if not gemini_api_key and IS_COLAB:
    try:
        gemini_api_key = userdata.get('GEMINI_API_KEY')
    except Exception:
        pass # Handled below by a general error message if still not found

# Determine the actual API key to use for OpenAI (placeholder logic)
openai_api_key = openai_api_key_input if openai_api_key_input else os.getenv('OPENAI_API_KEY')


if app_config["AI_SERVICE_TYPE"] == "gemini":
    if not gemini_api_key:
        st.error("GEMINI_API_KEY not found. Please enter it in the sidebar or set it as an environment variable.")
        st.stop()
    # Fixed: Passing api_key directly
    ai_service = GeminiService(model_name=app_config["GEMINI_MODEL_NAME"], api_key=gemini_api_key)
elif app_config["AI_SERVICE_TYPE"] == "openai":
    if not openai_api_key:
        st.warning("OPENAI_API_KEY not found. OpenAI service is currently a placeholder.")
    ai_service = OpenAIService(model_name=app_config["OPENAI_MODEL_NAME"], client=openai_api_key) # Passing key for placeholder
else:
    st.error(f"Unsupported AI_SERVICE_TYPE: {app_config['AI_SERVICE_TYPE']}")
    st.stop()



# Main content area
search_query = st.text_input("Enter Job Search Query", "DevOps Engineer for climate impact")

# 4. File Uploader for context documents
uploaded_file = st.file_uploader("Upload Context Document (e.g., Resume, Job Description)", type=["png", "jpg", "jpeg", "pdf", "txt", "md", "docx"])

context_text = None
context_image_filepath = None
temp_file_paths = [] # To keep track of temporary files for cleanup

MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB
MIN_TEXT_CHAR_COUNT = 50 # Minimum characters for text-based files

if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error(f"File is too large. Max size is {MAX_FILE_SIZE / (1024 * 1024):.0f} MB.")
        uploaded_file = None
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_uploaded_filepath = tmp_file.name
        temp_file_paths.append(temp_uploaded_filepath)

        if uploaded_file.type in ["image/jpeg", "image/png"] or uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            context_image_filepath = temp_uploaded_filepath
            st.success(f"Uploaded image file: {uploaded_file.name}")
        elif uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(('.pdf')):
            try:
                pdf_reader = pypdf.PdfReader(temp_uploaded_filepath)
                extracted_text = ""
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() or ""
                context_text = extracted_text
                st.success(f"Extracted text from PDF: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading PDF file: {e}")
                uploaded_file = None
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_file.name.lower().endswith(('.docx')):
            try:
                document = docx.Document(temp_uploaded_filepath)
                extracted_text = "\n".join([para.text for para in document.paragraphs])
                context_text = extracted_text
                st.success(f"Extracted text from DOCX: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading DOCX file: {e}")
                uploaded_file = None
        elif uploaded_file.type in ["text/plain", "text/markdown"] or uploaded_file.name.lower().endswith(('.txt', '.md')):
            extracted_text = uploaded_file.getvalue().decode("utf-8")
            context_text = extracted_text
            st.success(f"Uploaded text file: {uploaded_file.name}")
        else:
             st.error("Unsupported file type. Please upload PNG, JPG, JPEG, PDF, TXT, MD, or DOCX.")
             uploaded_file = None

    # Validate extracted text content if applicable
    if context_text:
        if not context_text.strip():
            st.error("Extracted text content is empty. Please upload a document with content.")
            context_text = None
        elif len(context_text.strip()) < MIN_TEXT_CHAR_COUNT:
            st.error(f"Extracted text content has too little content ({len(context_text.strip())} characters). Please upload a document with at least {MIN_TEXT_CHAR_COUNT} characters.")
            context_text = None


if st.button("Find Job Leads"):
    if ai_service is None:
        st.error("AI service not initialized. Please select a valid service.")
    else:
        with st.spinner(f"Searching for job leads using {app_config['AI_SERVICE_TYPE']}..."):
            leads = find_job_leads(
                user_query=search_query,
                ai_service=ai_service,
                context_text=context_text, # Pass extracted text content
                context_image_filepath=context_image_filepath # Pass temporary image file path
            )

            if leads:
                st.success(f"Found {len(leads)} Job Leads:")
                for i, lead in enumerate(leads):
                    st.subheader(f"{i+1}. {lead.title} at {lead.company}")
                    st.write(f"**Summary:** {lead.description}")
                    st.markdown(f"**Link:** [Apply Here]({lead.link})")
                    st.markdown("--- (End of Lead) ---")
            else:
                st.info("No job leads were returned for your query. Try a different search term or check your API key.")

    # Clean up all temporary files after processing
    for f_path in temp_file_paths:
        if os.path.exists(f_path):
            os.remove(f_path)
