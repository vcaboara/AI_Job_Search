import pytest
from unittest.mock import MagicMock, patch
from job_search_module.core import find_job_leads, JobLead
from job_search_module.services.gemini import GeminiService


@pytest.fixture
def mock_gemini_client():
    """Fixture to mock the genai.Client and its generate_content method."""
    with patch('google.genai.Client') as MockClient:
        mock_instance = MockClient.return_value
        # Configure the mock to return a predefined JSON response
        mock_response_text = """[
            {
                "title": "Mocked DevOps Engineer",
                "company": "MockCorp",
                "description": "A simulated DevOps role.",
                "link": "http://mockcorp.com/jobs/devops"
            }
        ]"""
        mock_response = MagicMock()
        mock_response.text = mock_response_text
        mock_instance.models.generate_content.return_value = mock_response

        # Wrap the mocked client in our GeminiService so the core function
        # receives an object implementing `generate_content`.
        service = GeminiService(client=mock_instance)
        # Expose the underlying mock client for assertions in tests
        service._mock_client = mock_instance  # type: ignore[attr-defined]
        yield service


def test_find_job_leads_placeholder(mock_gemini_client):
    """Test that find_job_leads can be called and returns a list of JobLead objects (mocked)."""
    user_query = "test query"
    leads = find_job_leads(user_query=user_query,
                           ai_service=mock_gemini_client)

    # Assert that the underlying mocked client's method was called
    mock_gemini_client._mock_client.models.generate_content.assert_called_once()

    # Assert the return type and content based on the mock
    assert isinstance(leads, list)
    assert len(leads) == 1
    assert isinstance(leads[0], JobLead)
    assert leads[0].title == "Mocked DevOps Engineer"
    assert leads[0].company == "MockCorp"
