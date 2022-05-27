import pytest
import httpx


Response = httpx._models.Response

@pytest.mark.asyncio
async def test_get_questions(client):
    response = await client.get("/questions/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_question(client):
    
    question_id: int = 1

    response: Response = await client.get(f"/questions/{question_id}")

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_malformed_get_question(client):
    bad_id: float = 9.12

    response: Response = await client.get(f"/questions/{bad_id}")

    assert response.status_code == 422
