import httpx
import pytest

Response = httpx._models.Response


@pytest.mark.asyncio
async def test_get_questions(client):
    """Return a list of questions given a response."""
    response = await client.get("/questions/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_question(client):
    """Return resource not found given an id that isn't in db."""
    question_id: int = 100

    response: Response = await client.get(f"/questions/{question_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Question {question_id} does not exist."


@pytest.mark.asyncio
async def test_malformed_get_question(client):
    """Return unable to process contained instructions due to incorrect query."""
    bad_id: float = 9.12

    response: Response = await client.get(f"/questions/{bad_id}")

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"
