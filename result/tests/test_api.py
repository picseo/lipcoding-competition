import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_signup_login_me():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        # 회원가입
        resp = await ac.post("/api/signup", json={
            "email": "user@example.com",
            "password": "password123",
            "name": "김멘토",
            "role": "mentor"
        })
        assert resp.status_code == 201

        # 로그인
        resp = await ac.post("/api/login", data={
            "username": "user@example.com",
            "password": "password123"
        })
        assert resp.status_code == 200
        token = resp.json()["token"]

        # 내 정보 조회
        resp = await ac.get("/api/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "user@example.com"
        assert data["role"] == "mentor"

@pytest.mark.asyncio
async def test_full_api_flow():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        # 1. 멘토 회원가입
        mentor_email = "mentor@example.com"
        mentor_pw = "pw123456"
        resp = await ac.post("/api/signup", json={
            "email": mentor_email,
            "password": mentor_pw,
            "name": "멘토유저",
            "role": "mentor"
        })
        assert resp.status_code == 201

        # 2. 멘티 회원가입
        mentee_email = "mentee@example.com"
        mentee_pw = "pw654321"
        resp = await ac.post("/api/signup", json={
            "email": mentee_email,
            "password": mentee_pw,
            "name": "멘티유저",
            "role": "mentee"
        })
        assert resp.status_code == 201

        # 3. 멘토 로그인
        resp = await ac.post("/api/login", data={
            "username": mentor_email,
            "password": mentor_pw
        })
        assert resp.status_code == 200
        mentor_token = resp.json()["token"]

        # 4. 멘티 로그인
        resp = await ac.post("/api/login", data={
            "username": mentee_email,
            "password": mentee_pw
        })
        assert resp.status_code == 200
        mentee_token = resp.json()["token"]

        # 5. 멘토 내 정보 조회
        resp = await ac.get("/api/me", headers={"Authorization": f"Bearer {mentor_token}"})
        assert resp.status_code == 200
        mentor_id = resp.json()["id"]

        # 6. 멘티 내 정보 조회
        resp = await ac.get("/api/me", headers={"Authorization": f"Bearer {mentee_token}"})
        assert resp.status_code == 200
        mentee_id = resp.json()["id"]

        # 7. 멘토 프로필 수정 (이미지, 스킬 포함)
        import base64
        img_bytes = base64.b64encode(b"dummyimage").decode()
        resp = await ac.put("/api/profile", headers={"Authorization": f"Bearer {mentor_token}"}, json={
            "id": mentor_id,
            "name": "멘토수정",
            "role": "mentor",
            "bio": "백엔드 멘토",
            "image": img_bytes,
            "skills": ["FastAPI", "Python"]
        })
        assert resp.status_code == 200
        assert resp.json()["profile"]["skills"] == ["FastAPI", "Python"]

        # 8. 멘티 프로필 수정 (이미지)
        resp = await ac.put("/api/profile", headers={"Authorization": f"Bearer {mentee_token}"}, json={
            "id": mentee_id,
            "name": "멘티수정",
            "role": "mentee",
            "bio": "프론트엔드 멘티",
            "image": img_bytes
        })
        assert resp.status_code == 200
        assert resp.json()["profile"]["name"] == "멘티수정"

        # 9. 멘토 프로필 이미지 조회
        resp = await ac.get(f"/api/images/mentor/{mentor_id}", headers={"Authorization": f"Bearer {mentor_token}"})
        assert resp.status_code == 200

        # 10. 멘티가 멘토 리스트 조회 (필터/정렬)
        resp = await ac.get("/api/mentors", headers={"Authorization": f"Bearer {mentee_token}"})
        assert resp.status_code == 200
        assert any(m["email"] == mentor_email for m in resp.json())

        resp = await ac.get("/api/mentors?skill=FastAPI", headers={"Authorization": f"Bearer {mentee_token}"})
        assert resp.status_code == 200
        assert any("FastAPI" in m["profile"]["skills"] for m in resp.json())

        # 11. 멘티가 멘토에게 매칭 요청
        resp = await ac.post("/api/match-requests", headers={"Authorization": f"Bearer {mentee_token}"}, json={
            "mentorId": mentor_id,
            "menteeId": mentee_id,
            "message": "멘토링 요청합니다!"
        })
        assert resp.status_code == 200
        match_id = resp.json()["id"]

        # 12. 멘토가 받은 매칭 요청 목록 조회
        resp = await ac.get("/api/match-requests/incoming", headers={"Authorization": f"Bearer {mentor_token}"})
        assert resp.status_code == 200
        assert any(m["id"] == match_id for m in resp.json())

        # 13. 멘티가 보낸 매칭 요청 목록 조회
        resp = await ac.get("/api/match-requests/outgoing", headers={"Authorization": f"Bearer {mentee_token}"})
        assert resp.status_code == 200
        assert any(m["id"] == match_id for m in resp.json())

        # 14. 멘토가 매칭 요청 수락
        resp = await ac.put(f"/api/match-requests/{match_id}/accept", headers={"Authorization": f"Bearer {mentor_token}"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "accepted"

        # 15. 멘토가 매칭 요청 거절 (상태 변경 테스트, 실제로는 이미 accepted라서 상태만 확인)
        resp = await ac.put(f"/api/match-requests/{match_id}/reject", headers={"Authorization": f"Bearer {mentor_token}"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "rejected"

        # 16. 멘티가 매칭 요청 취소
        resp = await ac.delete(f"/api/match-requests/{match_id}", headers={"Authorization": f"Bearer {mentee_token}"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "cancelled"
