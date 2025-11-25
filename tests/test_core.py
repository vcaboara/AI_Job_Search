import pytest
from unittest.mock import MagicMock, patch

from job_search_module.core import find_job_leads, JobLead
from job_search_module.services.base import AbstractAIService # Import AbstractAIService

@pytest.fixture
def mock_ai_service():
    """Fixture to mock an AbstractAIService and its generate_content method."""
    mock_instance = MagicMock(spec=AbstractAIService)
    # Configure the mock to return a predefined JSON response
    mock_response_text = """[
        {
            "title": "Mocked DevOps Engineer",
            "company": "MockCorp",
            "description": "A simulated DevOps role.",
            "link": "http://mockcorp.com/jobs/devops"
        }
    ]"""
    mock_instance.generate_content.return_value = mock_response_text
    return mock_instance

def test_find_job_leads_placeholder(mock_ai_service): # Use the new fixture
    """Test that find_job_leads can be called and returns a list of JobLead objects (mocked)."""
    user_query = "test query"
    leads = find_job_leads(user_query=user_query, ai_service=mock_ai_service) # Pass ai_service

    # Assert that the mocked service's method was called
    mock_ai_service.generate_content.assert_called_once()

    # Assert the return type and content based on the mock
    assert isinstance(leads, list)
    assert len(leads) == 1
    assert isinstance(leads[0], JobLead)
    assert leads[0].title == "Mocked DevOps Engineer"
    assert leads[0].company == "MockCorp"
