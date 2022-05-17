from src.main import app
from starlette.testclient import TestClient


client = TestClient(app)


def test_root():
    response = client.get("/tools")

    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_post_question():
    data = {
        "text": "What about Scooby Doo?",
        "publish": False,
        "answers": [
            {
                "text": "He cool.",
                "is_correct": False,
            },
            {
                "text": "He nice.",
                "is_correct": False,
            },
            {
                "text": "He fantastic.",
                "is_correct": False,
            },
            {
                "text": "He smart too.",
                "is_correct": True,
            },
        ],
    }
    response = client.post("/questions", json=data)

    assert response.status_code == 201


def test_too_many_correct_answers():
    data = {
        "text": "What about Scooby Doo?",
        "publish": False,
        "answers": [
            {
                "text": "He cool.",
                "is_correct": False,
            },
            {
                "text": "He nice.",
                "is_correct": False,
            },
            {
                "text": "He fantastic.",
                "is_correct": True,
            },
            {
                "text": "He smart too.",
                "is_correct": True,
            },
        ],
    }
    response = client.post("/questions", json=data)

    message = {
        "detail": [
            {
                "loc": ["body", "answers"],
                "msg": "Please select one correct answer.",
                "type": "assertion_error",
            }
        ]
    }

    assert response.status_code == 422
    assert response.json() == message
