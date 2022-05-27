import httpx
import pytest

Response = httpx._models.Response


@pytest.mark.asyncio
async def test_get_answers(client):
    response: Response = await client.get("/answers/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_answer(client):
    answer_id: int = 1

    response: Response = await client.get(f"/answers/{answer_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_malformed_get_answer(client):
    bad_id: float = 5.2

    response: Response = await client.get(f"/answers/{bad_id}")

    assert response.status_code == 422
