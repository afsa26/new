from fastapi import FastAPI,Depends
from pydantic import BaseModel
import schemas,models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yeild db
    finally:
        db.close()
        

class Blog(BaseModel):
    title:str
    body:str



@app.post('/Blog')
def create(request:schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title= request.title,body=request,body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/Blog')
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    
    return blogs


@app.get('/Blog/{id}')
def show(id):