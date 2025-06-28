from fastapi import FastAPI, Depends, HTTPException, status, Response, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image

app = FastAPI(title="Mentor-Mentee Matching API")

# JWT 설정
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# --- Pydantic Schemas (일부 예시) ---
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str  # mentor or mentee

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

class MentorProfileDetails(BaseModel):
    name: str
    bio: str
    imageUrl: str
    skills: Optional[List[str]] = None

class MenteeProfileDetails(BaseModel):
    name: str
    bio: str
    imageUrl: str

class MentorProfile(BaseModel):
    id: int
    email: EmailStr
    role: str
    profile: MentorProfileDetails

class MenteeProfile(BaseModel):
    id: int
    email: EmailStr
    role: str
    profile: MenteeProfileDetails

class UpdateMentorProfileRequest(BaseModel):
    id: int
    name: str
    role: str
    bio: str
    image: str  # base64 encoded
    skills: List[str]

class UpdateMenteeProfileRequest(BaseModel):
    id: int
    name: str
    role: str
    bio: str
    image: str  # base64 encoded

class MatchRequestCreate(BaseModel):
    mentorId: int
    menteeId: int
    message: str

class MatchRequest(BaseModel):
    id: int
    mentorId: int
    menteeId: int
    message: str
    status: str  # pending, accepted, rejected, cancelled

class MatchRequestOutgoing(BaseModel):
    id: int
    mentorId: int
    menteeId: int
    status: str

# --- 유저 데이터 예시 (실제 구현시 DB로 대체) ---
fake_users_db = {}
fake_match_requests = {}

# --- JWT 유틸 함수 ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(email)
    if user is None:
        raise credentials_exception
    return user

def validate_profile_image(image_b64: str):
    try:
        image_bytes = base64.b64decode(image_b64)
        # 1MB 이하
        if len(image_bytes) > 1024 * 1024:
            raise HTTPException(status_code=400, detail="이미지 크기는 1MB 이하여야 합니다.")
        # 확장자 체크 (Pillow로 대체)
        with Image.open(BytesIO(image_bytes)) as img:
            ext = img.format.lower()
            if ext not in ("jpeg", "png"):
                raise HTTPException(status_code=400, detail="이미지는 .jpg 또는 .png 형식만 허용합니다.")
            w, h = img.size
            if w != h:
                raise HTTPException(status_code=400, detail="이미지는 정사각형이어야 합니다.")
            if w < 500 or w > 1000:
                raise HTTPException(status_code=400, detail="이미지 해상도는 500x500~1000x1000 픽셀이어야 합니다.")
        return image_bytes
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="이미지 파일이 올바르지 않습니다.")

# --- 엔드포인트 ---
@app.post("/api/signup", status_code=201, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def signup(req: SignupRequest):
    try:
        if req.email in fake_users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        fake_users_db[req.email] = {
            "id": len(fake_users_db) + 1,
            "email": req.email,
            "hashed_password": get_password_hash(req.password),
            "name": req.name,
            "role": req.role,
            "profile": {
                "name": req.name,
                "bio": "",
                "imageUrl": f"/images/{req.role}/" + str(len(fake_users_db) + 1),
                "skills": [] if req.role == "mentor" else None
            }
        }
        return Response(status_code=201)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login", response_model=LoginResponse, responses={
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = fake_users_db.get(form_data.username)
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        token = create_access_token({"sub": user["email"]})
        return {"token": token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/me", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "email": "user@example.com",
                    "role": "mentor",
                    "profile": {
                        "name": "Alice",
                        "bio": "Frontend mentor",
                        "imageUrl": "/images/mentor/1",
                        "skills": ["React", "Vue"]
                    }
                }
            }
        }
    },
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def get_me(current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] == "mentor":
            return MentorProfile(
                id=current_user["id"],
                email=current_user["email"],
                role="mentor",
                profile=MentorProfileDetails(
                    name=current_user["profile"]["name"],
                    bio=current_user["profile"].get("bio", ""),
                    imageUrl=current_user["profile"].get("imageUrl", ""),
                    skills=current_user["profile"].get("skills", [])
                )
            )
        else:
            return MenteeProfile(
                id=current_user["id"],
                email=current_user["email"],
                role="mentee",
                profile=MenteeProfileDetails(
                    name=current_user["profile"]["name"],
                    bio=current_user["profile"].get("bio", ""),
                    imageUrl=current_user["profile"].get("imageUrl", "")
                )
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/profile", responses={
    200: {"model": MentorProfile},  # MentorProfile 또는 MenteeProfile 중 하나로 지정
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def update_profile(
    data: dict,  # Union 대신 dict로 받고 내부에서 분기 처리
    current_user: dict = Depends(get_current_user)
):
    try:
        user = fake_users_db.get(current_user["email"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        # 이미지 저장(메모리)
        image = data.get("image")
        if image:
            image_bytes = validate_profile_image(image)
            user["profile"]["image_bytes"] = image_bytes
        user["profile"]["name"] = data.get("name", user["profile"]["name"])
        user["profile"]["bio"] = data.get("bio", user["profile"].get("bio", ""))
        if user["role"] == "mentor":
            user["profile"]["skills"] = data.get("skills", user["profile"].get("skills", []))
            return MentorProfile(
                id=user["id"],
                email=user["email"],
                role="mentor",
                profile=MentorProfileDetails(
                    name=user["profile"]["name"],
                    bio=user["profile"].get("bio", ""),
                    imageUrl=user["profile"].get("imageUrl", ""),
                    skills=user["profile"].get("skills", [])
                )
            )
        else:
            return MenteeProfile(
                id=user["id"],
                email=user["email"],
                role="mentee",
                profile=MenteeProfileDetails(
                    name=user["profile"]["name"],
                    bio=user["profile"].get("bio", ""),
                    imageUrl=user["profile"].get("imageUrl", "")
                )
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/{role}/{id}", responses={
    200: {"content": {"image/jpeg": {}}},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def get_profile_image(role: str, id: int, current_user: dict = Depends(get_current_user)):
    try:
        for user in fake_users_db.values():
            if user["role"] == role and user["id"] == id:
                image_bytes = user["profile"].get("image_bytes")
                if not image_bytes:
                    raise HTTPException(status_code=404, detail="No image found")
                return StreamingResponse(BytesIO(image_bytes), media_type="image/jpeg")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mentors", responses={
    200: {"content": {"application/json": {"example": []}}},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def get_mentors(skill: Optional[str] = None, order_by: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentee":
            raise HTTPException(status_code=401, detail="Only mentee can access mentor list")
        mentors = [u for u in fake_users_db.values() if u["role"] == "mentor"]
        if skill:
            mentors = [m for m in mentors if skill in (m["profile"].get("skills") or [])]
        if order_by == "skill":
            mentors.sort(key=lambda m: (m["profile"].get("skills") or [""])[0])
        elif order_by == "name":
            mentors.sort(key=lambda m: m["profile"].get("name", ""))
        else:
            mentors.sort(key=lambda m: m["id"])
        result = [MentorProfile(
            id=m["id"],
            email=m["email"],
            role="mentor",
            profile=MentorProfileDetails(
                name=m["profile"]["name"],
                bio=m["profile"].get("bio", ""),
                imageUrl=m["profile"].get("imageUrl", ""),
                skills=m["profile"].get("skills", [])
            )
        ) for m in mentors]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 매칭 요청 관련 엔드포인트 ---
@app.post("/api/match-requests", response_model=MatchRequest, responses={
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def create_match_request(req: MatchRequestCreate, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentee":
            raise HTTPException(status_code=401, detail="Only mentee can send match requests")
        mentor = next((u for u in fake_users_db.values() if u["id"] == req.mentorId and u["role"] == "mentor"), None)
        if not mentor:
            raise HTTPException(status_code=400, detail="Mentor not found")
        match_id = len(fake_match_requests) + 1
        match = {
            "id": match_id,
            "mentorId": req.mentorId,
            "menteeId": req.menteeId,
            "message": req.message,
            "status": "pending"
        }
        fake_match_requests[match_id] = match
        return match
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/match-requests/incoming", response_model=List[MatchRequest], responses={
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def get_incoming_match_requests(current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentor":
            raise HTTPException(status_code=401, detail="Only mentor can view incoming requests")
        return [m for m in fake_match_requests.values() if m["mentorId"] == current_user["id"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/match-requests/outgoing", response_model=List[MatchRequestOutgoing], responses={
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def get_outgoing_match_requests(current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentee":
            raise HTTPException(status_code=401, detail="Only mentee can view outgoing requests")
        return [MatchRequestOutgoing(**{k: v for k, v in m.items() if k in ["id", "mentorId", "menteeId", "status"]}) for m in fake_match_requests.values() if m["menteeId"] == current_user["id"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/match-requests/{id}/accept", response_model=MatchRequest, responses={
    404: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def accept_match_request(id: int, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentor":
            raise HTTPException(status_code=401, detail="Only mentor can accept requests")
        match = fake_match_requests.get(id)
        if not match:
            raise HTTPException(status_code=404, detail="Match request not found")
        match["status"] = "accepted"
        return match
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/match-requests/{id}/reject", response_model=MatchRequest, responses={
    404: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def reject_match_request(id: int, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentor":
            raise HTTPException(status_code=401, detail="Only mentor can reject requests")
        match = fake_match_requests.get(id)
        if not match:
            raise HTTPException(status_code=404, detail="Match request not found")
        match["status"] = "rejected"
        return match
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/match-requests/{id}", response_model=MatchRequest, responses={
    404: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def cancel_match_request(id: int, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "mentee":
            raise HTTPException(status_code=401, detail="Only mentee can cancel requests")
        match = fake_match_requests.get(id)
        if not match:
            raise HTTPException(status_code=404, detail="Match request not found")
        match["status"] = "cancelled"
        return match
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/swagger-ui")

@app.get("/swagger-ui", include_in_schema=False)
def swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")
