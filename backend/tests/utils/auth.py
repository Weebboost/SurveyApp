from fastapi.testclient import TestClient

def user_authentication_header(*, client: TestClient, email: str, password: str) -> dict[str:str]:
    data = {"username": email, "password": password}
    r = client.post("/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers