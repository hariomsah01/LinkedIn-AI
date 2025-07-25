from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.auth import router as auth_router
from app.models import UserImage, User
from app.image_processor import process_image
import shutil, os, uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)

@app.post("/upload")
def upload_image(user_id: int = Form(...), file: UploadFile = File(...), session: Session = Depends(get_session)):
    ext = os.path.splitext(file.filename)[-1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    upload_path = f"app/static/uploads/{unique_name}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processed_filename = process_image(upload_path)
    image = UserImage(filename=unique_name, processed_filename=processed_filename, user_id=user_id)
    session.add(image)
    session.commit()
    return {
        "message": "Image uploaded and processed",
        "original": f"/static/uploads/{unique_name}",
        "processed": f"/static/processed/{processed_filename}"
    }

@app.get("/gallery/{user_id}")
def get_user_gallery(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    images = session.exec(select(UserImage).where(UserImage.user_id == user_id)).all()
    return {
        "user": user.username,
        "images": [
            {"original": f"/static/uploads/{img.filename}", "processed": f"/static/processed/{img.processed_filename}"}
            for img in images
        ]
    }
