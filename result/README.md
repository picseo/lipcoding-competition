# Mentor-Mentee Matching App (FastAPI)

## 프로젝트 개요
- FastAPI 기반 멘토-멘티 매칭 백엔드
- OpenAPI 명세(`openapi.yaml`) 및 요구사항 문서 기반 구현

## 실행 방법

1. 의존성 설치
```
pip install -r requirements.txt
```
2. 서버 실행
```
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## 주요 기능
- 회원가입/로그인(JWT)
- 프로필 관리
- 멘토 목록 조회/검색
- 매칭 요청/수락/거절/취소

## 참고
- API 명세: `openapi.yaml`
- 요구사항: requirements 폴더 내 문서
