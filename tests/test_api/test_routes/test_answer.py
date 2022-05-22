import pytest


@pytest.mark.asyncio
async def test_get_answers(client):
    response = await client.get("/answers/")

    assert response.status_code == 200
