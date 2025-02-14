def test_login(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "teacher3@mail.ru", "password": "testPass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
