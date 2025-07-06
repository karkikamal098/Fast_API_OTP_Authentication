from typing import List, Union
from fastapi import FastAPI, Depends, status, Response, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from .database import engine,SessionLocal
from . import schemas, models
from sqlalchemy.orm import Session
from .utils import hash_password, verify_password, create_access_token,verify_token
from .email_utils import generate_otp, send_otp_email
from .otp_store import save_otp, verify_otp

import smtplib
from email.message import EmailMessage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)



models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/blog")
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": "Blog created successfully", "blog": new_blog}


@app.get("/blog", response_model = list[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Blog with id {id} not found"}
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Blog)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog



@app.post("/user/signup", response_model= schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserSignUp, db:Session = Depends(get_db)):
    hashed_password = hash_password(request.password)
    new_user = models.User(email=request.email, password=hashed_password, name=request.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/user/login", status_code=status.HTTP_200_OK)
def login(request: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



# otp send and verification
@app.post("/send-otp")
async def send_otp(data: schemas.EmailRequest, background_tasks: BackgroundTasks):
    otp = generate_otp()
    save_otp(data.email, otp)
    background_tasks.add_task(send_otp_email, data.email, otp)
    return {"message": "OTP sent successfully"}


@app.post("/verify-otp")
def verify_otp_route(data: schemas.OTPVerifyRequest):
    if verify_otp(data.email, data.otp):
        return {"message": "OTP verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

