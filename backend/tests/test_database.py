import pytest
from backend.database import create_engine, Base, get_db
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.main import app
from backend.models import Video, Comment
from unittest.mock import patch

@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def client(engine, db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]

def test_create_video(client, db):
    with patch('backend.main.fetch_video_data') as mock_fetch:
        mock_fetch.return_value = {'title': 'Test Video', 'description': 'Test Description'}
        response = client.post("/videos/test_id")
        assert response.status_code == 200
        video = db.query(Video).filter_by(id="test_id").first()
        assert video is not None
        assert video.title == "Test Video"
        assert video.description == "Test Description"

def test_create_comment(client, db):
    video = Video(id="test_id", title="Test Video", description="Test Description")
    db.add(video)
    db.commit()
    response = client.post("/comments", json={"video_id": "test_id", "text": "Great video!"})
    assert response.status_code == 200
    comment = db.query(Comment).filter_by(text="Great video!").first()
    assert comment is not None
    assert comment.video_id == "test_id"