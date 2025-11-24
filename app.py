import streamlit as st
import os
import json
from typing import List, Optional

# Conditional import for Colab-specific modules
try:
    from google.colab import userdata
    IS_COLAB = True
except ImportError:
    IS_COLAB = False

# Import the refactored components from the new module
from job_search_module.core import JobLead, find_job_leads

# Ensure GEMINI_API_KEY is set (for Colab context or local env)
# This logic must be before any calls to the find_job_leads function
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

# --- Streamlit App --- #
st.title("Gemini Job Lead Finder")
st.write("Enter your job search query to find relevant leads. This app uses the Gemini API.")

search_query = st.text_input("Enter Job Search Query", "DevOps Engineer for climate impact")

if st.button("Find Job Leads"):
    if not os.getenv("GEMINI_API_KEY"):
        st.error("GEMINI_API_KEY is not set. Please add it to Colab secrets or your environment variables.")
    else:
        with st.spinner("Searching for job leads..."):
            # Call the imported find_job_leads function
            leads = find_job_leads(user_query=search_query, context_filepath=None)

            if leads:
                st.success(f"Found {len(leads)} Job Leads:")
                for i, lead in enumerate(leads):
                    st.subheader(f"{i+1}. {lead.title} at {lead.company}")
                    st.write(f"**Summary:** {lead.description}")
                    st.markdown(f"**Link:** [Apply Here]({lead.link})")
                    st.markdown("--- (End of Lead) ---")
            else:
                st.info("No job leads were returned for your query. Try a different search term.")
