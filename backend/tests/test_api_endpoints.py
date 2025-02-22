from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch
import pytest

client = TestClient(app)

def test_sentiment_analysis():
    response = client.post("/analyze", json={"comments": ["Great video!", "Terrible content"]})
    assert response.status_code == 200
    assert len(response.json()["scores"]) == 2

@patch('backend.main.fetch_video_data')
def test_fetch_video_endpoint_success(mock_fetch):
    mock_fetch.return_value = {'title': 'Test Video', 'description': 'Test Description'}
    response = client.get("/videos/test_id")
    assert response.status_code == 200
    assert response.json()['title'] == 'Test Video'

@patch('backend.main.fetch_video_data')
def test_fetch_video_endpoint_not_found(mock_fetch):
    mock_fetch.return_value = None
    response = client.get("/videos/nonexistent_id")
    assert response.status_code == 404

def test_sentiment_analysis_invalid_input():
    response = client.post("/analyze", json={"comments": []})
    assert response.status_code == 400
    assert response.json()["detail"] == "No comments provided"