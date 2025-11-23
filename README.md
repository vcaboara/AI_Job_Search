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
