import pytest

@pytest.mark.django_db
def test_create_immobilie(api_client):

    payload = {
        "title": "my titile",
        "description": "my descriptiom",
        "provider": "my provider",
        "price": 1000000,
            "provider_id": "156",
        "url": "http://www.example.com",
        "location": "privat",
          "type": "house",
          "resource": {
                "name": "ZVG",
                "base_url": "http://www.example.com",
                "crawler": "BLAH"
            }
    }
    response_create = api_client.post("/immoviewer/api/immobilie/", data=payload, format="json")
    assert response_create.status_code == 201
    assert payload['provider_id'] == response_create.data['provider_id']
