import base64
import os
from fastapi.testclient import TestClient
from main import app, fake_users_db, get_password_hash

client = TestClient(app)

def get_token(email, password):
    resp = client.post("/api/login", data={"username": email, "password": password})
    return resp.json()["token"]

def test_profile_image_validation():
    # 테스트용 유저 생성
    email = "imgtest@example.com"
    password = "testpass"
    fake_users_db[email] = {
        "id": 999,
        "email": email,
        "hashed_password": get_password_hash(password),
        "name": "imgtest",
        "role": "mentor",
        "profile": {"name": "imgtest", "bio": "", "imageUrl": "", "skills": []}
    }
    token = get_token(email, password)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. 정상 jpg (500x500)
    with open("tests/sample_500x500.jpg", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": img_b64, "skills": []}, headers=headers)
    assert resp.status_code == 200

    # 2. png, 1000x1000
    with open("tests/sample_1000x1000.png", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": img_b64, "skills": []}, headers=headers)
    assert resp.status_code == 200

    # 3. 400x400 (해상도 오류)
    with open("tests/sample_400x400.jpg", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": img_b64, "skills": []}, headers=headers)
    assert resp.status_code == 400
    assert "해상도" in resp.json()["detail"]

    # 4. 500x600 (정사각형 오류)
    with open("tests/sample_500x600.jpg", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": img_b64, "skills": []}, headers=headers)
    assert resp.status_code == 400
    assert "정사각형" in resp.json()["detail"]

    # 5. 1.5MB jpg (용량 초과)
    with open("tests/sample_1500kb.jpg", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": img_b64, "skills": []}, headers=headers)
    assert resp.status_code == 400
    assert "1MB" in resp.json()["detail"]

    # 6. gif (확장자 오류)
    with open("tests/sample_500x500.gif", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": img_b64, "skills": []}, headers=headers)
    assert resp.status_code == 400
    assert ".jpg" in resp.json()["detail"] or ".png" in resp.json()["detail"]

    # 7. 잘못된 base64
    resp = client.put("/api/profile", json={"name": "imgtest", "role": "mentor", "bio": "", "image": "notbase64", "skills": []}, headers=headers)
    assert resp.status_code == 400
    assert "올바르지 않" in resp.json()["detail"]

# 샘플 이미지는 tests/ 폴더에 준비되어 있어야 합니다.
