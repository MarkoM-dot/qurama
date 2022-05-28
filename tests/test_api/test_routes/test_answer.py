import httpx
import pytest

Response = httpx._models.Response


@pytest.mark.asyncio
async def test_get_answers(client):
    """Return a list of answers given a response."""
    response: Response = await client.get("/answers/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_answer(client):
    """Return resource not found given an id that isn't in db."""
    answer_id: int = 100

    response: Response = await client.get(f"/answers/{answer_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Answer {answer_id} does not exist."


@pytest.mark.asyncio
async def test_malformed_get_answer(client):
    """Return unable to process contained instructions due to incorrect query."""
    bad_id: float = 5.2

    response: Response = await client.get(f"/answers/{bad_id}")

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"
